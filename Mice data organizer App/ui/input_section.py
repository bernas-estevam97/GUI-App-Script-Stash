# input_section.py
import customtkinter as ctk
from tkinter import filedialog
import os


class InputSection(ctk.CTkFrame):
    def __init__(self, parent, get_script_callback):
        super().__init__(parent, corner_radius=12, border_width=1)
        self.get_script = get_script_callback
        self.directory_path = ctk.StringVar()

        # Label (dynamic depending on script)
        self.label = ctk.CTkLabel(self, text="📂 Input Directory:", font=ctk.CTkFont(size=13, weight="bold"))
        self.label.pack(anchor="w", padx=10, pady=(10, 5))

        # Frame to hold entry + button
        self.frame = ctk.CTkFrame(self, fg_color=("gray90", "gray13"))
        self.frame.pack(fill="x", padx=10, pady=(10, 5))

        # Entry for directory/file path
        self.entry = ctk.CTkEntry(
            self.frame,
            textvariable=self.directory_path,
            placeholder_text="Select a directory or file"
        )
        self.entry.pack(side="left", expand=True, fill="x", padx=(0, 10), pady=10)

        # Browse button
        self.button = ctk.CTkButton(self.frame, text="Browse", command=self.browse)
        self.button.pack(side="right", pady=10)

        

    def update_label(self):
        """Periodically check the selected script and update label text."""
        script = self.get_script()
        if script == "Mouseframe data organizer":
            self.label.configure(text="📊 Choose your Excel File:")
        else:
            self.label.configure(text="📂 Input Directory:")
        self.after(500, self.update_label)  # keep updating in case user switches script

    def browse(self):
        script = self.get_script()
        if script == "Mouseframe data organizer":
            file = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
            if file and file.endswith((".xlsx", ".xls")):
                self.directory_path.set(file)
        else:
            path = filedialog.askdirectory()
            if path and os.path.isdir(path):
                self.directory_path.set(path)
