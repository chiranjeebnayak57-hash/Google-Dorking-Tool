#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
import urllib.parse
import sys

class SmartDorkBrowser:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Dork Searcher (Linux Edition)")
        self.root.geometry("450x350")
        self.root.resizable(False, False)

        # 'clam' theme generally looks the cleanest across different Linux desktop environments
        style = ttk.Style()
        try:
            style.theme_use('clam')
        except tk.TclError:
            pass # Fallback to default if clam is missing for some reason

        self.create_widgets()

    def create_widgets(self):
        # --- Main Frame ---
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Search Topic ---
        ttk.Label(main_frame, text="Search Topic / Keywords:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.search_entry = ttk.Entry(main_frame, width=40)
        self.search_entry.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(0, 15))
        self.search_entry.focus()

        # --- File Type Dropdown ---
        ttk.Label(main_frame, text="Target File Type:").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))

        self.file_types = {
            "PDF Document (.pdf)": "pdf",
            "Word Document (.doc/.docx)": "docx",
            "Excel Spreadsheet (.xls/.xlsx)": "xlsx",
            "PowerPoint (.ppt/.pptx)": "pptx",
            "Text File (.txt)": "txt",
            "CSV Data (.csv)": "csv",
            "Log File (.log)": "log"
        }

        self.file_type_combo = ttk.Combobox(main_frame, values=list(self.file_types.keys()), state="readonly", width=37)
        self.file_type_combo.current(0)
        self.file_type_combo.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(0, 15))

        # --- Optional Site Filter ---
        ttk.Label(main_frame, text="Target Specific Site (Optional):").grid(row=4, column=0, sticky=tk.W, pady=(0, 5))
        self.site_entry = ttk.Entry(main_frame, width=40)
        self.site_entry.insert(0, "e.g., edu, gov, or example.com")
        self.site_entry.bind("<FocusIn>", self.clear_placeholder)
        self.site_entry.grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=(0, 15))

        # --- Browser Selection (Linux Optimized) ---
        ttk.Label(main_frame, text="Open Results In:").grid(row=6, column=0, sticky=tk.W, pady=(0, 5))

        # Linux specific executable mappings
        self.browsers = {
            "System Default (xdg-open)": None,
            "Firefox": "firefox",
            "Google Chrome": "google-chrome",
            "Chromium": "chromium-browser", # or 'chromium' depending on distro
            "Brave Browser": "brave-browser",
            "Opera": "opera"
        }

        self.browser_combo = ttk.Combobox(main_frame, values=list(self.browsers.keys()), state="readonly", width=37)
        self.browser_combo.current(0)
        self.browser_combo.grid(row=7, column=0, columnspan=2, sticky=tk.W, pady=(0, 20))

        # --- Search Button ---
        search_btn = ttk.Button(main_frame, text="Execute Smart Search", command=self.execute_search)
        search_btn.grid(row=8, column=0, columnspan=2, pady=5)

    def clear_placeholder(self, event):
        if self.site_entry.get() == "e.g., edu, gov, or example.com":
            self.site_entry.delete(0, tk.END)

    def execute_search(self):
        query = self.search_entry.get().strip()

        if not query:
            messagebox.showwarning("Input Error", "Please enter a search topic.")
            return

        selected_file_desc = self.file_type_combo.get()
        file_ext = self.file_types[selected_file_desc]
        dork_query = f'"{query}" filetype:{file_ext}'

        site_filter = self.site_entry.get().strip()
        if site_filter and site_filter != "e.g., edu, gov, or example.com":
            dork_query += f' site:{site_filter}'

        encoded_query = urllib.parse.quote_plus(dork_query)
        google_url = f"https://www.google.com/search?q={encoded_query}"

        selected_browser_name = self.browser_combo.get()
        browser_key = self.browsers[selected_browser_name]

        try:
            if browser_key is None:
                # On Linux, this effectively calls xdg-open
                webbrowser.open(google_url)
            else:
                try:
                    # Register the browser command just in case Python's internal list misses it
                    # The '%s' is where the URL gets injected
                    webbrowser.register(browser_key, None, webbrowser.BackgroundBrowser(browser_key))
                    target_browser = webbrowser.get(browser_key)
                    target_browser.open(google_url)
                except webbrowser.Error:
                    messagebox.showwarning("Browser Not Found",
                                           f"Could not locate '{browser_key}' in your system PATH.\n\nOpening in system default browser instead.")
                    webbrowser.open(google_url)

        except Exception as e:
            messagebox.showerror("Execution Error", f"An unexpected error occurred:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartDorkBrowser(root)
    root.mainloop()
