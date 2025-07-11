"""
Language Selector Dialog
Converted from C# Language.cs class
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from .translation_manager import TranslationManager

class LanguageSelector:
    """Language selection dialog window"""
    
    def __init__(self, parent):
        self.parent = parent
        self.result = None
        self.dialog = None
        self.language_var = None
        
    def show(self):
        """Show the language selection dialog and return selected language"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Select Language")
        self.dialog.geometry("400x200")
        self.dialog.resizable(False, False)
        
        # Center the dialog
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Center on screen
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (200 // 2)
        self.dialog.geometry(f"400x200+{x}+{y}")
        
        # Create the UI
        self._create_ui()
        
        # Handle window close
        self.dialog.protocol("WM_DELETE_WINDOW", self._on_cancel)
        
        # Wait for the dialog to close
        self.dialog.wait_window()
        
        return self.result
    
    def _create_ui(self):
        """Create the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title label
        title_label = ttk.Label(
            main_frame, 
            text="Choose Language:",
            font=("Segoe UI", 14, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Language selection frame
        lang_frame = ttk.Frame(main_frame)
        lang_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Language combobox
        self.language_var = tk.StringVar()
        languages = TranslationManager.get_supported_languages()
        
        language_combo = ttk.Combobox(
            lang_frame,
            textvariable=self.language_var,
            values=languages,
            state="readonly",
            font=("Segoe UI", 10),
            width=30
        )
        language_combo.pack(anchor=tk.CENTER)
        language_combo.set("English")  # Default selection
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        # Continue button
        continue_btn = ttk.Button(
            button_frame,
            text="Continue",
            command=self._on_continue,
            style="Accent.TButton"
        )
        continue_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Cancel button
        cancel_btn = ttk.Button(
            button_frame,
            text="Cancel",
            command=self._on_cancel
        )
        cancel_btn.pack(side=tk.RIGHT)
        
        # Set focus and enter key binding
        language_combo.focus()
        self.dialog.bind('<Return>', lambda e: self._on_continue())
        self.dialog.bind('<Escape>', lambda e: self._on_cancel())
    
    def _on_continue(self):
        """Handle continue button click"""
        selected_language = self.language_var.get()
        if not selected_language:
            messagebox.showwarning("Warning", "Please select a language.")
            return
            
        self.result = selected_language
        self.dialog.destroy()
    
    def _on_cancel(self):
        """Handle cancel button click or window close"""
        self.result = None
        self.dialog.destroy()

class LanguageState:
    """Global language state manager"""
    selected_language = "English"
    
    @classmethod
    def set_language(cls, language):
        """Set the current language"""
        cls.selected_language = language
    
    @classmethod
    def get_language(cls):
        """Get the current language"""
        return cls.selected_language
    
    @classmethod
    def translate(cls, key, default_text=""):
        """Get translated text for current language"""
        translation = TranslationManager.get_translation(cls.selected_language, key)
        return translation if translation is not None else default_text