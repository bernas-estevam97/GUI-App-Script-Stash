import os
import traceback
import customtkinter as ctk
from tkinter import filedialog
import tkinter as tk

# Dummy imports for core scripts
import core.excel_filtering
import core.excel_mean_time_prep
import core.mouseframe_data_organizer

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("CustomTkinter Script Launcher")
        self.wm_title('Mice data organizer')
        self.geometry("600x550")
        self.resizable(False, False)

        # App icon
        try:
            self.iconbitmap("assets/python-icon.ico")  # Windows
        except:
            self.icon_image = tk.PhotoImage(file="assets/python-icon.png")  # Linux/macOS
            self.iconphoto(False, self.icon_image)

        # Variables
        self.directory_path = ctk.StringVar()
        self.output_dir_path = ctk.StringVar()
        self.experiment_type = ctk.StringVar()
        self.script_options = ["Excel Filtering", "Excel Mean time prep", "Mouseframe data organizer"]
        self.selected_script = ctk.StringVar(value=self.script_options[0])

        # ---------- Main Layout Frame ----------
        self.main_content_frame = ctk.CTkFrame(self)
        self.main_content_frame.pack(expand=True, fill="both", padx=20, pady=(20, 0))

        # --- Directory selection ---
        self.dir_label = ctk.CTkLabel(self.main_content_frame, text="Input Directory:")
        self.dir_label.pack(anchor="w")

        self.dir_frame = ctk.CTkFrame(self.main_content_frame)
        self.dir_frame.pack(pady=5, fill="x")

        self.dir_entry = ctk.CTkEntry(
            self.dir_frame,
            textvariable=self.directory_path,
            placeholder_text="Select a directory"
        )
        self.dir_entry.pack(side="left", expand=True, fill="x", padx=(0, 10), pady=5)

        self.browse_button = ctk.CTkButton(self.dir_frame, text="Browse", command=self.browse_directory)
        self.browse_button.pack(side="right", pady=5)

        # --- Script dropdown ---
        self.script_label = ctk.CTkLabel(self.main_content_frame, text="Select Script:")
        self.script_label.pack(anchor="w", pady=(10, 0))

        self.script_dropdown = ctk.CTkOptionMenu(
            self.main_content_frame,
            values=self.script_options,
            variable=self.selected_script,
            command=self.script_changed
        )
        self.script_dropdown.pack(pady=5, fill="x")

        # ---------- Extra Inputs Frame ----------
        self.extra_inputs_frame = ctk.CTkFrame(self.main_content_frame)
        self.extra_inputs_frame.pack(pady=10, fill="x")
        self.extra_inputs_frame.pack_forget()  # Hidden initially

        # --- Output directory ---
        self.output_dir_label = ctk.CTkLabel(self.extra_inputs_frame, text="Output Directory:")
        self.output_dir_label.pack(anchor="w")

        self.output_dir_inner_frame = ctk.CTkFrame(self.extra_inputs_frame)
        self.output_dir_inner_frame.pack(fill="x", pady=5)

        self.output_dir_entry = ctk.CTkEntry(
            self.output_dir_inner_frame,
            textvariable=self.output_dir_path,
            placeholder_text="Select output directory"
        )
        self.output_dir_entry.pack(side="left", expand=True, fill="x", padx=(0, 10), pady=5)

        self.output_browse_button = ctk.CTkButton(
            self.output_dir_inner_frame,
            text="Browse",
            command=self.browse_output_directory
        )
        self.output_browse_button.pack(side="right", pady=5)

        # --- Experimentation type ---
        self.experiment_label = ctk.CTkLabel(self.extra_inputs_frame, text="Experimentation Type:")
        self.experiment_label.pack(anchor="w", pady=(10, 0))

        self.experiment_entry = ctk.CTkEntry(
            self.extra_inputs_frame,
            textvariable=self.experiment_type,
            placeholder_text="Enter experimentation type"
        )
        self.experiment_entry.pack(fill="x", pady=5)

        # --- Run Script Button (moves depending on context) ---
        self.run_button_dynamic = ctk.CTkButton(self.extra_inputs_frame, text="Run Script", command=self.run_selected_script)
        self.run_button_static = ctk.CTkButton(self.main_content_frame, text="Run Script", command=self.run_selected_script)
        self.run_button_static.pack(pady=10)

        # --- Error Output Box ---
        self.error_box = ctk.CTkTextbox(self, height=100)
        self.error_box.pack(side="bottom", fill="x", padx=20, pady=10)
        self.error_box.configure(state="disabled")

    # ---------- Methods ----------
    def browse_directory(self):
        try:
            selected_dir = filedialog.askdirectory()
            if selected_dir and os.path.isdir(selected_dir):
                self.directory_path.set(selected_dir)
                self.clear_error()
            else:
                raise FileNotFoundError("Selected path is not a valid directory.")
        except Exception as e:
            self.log_error(e)

    def browse_output_directory(self):
        try:
            selected_dir = filedialog.askdirectory()
            if selected_dir and os.path.isdir(selected_dir):
                self.output_dir_path.set(selected_dir)
                self.clear_error()
            else:
                raise FileNotFoundError("Selected output path is not valid.")
        except Exception as e:
            self.log_error(e)

    def script_changed(self, selected_script):
        if selected_script == "Excel Mean time prep":
            self.extra_inputs_frame.pack(pady=10, fill="x")
            self.run_button_static.pack_forget()
            self.run_button_dynamic.pack(pady=10)
        else:
            self.extra_inputs_frame.pack_forget()
            self.run_button_dynamic.pack_forget()
            self.run_button_static.pack(pady=10)

    def run_selected_script(self):
        try:
            dir_path = self.directory_path.get()
            script = self.selected_script.get()

            if not dir_path or not os.path.isdir(dir_path):
                raise ValueError("Please select a valid input directory.")

            if script == "Excel Filtering":
                self.excel_filtering_run(dir_path)
            elif script == "Excel Mean time prep":
                self.excel_mean_time_prep_run(dir_path)
            elif script == "Mouseframe data organizer":
                self.mouseframe_data_organizer_run(dir_path)
            else:
                raise ValueError("Unknown script selected.")
        except Exception as e:
            self.log_error(e)

    def excel_filtering_run(self, path):
        last_directory = os.path.basename(os.path.dirname(path))
        self.clear_error()
        self.error_box.configure(state="normal")
        self.error_box.insert("end", f"Excel filtering ran successfully on: {last_directory}\n")
        self.error_box.configure(state="disabled")

    def excel_mean_time_prep_run(self, path):
        output_dir = self.output_dir_path.get()
        experiment = self.experiment_type.get()

        if not output_dir or not os.path.isdir(output_dir):
            raise ValueError("Please select a valid output directory.")
        if not experiment:
            raise ValueError("Please enter an experimentation type.")

        last_directory = os.path.basename(os.path.dirname(path))
        self.clear_error()
        self.error_box.configure(state="normal")
        self.error_box.insert("end", f"Excel mean time prep ran successfully on: {last_directory}\n")
        self.error_box.insert("end", f"Output Dir: {output_dir} | Experiment: {experiment}\n")
        self.error_box.configure(state="disabled")

    def mouseframe_data_organizer_run(self, path):
        file_name = os.path.basename(path)
        self.clear_error()
        self.error_box.configure(state="normal")
        self.error_box.insert("end", f"Mouseframe data organizer ran successfully on file: {file_name}\n")
        self.error_box.configure(state="disabled")

    def log_error(self, error):
        self.error_box.configure(state="normal")
        self.error_box.insert("end", f"Error: {str(error)}\n{traceback.format_exc()}\n")
        self.error_box.configure(state="disabled")

    def clear_error(self):
        self.error_box.configure(state="normal")
        self.error_box.delete("1.0", "end")
        self.error_box.configure(state="disabled")


if __name__ == "__main__":
    app = App()
    app.mainloop()
