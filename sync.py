import os
import argparse
import shutil
from utils.spotify import get_spotify_playlists, get_playlist_tracks
from utils.youtube import download_track_from_youtube
from utils.file_handler import (
    load_json,
    save_json,
    ensure_folder,
    sanitize_filename,
    get_track_filepath,
)
from dotenv import load_dotenv

# Load .env if available
load_dotenv()

# Set root directory for sync output
ROOT_DIR = os.getenv("SYNCIFY_ROOT", os.path.dirname(os.path.abspath(__file__)))
PLAYLISTS_FILE = os.path.join(ROOT_DIR, "playlists.json")
PLAYLISTS_DIR = os.path.join(ROOT_DIR, "playlists")


def print_columns(items, padding=4):
    """
    Nicely prints a list of strings in evenly spaced columns.
    """
    if not items:
        return

    term_width = shutil.get_terminal_size((100, 20)).columns
    max_len = max(len(item) for item in items) + padding
    num_cols = max(1, term_width // max_len)

    for i, item in enumerate(items):
        print(item.ljust(max_len), end="")
        if (i + 1) % num_cols == 0:
            print()
    print()


def list_all_playlists():
    playlists = get_spotify_playlists()
    print("\n🎵 Your Spotify Playlists:")
    items = [f"{name} ({pid})" for pid, name in playlists.items()]
    print_columns(items)


def list_synced_playlists():
    synced = load_json(PLAYLISTS_FILE, default=[])
    if not synced:
        print("\n❌ No playlists are currently synced.")
        return

    print("\n📂 Currently synced playlists:")
    all_playlists = get_spotify_playlists()
    items = [f"{all_playlists.get(pid, 'Unknown Playlist')} ({pid})" for pid in synced]
    print_columns(items)


def add_playlist(playlist_id):
    playlists = get_spotify_playlists()
    if playlist_id not in playlists:
        print(f"\n❌ Playlist ID not found on your account.")
        return

    tracked = load_json(PLAYLISTS_FILE, default=[])
    if playlist_id in tracked:
        print(f"\nℹ️ Playlist is already being tracked.")
    else:
        tracked.append(playlist_id)
        save_json(PLAYLISTS_FILE, tracked)
        print(f"\n✅ Added: {playlists[playlist_id]}")

    # Immediately sync the new playlist
    sync_single_playlist(playlist_id)


def remove_playlist(playlist_id):
    tracked = load_json(PLAYLISTS_FILE, default=[])
    if playlist_id not in tracked:
        print(f"\nℹ️ Playlist is not currently tracked.")
        return

    tracked.remove(playlist_id)
    save_json(PLAYLISTS_FILE, tracked)
    print(f"\n🗑️ Removed playlist from sync list.")


def sync_playlists():
    tracked_playlists = load_json(PLAYLISTS_FILE, default=[])
    if not tracked_playlists:
        print(
            "\n⚠️ No playlists to sync. Add one using: python sync.py add <playlist_id>"
        )
        return

    for playlist_id in tracked_playlists:
        sync_single_playlist(playlist_id)


def sync_single_playlist(playlist_id):
    all_playlists = get_spotify_playlists()
    if playlist_id not in all_playlists:
        print(f"[Spotify] Playlist ID {playlist_id} not found. Skipping.")
        return

    playlist_name, tracks = get_playlist_tracks(playlist_id)
    print(f"\n🎧 Syncing playlist: {playlist_name} ({len(tracks)} tracks)")

    safe_name = sanitize_filename(playlist_name)
    playlist_path = os.path.join(PLAYLISTS_DIR, safe_name)
    ensure_folder(playlist_path)

    playlist_meta_path = os.path.join(playlist_path, "playlist.json")
    local_tracks = load_json(playlist_meta_path, default={})

    for track in tracks:
        track_id = track["id"]
        if track_id in local_tracks:
            continue

        title = f"{track['artist']} - {track['name']}"
        print(f"\n➡️  New track: {title}")

        filepath = get_track_filepath(playlist_path, title)

        success = download_track_from_youtube(
            search_query=title,
            output_path=filepath,
            expected_duration_sec=track["duration"],
        )

        if success:
            local_tracks[track_id] = {
                "title": title,
                "file": os.path.basename(filepath),
                "duration": track["duration"],
            }
            save_json(playlist_meta_path, local_tracks)
        else:
            print(f"[Syncify] Failed to download: {title}")

    # Detect and remove obsolete tracks
    spotify_track_ids = set(track["id"] for track in tracks)
    obsolete_ids = [tid for tid in local_tracks if tid not in spotify_track_ids]

    for tid in obsolete_ids:
        file_to_delete = local_tracks[tid].get("file")
        full_path = os.path.join(playlist_path, file_to_delete)

        try:
            if os.path.exists(full_path):
                os.remove(full_path)
                print(f"🗑️ Removed old track: {file_to_delete}")
        except Exception as e:
            print(f"⚠️ Failed to delete {file_to_delete}: {e}")

        del local_tracks[tid]

    save_json(playlist_meta_path, local_tracks)


def main():
    parser = argparse.ArgumentParser(
        description="🎶 Syncify: Sync your Spotify playlists locally."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    subparsers.add_parser("list", help="Show all Spotify playlists on your account")
    subparsers.add_parser("synced", help="Show playlists currently being synced")

    add_parser = subparsers.add_parser("add", help="Add a playlist to the sync list")
    add_parser.add_argument("playlist_id", help="Spotify Playlist ID")

    remove_parser = subparsers.add_parser(
        "remove", help="Remove a playlist from sync list"
    )
    remove_parser.add_argument("playlist_id", help="Spotify Playlist ID")

    subparsers.add_parser("sync", help="Sync all currently tracked playlists")

    args = parser.parse_args()

    if args.command == "list":
        list_all_playlists()
    elif args.command == "synced":
        list_synced_playlists()
    elif args.command == "add":
        add_playlist(args.playlist_id)
    elif args.command == "remove":
        remove_playlist(args.playlist_id)
    elif args.command == "sync":
        sync_playlists()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
