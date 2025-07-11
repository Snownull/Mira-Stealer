"""
Data Viewer Components
Enhanced grids and viewers for displaying collected data
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import json
from datetime import datetime
from .models import *

class DataGrid:
    """Enhanced data grid widget"""
    
    def __init__(self, parent, columns, column_widths=None):
        self.parent = parent
        self.columns = columns
        self.column_widths = column_widths or {}
        self.data = []
        
        self._create_widget()
    
    def _create_widget(self):
        """Create the treeview widget"""
        # Create frame for treeview and scrollbars
        self.frame = tk.Frame(self.parent)
        
        # Create treeview
        self.tree = ttk.Treeview(self.frame, columns=self.columns, show="headings", height=15)
        
        # Configure columns
        for col in self.columns:
            width = self.column_widths.get(col, 100)
            self.tree.column(col, width=width, anchor=tk.CENTER)
            self.tree.heading(col, text=col, anchor=tk.CENTER)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(self.frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack everything
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Configure grid weights
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
    
    def pack(self, **kwargs):
        """Pack the frame"""
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        """Grid the frame"""
        self.frame.grid(**kwargs)
    
    def clear(self):
        """Clear all data"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.data.clear()
    
    def add_row(self, values):
        """Add a row to the grid"""
        self.tree.insert("", tk.END, values=values)
        self.data.append(values)
    
    def get_selected(self):
        """Get selected row data"""
        selection = self.tree.selection()
        if selection:
            return self.tree.item(selection[0])['values']
        return None
    
    def export_to_csv(self, filename):
        """Export data to CSV file"""
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                # Write headers
                writer.writerow(self.columns)
                # Write data
                writer.writerows(self.data)
            return True
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export data: {str(e)}")
            return False

class ClientDataViewer:
    """Viewer for client connection data"""
    
    def __init__(self, parent):
        self.parent = parent
        self.grid = None
        self._create_ui()
    
    def _create_ui(self):
        """Create the UI"""
        # Title
        title = tk.Label(self.parent, text="Client Connections", 
                        font=("Segoe UI", 14, "bold"))
        title.pack(pady=10)
        
        # Buttons frame
        btn_frame = tk.Frame(self.parent)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Export button
        export_btn = tk.Button(btn_frame, text="Export to CSV", 
                              command=self._export_data,
                              bg="#3498DB", fg="white", font=("Segoe UI", 10))
        export_btn.pack(side=tk.LEFT, padx=5)
        
        # Clear button
        clear_btn = tk.Button(btn_frame, text="Clear All", 
                             command=self._clear_data,
                             bg="#E74C3C", fg="white", font=("Segoe UI", 10))
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Refresh button
        refresh_btn = tk.Button(btn_frame, text="Refresh", 
                               command=self._refresh_data,
                               bg="#27AE60", fg="white", font=("Segoe UI", 10))
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Data grid
        columns = ["IP", "Country", "OS", "File Type", "File Size", 
                  "Exodus", "Blockchain", "Binance", "MetaMask", 
                  "FileZilla", "Edge Passwords", "Chrome Passwords", "Files"]
        
        column_widths = {
            "IP": 120,
            "Country": 70,
            "OS": 150,
            "File Type": 80,
            "File Size": 100,
            "Exodus": 60,
            "Blockchain": 80,
            "Binance": 70,
            "MetaMask": 80,
            "FileZilla": 70,
            "Edge Passwords": 100,
            "Chrome Passwords": 120,
            "Files": 60
        }
        
        self.grid = DataGrid(self.parent, columns, column_widths)
        self.grid.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def add_client(self, client_data: ClientData):
        """Add client data to the grid"""
        values = [
            client_data.ip,
            client_data.country,
            client_data.os,
            client_data.file_type,
            client_data.file_size,
            client_data.exodus,
            client_data.blockchain,
            client_data.binance,
            client_data.metamask,
            client_data.filezilla,
            client_data.edge_passwords,
            client_data.chrome_passwords,
            client_data.files
        ]
        self.grid.add_row(values)
    
    def _export_data(self):
        """Export data to CSV"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Export Client Data"
        )
        if filename:
            if self.grid.export_to_csv(filename):
                messagebox.showinfo("Success", f"Data exported to {filename}")
    
    def _clear_data(self):
        """Clear all data"""
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all client data?"):
            self.grid.clear()
    
    def _refresh_data(self):
        """Refresh data display"""
        # This would reload data from storage
        pass

class PasswordViewer:
    """Viewer for password data"""
    
    def __init__(self, parent):
        self.parent = parent
        self.grid = None
        self.search_var = None
        self._create_ui()
    
    def _create_ui(self):
        """Create the UI"""
        # Title
        title = tk.Label(self.parent, text="Collected Passwords", 
                        font=("Segoe UI", 14, "bold"))
        title.pack(pady=10)
        
        # Search frame
        search_frame = tk.Frame(self.parent)
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(search_frame, text="Search Website:").pack(side=tk.LEFT)
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=(5, 10))
        
        search_btn = tk.Button(search_frame, text="Search", 
                              command=self._search_passwords,
                              bg="#3498DB", fg="white")
        search_btn.pack(side=tk.LEFT, padx=5)
        
        # Buttons frame
        btn_frame = tk.Frame(self.parent)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Load from disk button
        load_btn = tk.Button(btn_frame, text="Load from Disk", 
                            command=self._load_from_disk,
                            bg="#9B59B6", fg="white", font=("Segoe UI", 10))
        load_btn.pack(side=tk.LEFT, padx=5)
        
        # Export button
        export_btn = tk.Button(btn_frame, text="Export to CSV", 
                              command=self._export_data,
                              bg="#3498DB", fg="white", font=("Segoe UI", 10))
        export_btn.pack(side=tk.LEFT, padx=5)
        
        # Clear button
        clear_btn = tk.Button(btn_frame, text="Clear All", 
                             command=self._clear_data,
                             bg="#E74C3C", fg="white", font=("Segoe UI", 10))
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Data grid
        columns = ["Website", "Username", "Password", "Browser", "Client IP"]
        column_widths = {
            "Website": 200,
            "Username": 150,
            "Password": 150,
            "Browser": 100,
            "Client IP": 120
        }
        
        self.grid = DataGrid(self.parent, columns, column_widths)
        self.grid.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def add_password(self, website, username, password, browser="", client_ip=""):
        """Add password to the grid"""
        values = [website, username, password, browser, client_ip]
        self.grid.add_row(values)
    
    def _search_passwords(self):
        """Search for specific website passwords"""
        search_term = self.search_var.get().strip().lower()
        if not search_term:
            messagebox.showwarning("Warning", "Please enter a website to search for.")
            return
        
        # Filter current data
        filtered_data = []
        for row in self.grid.data:
            if search_term in row[0].lower():  # Search in website column
                filtered_data.append(row)
        
        # Clear and repopulate grid
        self.grid.clear()
        for row in filtered_data:
            self.grid.add_row(row)
        
        messagebox.showinfo("Search Results", f"Found {len(filtered_data)} matches for '{search_term}'")
    
    def _load_from_disk(self):
        """Load passwords from zip files on disk"""
        # This would implement the file scanning functionality
        messagebox.showinfo("Info", "This would scan client files for passwords.")
    
    def _export_data(self):
        """Export data to CSV"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Export Password Data"
        )
        if filename:
            if self.grid.export_to_csv(filename):
                messagebox.showinfo("Success", f"Data exported to {filename}")
    
    def _clear_data(self):
        """Clear all data"""
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all password data?"):
            self.grid.clear()

