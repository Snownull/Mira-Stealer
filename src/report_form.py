"""
Report Form (Notification System)
Converted from C# ReportFrm.cs class
"""

import tkinter as tk
from tkinter import messagebox
import threading
import time
import os

class ReportForm:
    """Notification popup form"""
    
    def __init__(self, parent=None):
        self.parent = parent
        self.window = None
        self.fade_thread = None
        
    def show_notification(self, title="New Client Connected", message="Data received successfully", duration=5):
        """Show a notification popup"""
        try:
            # Create the notification window
            self.window = tk.Toplevel(self.parent) if self.parent else tk.Tk()
            
            # Configure window
            self.window.title(title)
            self.window.geometry("350x150")
            self.window.resizable(False, False)
            
            # Set window properties
            self.window.attributes('-topmost', True)
            self.window.overrideredirect(True)  # Remove window decorations
            
            # Position at top-right of screen
            screen_width = self.window.winfo_screenwidth()
            screen_height = self.window.winfo_screenheight()
            x = screen_width - 370
            y = 20
            self.window.geometry(f"350x150+{x}+{y}")
            
            # Style the window
            self.window.configure(bg="#2C3E50")
            
            # Create content frame
            content_frame = tk.Frame(self.window, bg="#2C3E50", padx=20, pady=15)
            content_frame.pack(fill=tk.BOTH, expand=True)
            
            # Title label
            title_label = tk.Label(
                content_frame,
                text=title,
                font=("Segoe UI", 12, "bold"),
                bg="#2C3E50",
                fg="#3498DB"
            )
            title_label.pack(anchor=tk.W)
            
            # Message label
            message_label = tk.Label(
                content_frame,
                text=message,
                font=("Segoe UI", 10),
                bg="#2C3E50",
                fg="#ECF0F1",
                wraplength=300,
                justify=tk.LEFT
            )
            message_label.pack(anchor=tk.W, pady=(5, 10))
            
            # Close button
            close_btn = tk.Button(
                content_frame,
                text="✕",
                command=self._close_window,
                bg="#E74C3C",
                fg="white",
                font=("Segoe UI", 10, "bold"),
                relief=tk.FLAT,
                width=3,
                height=1
            )
            close_btn.pack(anchor=tk.E)
            
            # Start fade animation after duration
            self.window.after(duration * 1000, self._start_fade_out)
            
            # Play notification sound (if available)
            self._play_notification_sound()
            
            # Show the window
            self.window.deiconify()
            
        except Exception as e:
            print(f"Error showing notification: {e}")
    
    def _play_notification_sound(self):
        """Play notification sound"""
        try:
            # Try to play system notification sound
            # On different platforms, this would be different
            # For now, we'll skip audio in this environment
            pass
        except Exception as e:
            print(f"Could not play notification sound: {e}")
    
    def _start_fade_out(self):
        """Start the fade out animation"""
        if self.window and self.window.winfo_exists():
            self.fade_thread = threading.Thread(target=self._fade_out_animation, daemon=True)
            self.fade_thread.start()
    
    def _fade_out_animation(self):
        """Fade out animation"""
        try:
            if not self.window or not self.window.winfo_exists():
                return
                
            # Fade out steps
            fade_steps = 10
            for i in range(fade_steps, -1, -1):
                if not self.window or not self.window.winfo_exists():
                    break
                    
                opacity = i / fade_steps
                
                # Schedule the opacity change on the main thread
                self.window.after_idle(lambda op=opacity: self._set_opacity(op))
                
                time.sleep(0.1)
            
            # Close the window
            self.window.after_idle(self._close_window)
            
        except Exception as e:
            print(f"Error in fade animation: {e}")
    
    def _set_opacity(self, opacity):
        """Set window opacity"""
        try:
            if self.window and self.window.winfo_exists():
                self.window.attributes('-alpha', opacity)
        except Exception as e:
            print(f"Error setting opacity: {e}")
    
    def _close_window(self):
        """Close the notification window"""
        try:
            if self.window and self.window.winfo_exists():
                self.window.destroy()
                self.window = None
        except Exception as e:
            print(f"Error closing window: {e}")

class NotificationManager:
    """Manages multiple notifications"""
    
    def __init__(self, parent=None):
        self.parent = parent
        self.notifications = []
        
    def show_client_connected(self, client_ip):
        """Show notification for new client connection"""
        notification = ReportForm(self.parent)
        notification.show_notification(
            title="New Client Connected!",
            message=f"Client {client_ip} has connected and sent data.",
            duration=5
        )
        self.notifications.append(notification)
        
    def show_mnemonic_received(self, wallet_type):
        """Show notification for received mnemonic"""
        notification = ReportForm(self.parent)
        notification.show_notification(
            title="Mnemonic Received!",
            message=f"{wallet_type} wallet mnemonic has been received.",
            duration=4
        )
        self.notifications.append(notification)
        
    def show_passwords_received(self, count):
        """Show notification for received passwords"""
        notification = ReportForm(self.parent)
        notification.show_notification(
            title="Passwords Received!",
            message=f"Received {count} passwords from client.",
            duration=4
        )
        self.notifications.append(notification)
        
    def show_error(self, error_message):
        """Show error notification"""
        notification = ReportForm(self.parent)
        notification.show_notification(
            title="Error",
            message=error_message,
            duration=6
        )
        self.notifications.append(notification)
        
    def clear_all(self):
        """Clear all notifications"""
        for notification in self.notifications:
            if notification.window and notification.window.winfo_exists():
                notification._close_window()
        self.notifications.clear()