import os
import json


def get_dataset_path(project_root):
    return os.path.join(project_root, "datasets")


def list_datasets(project_root):
    path = get_dataset_path(project_root)

    if not os.path.exists(path):
        return []

    return [f for f in os.listdir(path) if f.endswith(".json")]


def load_dataset(project_root, filename):
    path = os.path.join(project_root, "datasets", filename)

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)