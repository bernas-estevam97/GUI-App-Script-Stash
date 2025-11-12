import customtkinter as ctk
from tkinter import filedialog
import os
import json
from core import excel_filtering, excel_mean_time_prep, mouseframe_data_organizer


class ScriptDropdown(ctk.CTkFrame):
    def __init__(self, parent, input_getter, output_getter, experiment_getter, log_fn, clear_log_fn, input_section):
        super().__init__(parent, corner_radius=12, border_width=1, fg_color=("gray90", "gray13"))

        # External getters / loggers
        self.input_getter = input_getter
        self.output_getter = output_getter
        self.experiment_getter = experiment_getter
        self.log = log_fn
        self.clear_log = clear_log_fn
        self.input_section = input_section

        # State
        self.selected_script = ctk.StringVar(value="Excel Filtering")
        self.output_dir_var = ctk.StringVar()
        self.experiment_type_var = ctk.StringVar()
        self.dict_input_var = ctk.StringVar()

        # Layout base
        self.columnconfigure(0, weight=1)

        # --- Section Title ---
        ctk.CTkLabel(
            self,
            text="⚙️ Script Selection",
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, sticky="w", padx=10, pady=(10, 5))

        # --- Script dropdown ---
        self.dropdown = ctk.CTkOptionMenu(
            self,
            values=["Excel Filtering", "Excel Mean Time Prep", "Mouseframe data organizer"],
            variable=self.selected_script,
            command=self.on_change,
            height=35
        )
        self.dropdown.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))

        # --- Extra Wrapper (consistent style) ---
        self.extra_wrapper = ctk.CTkFrame(
            self, corner_radius=10, border_width=0, fg_color=("gray90", "gray13")
        )
        self.extra_wrapper.columnconfigure(0, weight=1)
        self.extra_wrapper.columnconfigure(1, weight=0)
        self.extra_wrapper.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))

        # --- Inside wrapper ---
        self.extra_frame = ctk.CTkFrame(self.extra_wrapper, fg_color=("gray90", "gray13"))
        self.extra_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        self.extra_frame.columnconfigure(0, weight=1)
        self.extra_frame.columnconfigure(1, weight=0)

        # 📁 Output Directory
        self.output_label = ctk.CTkLabel(
            self.extra_frame, text="📁 Output Directory:", font=ctk.CTkFont(weight="bold")
        )
        self.output_entry = ctk.CTkEntry(
            self.extra_frame, textvariable=self.output_dir_var,
            placeholder_text="Select output directory...", height=35
        )
        self.output_browse = ctk.CTkButton(
            self.extra_frame, text="Browse", width=110, height=35, command=self.browse_output_dir
        )

        # 🔬 Experimentation Type
        self.experiment_label = ctk.CTkLabel(
            self.extra_frame, text="🔬 Experimentation Type:", font=ctk.CTkFont(weight="bold")
        )
        self.experiment_entry = ctk.CTkEntry(
            self.extra_frame, textvariable=self.experiment_type_var,
            placeholder_text="Enter type", height=35
        )

        # 📚 Dictionary Input (for Mouseframe)
        self.dict_label = ctk.CTkLabel(
            self.extra_frame, text="📚 Dictionary (JSON or Python dict):", font=ctk.CTkFont(weight="bold")
        )
        self.dict_entry = ctk.CTkEntry(
            self.extra_frame, textvariable=self.dict_input_var,
            placeholder_text="Paste dict or browse JSON file...", height=35
        )
        self.dict_browse = ctk.CTkButton(
            self.extra_frame, text="Browse", width=110, height=35, command=self.browse_dict_file
        )

        # --- Run Script Button ---
        self.run_button = ctk.CTkButton(
            self, text="▶️ Run Script", height=40, command=self.run_script
        )
        self.run_button.grid(row=3, column=0, sticky="ew", padx=10, pady=(0, 12))

        # Initialize layout
        self.on_change(self.selected_script.get())

    # --- Handlers ---
    def on_change(self, value):
        """Update which fields appear depending on selected script."""
        script = value.strip().lower()

        # Hide everything first
        for w in (
            self.output_label, self.output_entry, self.output_browse,
            self.experiment_label, self.experiment_entry,
            self.dict_label, self.dict_entry, self.dict_browse
        ):
            w.grid_remove()

        # Default: show the wrapper, same padding for all
        self.extra_wrapper.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))

        if script == "mouseframe data organizer":
            # Change label on input section
            self.input_section.label.configure(text="📊 Choose your Excel File:")

            # Show dictionary input only
            self.dict_label.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(5, 0))
            self.dict_entry.grid(row=1, column=0, sticky="ew", padx=(10, 10), pady=(0, 10))
            self.dict_browse.grid(row=1, column=1, sticky="e", padx=(0, 10), pady=(0, 10))
            return

        # For Excel scripts
        self.input_section.label.configure(text="📂 Input Directory:")

        # Always show output directory for Excel scripts
        self.output_label.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(5, 0))
        self.output_entry.grid(row=1, column=0, sticky="ew", padx=(10, 10), pady=(5, 10))
        self.output_browse.grid(row=1, column=1, sticky="e", padx=(0, 10), pady=(5, 10))

        if script == "excel mean time prep":
            self.experiment_label.grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=(0, 5))
            self.experiment_entry.grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10))

    # --- Browsers ---
    def browse_output_dir(self):
        path = filedialog.askdirectory()
        if path and os.path.isdir(path):
            self.output_dir_var.set(path)

    def browse_dict_file(self):
        file = filedialog.askopenfilename(filetypes=[
            ("JSON files", "*.json"), ("Text files", "*.txt"), ("All files", "*.*")
        ])
        if file:
            self.dict_input_var.set(file)

    # --- Run Script Logic ---
    def run_script(self):
        self.clear_log()
        try:
            script = self.selected_script.get().strip().lower()
            input_path = self.input_getter()

            if not input_path:
                raise ValueError("Please select a valid input path.")

            # --- Mouseframe Data Organizer ---
            if script == "mouseframe data organizer":
                if not os.path.isfile(input_path):
                    raise ValueError("Please select a valid Excel file (.xlsx/.xls).")

                dict_input = self.dict_input_var.get().strip()
                user_dict = {}

                if dict_input:
                    if os.path.isfile(dict_input):
                        with open(dict_input, "r", encoding="utf-8") as f:
                            user_dict = json.load(f)
                    else:
                        try:
                            user_dict = eval(dict_input, {"__builtins__": None}, {})
                            if not isinstance(user_dict, dict):
                                raise ValueError
                        except Exception:
                            raise ValueError("Invalid dictionary input. Please enter valid JSON or Python dict literal.")

                self.log("▶️ Running Mouseframe Data Organizer...")
                output_file = mouseframe_data_organizer.run(input_path, user_dict)
                self.log(f"✅ Extracted data saved inside: {os.path.dirname(output_file)}")
                self.log(f"📄 Output file: {os.path.basename(output_file)}")
                return

            # --- Excel Filtering ---
            elif script == "excel filtering":
                if not os.path.isdir(input_path):
                    raise ValueError("Please select a valid input directory.")
                output_dir = self.output_getter() or input_path
                self.log("▶️ Running Excel Filtering...")
                excel_filtering.run(input_path, output_dir, log_fn=self.log)

            # --- Excel Mean Time Prep ---
            elif script == "excel mean time prep":
                if not os.path.isdir(input_path):
                    raise ValueError("Please select a valid input directory.")
                output_dir = self.output_getter() or input_path
                experiment = self.experiment_getter()
                if not experiment:
                    raise ValueError("Please enter an experimentation type before running.")
                self.log("▶️ Running Excel Mean Time Prep...")
                excel_mean_time_prep.run(input_path, output_dir, experiment, log_fn=self.log)

            self.log(f"✅ {self.selected_script.get()} completed successfully.")

        except Exception as e:
            import traceback
            self.log(f"❌ Error: {str(e)}\n{traceback.format_exc()}")

    def get_selected_script(self):
        return self.selected_script.get()
