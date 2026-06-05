import tkinter as tk
from tkinter import ttk
from core.base_screen import BaseScreen


class SettingsScreen(BaseScreen):

    def __init__(self, app):
        super().__init__(app)

        tk.Label(self, text="Settings").pack(pady=10)

        self.auto_fit = tk.BooleanVar(
            value=self.app.services["settings"].auto_fit
        )

        tk.Checkbutton(
            self,
            text="Auto Fit Text",
            variable=self.auto_fit
        ).pack(pady=10)

        tk.Button(
            self,
            text="Save",
            command=self.save_settings
        ).pack(pady=10)

        tk.Button(
            self,
            text="Back",
            command=lambda: self.app.show_screen("dataset")
        ).pack()

    def save_settings(self):
        settings = self.app.services["settings"]
        settings.auto_fit = self.auto_fit.get()
        settings.save()