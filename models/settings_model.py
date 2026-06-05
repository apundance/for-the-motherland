import json
import os


class SettingsModel:
    def __init__(self, project_root):
        self.path = os.path.join(project_root, "settings.json")

        self.auto_fit = True

        self.shortcuts = {
            "next": "Right",
            "prev": "Left",
            "flip": "space"
        }

        self.load()

    def load(self):
        if not os.path.exists(self.path):
            return

        with open(self.path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.auto_fit = data.get("auto_fit", True)
        self.shortcuts = data.get("shortcuts", self.shortcuts)

            
    def save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump({
                "auto_fit": self.auto_fit,
                "shortcuts": self.shortcuts
            }, f, indent=4)