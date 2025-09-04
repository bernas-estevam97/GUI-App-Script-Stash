# main_window.py
import customtkinter as ctk
from ui.input_section import InputSection
from ui.script_dropdown import ScriptDropdown
from ui.error_box import ErrorBox
from ui.custom_scroll import SimpleScrollableFrame  # simplified scrollable frame

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Mice Data Organizer")
        self.geometry("600x550")
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")

        # App icon
        try:
            self.iconbitmap("assets/python-icon.ico")
        except:
            self.icon_image = ctk.PhotoImage(file="assets/python-icon.png")
            self.iconphoto(False, self.icon_image)

        # --- Tabs with Unicode icons ---
        self.tab_control = ctk.CTkTabview(self, width=600, height=550)
        self.tab_control.add("🖥 Home")
        self.tab_control.add("❓ Help")
        self.tab_control.pack(expand=True, fill="both", padx=10, pady=10)

        # Optional: Style tab buttons
        self.tab_control.tab("🖥 Home").configure(fg_color=("gray85", "gray25"))
        #self.tab_control.tab("❓ Help").configure(fg_color=("gray15", "gray15"))

        # --- Scrollable frame inside Main tab ---
        self.main_scroll = SimpleScrollableFrame(self.tab_control.tab("🖥 Home"))
        self.main_scroll.pack(expand=True, fill="both")

        # --- Input section ---
        self.input_section = InputSection(
            self.main_scroll.inner_frame,
            get_script_callback=self.get_selected_script
        )
        self.input_section.pack(padx=20, pady=(20, 10), fill="x")

        # --- Error box ---
        self.error_box = ErrorBox(self.main_scroll.inner_frame)
        self.error_box.pack(side="bottom", fill="x", padx=20, pady=10)

        # --- Script dropdown ---
        self.dropdown_section = ScriptDropdown(
            self.main_scroll.inner_frame,
            input_getter=self.get_input_directory,
            output_getter=self.get_output_directory,
            experiment_getter=self.get_experiment_type,
            log_fn=self.error_box.log,
            clear_log_fn=self.error_box.clear,
            input_section=self.input_section
        )
        self.dropdown_section.pack(padx=20, pady=10, fill="x")

        # --- Update dynamic label ---
        self.input_section.update_label()

        # --- Help tab content ---
        help_frame = ctk.CTkFrame(
            self.tab_control.tab("❓ Help"),
            corner_radius=15,
            fg_color=("gray15", "gray25"),  # darker background
            border_width=1,
            border_color=("gray40", "gray60")
        )
        help_frame.pack(expand=True, fill="both", padx=15, pady=15)  # slightly reduced padding

        # Title
        help_title = ctk.CTkLabel(
            help_frame,
            text="❓ How to use Mice Data Organizer",
            font=ctk.CTkFont(size=18, weight="bold"),
            anchor="w"
        )
        help_title.pack(anchor="w", pady=(5, 10), padx=10)  # reduced top padding

        # Instructions
        instructions = [
            ("📂", "Step 1: Select your input directory or Excel file depending on the script."),
            ("⚙️", "Step 2: Choose which script to run from the dropdown menu."),
            ("📁", "Step 3: If needed, select an output directory and enter the experiment type."),
            ("▶️", "Step 4: Click 'Run Script' to process your data."),
        ]

        for icon, text in instructions:
            row = ctk.CTkLabel(
                help_frame,
                text=f"{icon}  {text}",
                font=ctk.CTkFont(size=14),
                anchor="w",
                justify="left"
            )
            row.pack(anchor="w", padx=20, pady=(2, 5))  # smaller top padding

        # Notes section
        notes_title = ctk.CTkLabel(
            help_frame,
            text="📌 Notes:",
            font=ctk.CTkFont(size=15, weight="bold"),
            anchor="w"
        )
        notes_title.pack(anchor="w", padx=20, pady=(10, 5))  # reduced top padding

        notes_text = (
            "- Scroll down if content is out of view.\n"
            "- Mouseframe Data Organizer requires an Excel file input.\n"
            "- Excel Mean Time Prep requires both output directory and experiment type."
        )
        notes_label = ctk.CTkLabel(
            help_frame,
            text=notes_text,
            font=ctk.CTkFont(size=14),
            anchor="w",
            justify="left"
        )
        notes_label.pack(anchor="w", padx=30, pady=(0, 10))

        # --- Button in Main tab to switch to Help ---
        self.help_button = ctk.CTkButton(
            self.main_scroll.inner_frame,
            text="❓ Help",
            command=lambda: self.tab_control.set("❓ Help")
        )
        self.help_button.pack(pady=10)

    # --- Getters ---
    def get_input_directory(self):
        return self.input_section.directory_path.get()

    def get_output_directory(self):
        return self.dropdown_section.output_dir_var.get()

    def get_experiment_type(self):
        return self.dropdown_section.experiment_type_var.get()

    def get_selected_script(self):
        return self.dropdown_section.get_selected_script()


if __name__ == "__main__":
    app = App()
    app.mainloop()
