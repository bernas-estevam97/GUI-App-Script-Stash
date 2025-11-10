# custom_scroll.py
import customtkinter as ctk
import tkinter as tk

class SimpleScrollableFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        # Determine background color for the canvas
        fg_color = self.cget("fg_color")
        if isinstance(fg_color, (tuple, list)):
            mode = ctk.get_appearance_mode().lower()
            bg_color = fg_color[0] if mode == "light" else fg_color[1]
        else:
            bg_color = fg_color

        # Canvas + scrollbar
        self.canvas = tk.Canvas(self, highlightthickness=0, bd=0, bg=bg_color)
        self.v_scrollbar = ctk.CTkScrollbar(self, orientation="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self._on_vscroll)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.v_scrollbar.grid(row=0, column=1, sticky="ns")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Inner frame
        self.inner_frame = ctk.CTkFrame(self, fg_color=bg_color)
        self.window = self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        # Bindings
        self.inner_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        # Bind mouse wheel globally once
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)  # Windows/macOS
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)    # Linux scroll up
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)    # Linux scroll down

    def _on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.window, width=event.width)

    def _on_vscroll(self, *args):
        self.v_scrollbar.set(*args)
        lo, hi = float(args[0]), float(args[1])
        if lo <= 0.0 and hi >= 1.0:
            self.v_scrollbar.grid_remove()
        else:
            self.v_scrollbar.grid(row=0, column=1, sticky="ns")

    def _on_mousewheel(self, event):
        # Windows/macOS
        if hasattr(event, "delta") and event.delta != 0:
            self.canvas.yview_scroll(-1 * int(event.delta / 120), "units")
        # Linux
        elif event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")
