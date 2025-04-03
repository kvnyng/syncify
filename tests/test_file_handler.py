from utils.file_handler import ensure_folder, get_track_filepath, sanitize_filename

playlist_name = "My 🔥 Playlist"
track_title = "Drake - God's Plan"

playlist_folder = f"./playlists/{sanitize_filename(playlist_name)}"
ensure_folder(playlist_folder)

output_path = get_track_filepath(playlist_folder, track_title)
print("Will save to:", output_path)