class WalletViewer:
    """Viewer for wallet data"""
    
    def __init__(self, parent):
        self.parent = parent
        self.metamask_grid = None
        self.exodus_grid = None
        self._create_ui()
    
    def _create_ui(self):
        """Create the UI"""
        # Create notebook for different wallet types
        notebook = ttk.Notebook(self.parent)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # MetaMask tab
        metamask_frame = ttk.Frame(notebook)
        notebook.add(metamask_frame, text="MetaMask Wallets")
        self._create_metamask_tab(metamask_frame)
        
        # Exodus tab
        exodus_frame = ttk.Frame(notebook)
        notebook.add(exodus_frame, text="Exodus Wallets")
        self._create_exodus_tab(exodus_frame)
    
    def _create_metamask_tab(self, parent):
        """Create MetaMask wallet tab"""
        # Title
        title = tk.Label(parent, text="MetaMask Wallets", 
                        font=("Segoe UI", 14, "bold"))
        title.pack(pady=10)
        
        # Buttons
        btn_frame = tk.Frame(parent)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        search_btn = tk.Button(btn_frame, text="Search on Disk", 
                              command=self._search_metamask,
                              bg="#E67E22", fg="white", font=("Segoe UI", 10))
        search_btn.pack(side=tk.LEFT, padx=5)
        
        # Grid
        columns = ["Client IP", "Wallet Data", "Type"]
        self.metamask_grid = DataGrid(parent, columns, {"Client IP": 120, "Wallet Data": 300, "Type": 100})
        self.metamask_grid.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def _create_exodus_tab(self, parent):
        """Create Exodus wallet tab"""
        # Title
        title = tk.Label(parent, text="Exodus Wallets", 
                        font=("Segoe UI", 14, "bold"))
        title.pack(pady=10)
        
        # Buttons
        btn_frame = tk.Frame(parent)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        search_btn = tk.Button(btn_frame, text="Search on Disk", 
                              command=self._search_exodus,
                              bg="#8E44AD", fg="white", font=("Segoe UI", 10))
        search_btn.pack(side=tk.LEFT, padx=5)
        
        # Grid
        columns = ["Client IP", "Wallet Data", "Type"]
        self.exodus_grid = DataGrid(parent, columns, {"Client IP": 120, "Wallet Data": 300, "Type": 100})
        self.exodus_grid.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def _search_metamask(self):
        """Search for MetaMask wallets"""
        messagebox.showinfo("Info", "This would search for MetaMask wallet files on disk.")
    
    def _search_exodus(self):
        """Search for Exodus wallets"""
        messagebox.showinfo("Info", "This would search for Exodus wallet files on disk.")