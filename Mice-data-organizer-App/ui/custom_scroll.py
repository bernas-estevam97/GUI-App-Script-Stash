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

        # Inner frame inside the canvas
        self.inner_frame = ctk.CTkFrame(self, fg_color=bg_color)
        self.window = self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        # Update scroll region when content changes
        self.inner_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        # Initial scroll bindings
        self._bind_all_children()

        # Re-bind every time new widgets are added dynamically
        self.inner_frame.bind("<Map>", lambda e: self._bind_all_children())
        self.inner_frame.bind("<Configure>", lambda e: self._bind_all_children())

    # ------------------ SCROLL BINDINGS ------------------

    def _bind_all_children(self):
        """Force all child widgets (even CTkEntry, CTkButton, etc.) to propagate scroll events."""
        widgets = self.inner_frame.winfo_children()
        queue = list(widgets)
        while queue:
            widget = queue.pop()
            try:
                # Bind directly
                widget.bind("<MouseWheel>", self._on_mousewheel, add="+")
                widget.bind("<Button-4>", self._on_mousewheel, add="+")
                widget.bind("<Button-5>", self._on_mousewheel, add="+")
            except Exception:
                pass
            # If widget has children, process them too
            if isinstance(widget, (tk.Frame, ctk.CTkFrame)):
                queue.extend(widget.winfo_children())

        # Also bind canvas itself (for empty area)
        self.canvas.bind("<MouseWheel>", self._on_mousewheel, add="+")
        self.canvas.bind("<Button-4>", self._on_mousewheel, add="+")
        self.canvas.bind("<Button-5>", self._on_mousewheel, add="+")
        self.inner_frame.bind("<MouseWheel>", self._on_mousewheel, add="+")
        self.inner_frame.bind("<Button-4>", self._on_mousewheel, add="+")
        self.inner_frame.bind("<Button-5>", self._on_mousewheel, add="+")

    # ------------------ SCROLL BEHAVIOR ------------------

    def _on_mousewheel(self, event):
        """Scroll canvas when mouse wheel is used anywhere inside."""
        if event.num == 4:   # Linux scroll up
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5: # Linux scroll down
            self.canvas.yview_scroll(1, "units")
        elif event.delta:    # Windows/macOS
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

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
