from core.app import Application
from screens.dataset_screen import DatasetScreen
from screens.setting_screen import SettingsScreen
from models.settings_model import SettingsModel


import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# def list_datasets():
    # path = r"C:\Code stuff\cks can suck my balls\datasets"
'''print("\n=== DATASET DEBUG ===")
    print("PATH:", path)
    print("EXISTS:", os.path.exists(path))
    print("FILES:", os.listdir(path) if os.path.exists(path) else "NO FOLDER")
    print("====================\n")

    return os.listdir(path) if os.path.exists(path) else []'''

services = {
    "settings": SettingsModel(PROJECT_ROOT)
}


if __name__ == "__main__":
    screens = {
        "settings": SettingsScreen,
        "dataset": DatasetScreen
    }

    app = Application(
        screen_registry=screens,
        start_screen="dataset",
        project_root=PROJECT_ROOT,
        services=services
    )

    # list_datasets()

    app.run()
