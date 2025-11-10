import customtkinter as ctk
from tkinter import filedialog
import os
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

        # --- Extra Fields Wrapper (gives border + rounded edges) ---
        self.extra_wrapper = ctk.CTkFrame(
            self,
            corner_radius=10,
            border_width=0,
            fg_color=("gray90", "gray13")
        )
        self.extra_wrapper.columnconfigure(0, weight=1)
        self.extra_wrapper.columnconfigure(1, weight=0)

        # 🔧 Place it once (hidden at start)
        self.extra_wrapper.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))
        self.extra_wrapper.grid_remove()

        # --- Extra Fields inside wrapper ---
        self.extra_frame = ctk.CTkFrame(self.extra_wrapper,fg_color=("gray90", "gray13"))
        self.extra_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        self.extra_frame.columnconfigure(0, weight=1)
        self.extra_frame.columnconfigure(1, weight=0)

        # Output directory
        ctk.CTkLabel(
            self.extra_frame,
            text="📁 Output Directory:",
            font=ctk.CTkFont(weight="bold")
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(5, 0))

        self.output_entry = ctk.CTkEntry(
            self.extra_frame,
            textvariable=self.output_dir_var,
            placeholder_text="Select output directory...",
            height=35
        )
        self.output_entry.grid(row=1, column=0, sticky="ew", padx=(10, 10), pady=(5, 10))

        self.output_browse = ctk.CTkButton(
            self.extra_frame,
            text="Browse",
            width=110,
            height=35,
            command=self.browse_output_dir
        )
        self.output_browse.grid(row=1, column=1, sticky="e", padx=(0, 10), pady=(5, 10))

        # Experiment type
        ctk.CTkLabel(
            self.extra_frame,
            text="🔬 Experimentation Type:",
            font=ctk.CTkFont(weight="bold")
        ).grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=(0, 5))

        self.experiment_entry = ctk.CTkEntry(
            self.extra_frame,
            textvariable=self.experiment_type_var,
            placeholder_text="Enter type",
            height=35
        )
        self.experiment_entry.grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10))

        # --- Run Script Button ---
        self.run_button = ctk.CTkButton(
            self,
            text="▶️ Run Script",
            height=40,
            command=self.run_script
        )
        self.run_button.grid(row=3, column=0, sticky="ew", padx=10, pady=(0, 12))

        # Initialize dropdown state
        self.on_change(self.selected_script.get())

    # --- Handlers ---
    def on_change(self, value):
        """Show/hide extra inputs and update InputSection label immediately."""
        script = value.strip().lower()

        # Update input label
        if script == "mouseframe data organizer":
            self.input_section.label.configure(text="📊 Choose your Excel File:")
            self.extra_wrapper.grid_remove()
            return  # no extra options for this script

        # Default label
        self.input_section.label.configure(text="📂 Input Directory:")

        # Show wrapper for scripts that need output directory
        if script in ("excel filtering", "excel mean time prep"):
            self.extra_wrapper.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))
        else:
            self.extra_wrapper.grid_remove()
            return

        # 🔬 Show/Hide Experimentation field based on script type
        if script == "excel mean time prep":
            self.experiment_entry.grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10))
            # Also show its label
            for widget in self.extra_frame.winfo_children():
                if isinstance(widget, ctk.CTkLabel) and "Experimentation" in widget.cget("text"):
                    widget.grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=(0, 5))
        else:
            # Hide experiment field and its label for other scripts
            self.experiment_entry.grid_remove()
            for widget in self.extra_frame.winfo_children():
                if isinstance(widget, ctk.CTkLabel) and "Experimentation" in widget.cget("text"):
                    widget.grid_remove()


    def browse_output_dir(self):
        path = filedialog.askdirectory()
        if path and os.path.isdir(path):
            self.output_dir_var.set(path)

    def run_script(self):
        self.clear_log()
        try:
            script = self.selected_script.get().strip().lower()
            input_path = self.input_getter()

            if not input_path:
                raise ValueError("Please select a valid input path.")

            # --- MOUSEFRAME DATA ORGANIZER ---
            if script == "mouseframe data organizer":
                if not os.path.isfile(input_path):
                    raise ValueError("Please select a valid Excel file (.xlsx/.xls).")
                
                output_file = mouseframe_data_organizer.run(input_path)
                self.log(f"✅ Extracted data saved inside: {os.path.dirname(output_file)}")
                self.log(f"📄 Output file: {os.path.basename(output_file)}")

            # --- EXCEL FILTERING ---
            elif script == "excel filtering":
                if not os.path.isdir(input_path):
                    raise ValueError("Please select a valid input directory.")
                
                output_dir = self.output_getter()
                if not output_dir or not os.path.isdir(output_dir):
                    output_dir = input_path  # default to same folder

                self.log(f"▶️ Running Excel Filtering...")
                excel_filtering.run(input_path, output_dir, log_fn=self.log)

            # --- EXCEL MEAN TIME PREP ---
            elif script == "excel mean time prep":
                if not os.path.isdir(input_path):
                    raise ValueError("Please select a valid input directory.")
                
                output_dir = self.output_getter()
                experiment = self.experiment_getter()

                if not output_dir or not os.path.isdir(output_dir):
                    output_dir = input_path  # default to same folder

                if not experiment:
                    raise ValueError("Please enter an experimentation type before running.")

                self.log(f"▶️ Running Excel Mean Time Prep...")
                excel_mean_time_prep.run(input_path, output_dir, experiment, log_fn=self.log)

            else:
                raise ValueError("Invalid script selected.")

            self.log(f"✅ {self.selected_script.get()} completed successfully.")

        except Exception as e:
            import traceback
            self.log(f"❌ Error: {str(e)}\n{traceback.format_exc()}")


        except Exception as e:
            import traceback
            self.log(f"❌ Error: {str(e)}\n{traceback.format_exc()}")

    def get_selected_script(self):
        return self.selected_script.get()
