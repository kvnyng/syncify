from utils.spotify import get_spotify_playlists, get_playlist_tracks


def main():
    playlists = get_spotify_playlists()
    print("Available playlists:")
    for pid, name in playlists.items():
        print(f"{name} - {pid}")

    # Pick one playlist to inspect tracks
    sample_id = next(iter(playlists))  # first one
    name, tracks = get_playlist_tracks(sample_id)

    print(f"\nTracks in '{name}':")
    for track in tracks[:5]:  # just first 5
        print(f"{track['artist']} - {track['name']} ({track['duration']} sec)")


if __name__ == "__main__":
    main()
