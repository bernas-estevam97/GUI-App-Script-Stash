import customtkinter as ctk


class ErrorBox(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=12, border_width=1)

        # Title
        self.label = ctk.CTkLabel(
            self,
            text="Logs & Errors",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.label.pack(anchor="w", padx=10, pady=(10, 5))

        # Textbox
        self.textbox = ctk.CTkTextbox(
            self,
            height=120,
            wrap="word"
        )
        self.textbox.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.textbox.configure(state="disabled")

    def log(self, message: str):
        self.textbox.configure(state="normal")
        self.textbox.insert("end", message + "\n")
        self.textbox.see("end")  # auto-scroll to bottom
        self.textbox.configure(state="disabled")

    def clear(self):
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")
        self.textbox.configure(state="disabled")
