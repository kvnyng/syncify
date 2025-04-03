import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

# These should be set in your environment or .env file
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv(
    "SPOTIPY_REDIRECT_URI", "http://localhost:8888/callback"
)

SCOPE = "playlist-read-private playlist-read-collaborative"

# Spotipy client setup
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope=SCOPE,
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        cache_path=".spotify_cache",
    )
)


def get_spotify_playlists():
    """
    Returns a dictionary of {playlist_id: playlist_name} for the current user.
    """
    playlists = {}
    results = sp.current_user_playlists()
    while results:
        for item in results["items"]:
            playlists[item["id"]] = item["name"]
        if results["next"]:
            results = sp.next(results)
        else:
            break
    return playlists


def get_playlist_tracks(playlist_id):
    """
    Returns a tuple (playlist_name, track_list) where each track includes:
    id, name, artist, and duration (in seconds)
    """
    playlist = sp.playlist(playlist_id)
    playlist_name = playlist["name"]
    tracks_data = []

    results = sp.playlist_tracks(playlist_id)
    while results:
        for item in results["items"]:
            track = item["track"]
            if not track:
                continue
            track_info = {
                "id": track["id"],
                "name": track["name"],
                "artist": track["artists"][0]["name"],
                "duration": track["duration_ms"] // 1000,  # in seconds
            }
            tracks_data.append(track_info)
        if results["next"]:
            results = sp.next(results)
        else:
            break

    return playlist_name, tracks_data
