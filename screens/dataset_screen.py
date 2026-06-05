import tkinter as tk
from tkinter import ttk

from core.base_screen import BaseScreen
from controllers.dataset_controller import DatasetController


class DatasetScreen(BaseScreen):
    def __init__(self, app):
        super().__init__(app)
        self.after(100, self.load_datasets)
        self.after(100, lambda: self.app.root.focus_force())
        self.app.root.focus_set()
        self.bind("<Configure>", self.on_resize)
        self.showing_front = True


        self.field_window = None
        self.data_fields = []

        # ===== TOP BAR =====
        top = tk.Frame(self, bg="#2a2a2a")
        top.pack(fill="x")

        self.selected = tk.StringVar()

        self.dropdown = ttk.Combobox(
            top,
            textvariable=self.selected,
            state="readonly",
            width=40
        )
        self.dropdown.bind("<FocusIn>", lambda e: self.app.root.focus_force())
        self.dropdown.pack(side="left", padx=10)

        self.dropdown.bind("<<ComboboxSelected>>", self.on_select)

        tk.Button(
            top,
            text="Settings",
            command=lambda: self.app.show_screen("settings")
        ).pack(side="right", padx=10)

        self.card_counter = tk.Label(
            top,
            text="0 / 0",
            bg="#2a2a2a",
            fg="white",
            font=("Segoe UI", 12)
        )
        self.card_counter.pack(side="left", padx=10)
        

        self.controller = DatasetController(self)

        # ===== DISPLAY =====
        self.display = tk.Label(self, bg="#1e1e1e", fg="white")
        self.display.pack(fill="both", expand=True)

        # nav buttons
        nav = tk.Frame(self, bg="#1e1e1e")
        nav.pack(fill="x")

        tk.Button(nav, text="Prev", command=self.controller.prev_card).pack(side="left")
        tk.Button(nav, text="Next", command=self.controller.next_card).pack(side="left")
        tk.Button(nav, text="Flip", command=self.flip_card).pack(side="left")

    # ===== EVENT → CONTROLLER =====
    def on_select(self, event=None):
        filename = self.selected.get()
        self.controller.load_dataset(filename)

    # ===== CALLED BY CONTROLLER =====
    def render_card(self, card):
        if not card:
            self.display.config(text="No data")
            return

        settings = self.app.services["settings"]

        front = card.get("front", "")
        back = card.get("back", "")

        text = front if self.showing_front else back

        # Get window size dynamically
        width = self.winfo_width()
        height = self.winfo_height()

        if settings.auto_fit:
            font_size = self.calculate_font_size(text, width, height)
        else:
            font_size = 24  # fallback default

        self.display.config(
            text=str(text),
            font=("Segoe UI", font_size),
            justify="center",
            wraplength=max(100, width - 50),
            padx=20,
            pady=20
        )

    def ask_field_selection(self, data):
        if not data:
            return

        sample = data[0]
        fields = list(sample.keys())

        window = tk.Toplevel(self)
        window.title("Choose Flashcard Fields")
        window.geometry("400x400")

        # IMPORTANT: scrollable container safety
        container = tk.Frame(window)
        container.pack(fill="both", expand=True)

        tk.Label(container, text="Front Fields").pack()

        front_vars = {}
        back_vars = {}

        for f in fields:
            row = tk.Frame(container)
            row.pack(fill="x", anchor="w")

            var1 = tk.BooleanVar()
            var2 = tk.BooleanVar()

            tk.Checkbutton(row, text=f"Front: {f}", variable=var1).pack(side="left")
            tk.Checkbutton(row, text=f"Back: {f}", variable=var2).pack(side="left")

            front_vars[f] = var1
            back_vars[f] = var2

        def confirm():
            front = [k for k, v in front_vars.items() if v.get()]
            back = [k for k, v in back_vars.items() if v.get()]

            self.controller.build_flashcards(front, back)
            window.destroy()

        tk.Button(container, text="Build Flashcards", command=confirm).pack(pady=10)

    def load_datasets(self):
        self.after(0, self._load_datasets_impl)


    def _load_datasets_impl(self):
        files = self.controller.get_datasets()

        print("FINAL FILE LIST:", files)

        self.dropdown["values"] = files

        if files:
            self.selected.set(files[0])
            self.dropdown.current(0)

    def flip_card(self):
        self.showing_front = not self.showing_front

        current = self.controller.deck.current()

        if current:
            self.render_card(current)

    def calculate_font_size(self, text, width, height):
        size = height // 12

        if len(text) > 300:
            size *= 0.6
        elif len(text) > 200:
            size *= 0.75
        elif len(text) > 100:
            size *= 0.9

        return max(16, min(int(size), 120))
    
    def on_resize(self, event):
        if hasattr(self.controller, "deck") and self.controller.deck:
            self.render_card(self.controller.deck.current())

    def bind_shortcuts(self):
        settings = self.app.services["settings"]
        root = self.app.root

        def next_card(event):
            self.controller.next_card()
            return "break"

        def prev_card(event):
            self.controller.prev_card()
            return "break"

        def flip_card(event):
            self.flip_card()
            return "break"

        root.bind("<Right>", next_card)
        root.bind("<Left>", prev_card)
        root.bind("<space>", flip_card)

    def on_show(self):
        self.bind_shortcuts()
        self.app.root.focus_force()

    def update_counter(self, current, total):
        self.card_counter.config(text=f"{current} / {total}")
