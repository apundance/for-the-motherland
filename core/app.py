import tkinter as tk


class Application:
    def __init__(
        self,
        screen_registry,
        start_screen,
        project_root,
        services=None
    ):
        self.root = tk.Tk()
        self.root.title("App")
        self.root.geometry("800x600")

        self.project_root = project_root

        # Generic dependency container
        self.services = services or {}

        self.screens = screen_registry
        self.current_screen = None

        self.show_screen(start_screen)

    def show_screen(self, name):
        if self.current_screen:
            self.current_screen.destroy()

        screen_class = self.screens[name]
        self.current_screen = screen_class(self)
        self.current_screen.pack(fill="both", expand=True)

        # NEW LINE
        if hasattr(self.current_screen, "on_show"):
            self.current_screen.on_show()
        

    def run(self):
        self.root.mainloop()