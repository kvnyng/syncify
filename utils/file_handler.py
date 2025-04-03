import os
import json
import re


def load_json(filepath, default=None):
    """
    Loads a JSON file. Returns `default` if file doesn't exist.
    """
    if not os.path.exists(filepath):
        return default if default is not None else {}
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(filepath, data):
    """
    Saves a dictionary to a JSON file.
    """
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def ensure_folder(path):
    """
    Creates a folder if it doesn't already exist.
    """
    os.makedirs(path, exist_ok=True)


def sanitize_filename(name):
    """
    Removes characters that are not allowed in filenames (cross-platform).
    """
    name = re.sub(r'[\\/*?:"<>|]', "", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name


def get_track_filepath(playlist_folder, track_title):
    safe_title = sanitize_filename(track_title)
    return os.path.join(playlist_folder, f"{safe_title}.m4a")
