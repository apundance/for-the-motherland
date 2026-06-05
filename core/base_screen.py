import tkinter as tk


class BaseScreen(tk.Frame):
    def __init__(self, app):
        super().__init__(app.root, bg="#1e1e1e")
        self.app = app

    def on_show(self):
        pass