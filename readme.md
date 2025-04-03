# Syncify

Syncify is a command-line tool that syncs your Spotify playlists to your local machine as `.m4a` audio files — by matching and downloading them from YouTube using `yt-dlp`.

Each playlist is saved in its own folder with a JSON manifest for tracking changes. Syncify will only download missing tracks and automatically delete tracks that are removed from your Spotify playlists.

GitHub: https://github.com/kvnyng/syncify

## Features

- Sync specific Spotify playlists to your local music folder
- Matches tracks to YouTube and downloads best-quality `.m4a`
- Skips tracks that are already downloaded
- Automatically deletes tracks no longer in the Spotify playlist
- Works as a global CLI command: `syncify`
- Easy `.env` configuration for Spotify credentials & save path

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/kvnyng/syncing.git
cd syncing
```

### 2. Configure your `.env`

Copy the example file and fill in your credentials:

```bash
cp .env.example .env
```

Then open `.env` and set your Spotify API credentials and your preferred local music folder.

### 3. Run the installer

```bash
chmod +x install.sh
./install.sh
```

This will:
- Create a Python virtual environment in `.venv`
- Install all required packages
- Register `syncify` as a global terminal command
- Load your `.env` for Spotify + local config

## .env Example

```env
# Spotify API credentials
SPOTIPY_CLIENT_ID=your_spotify_client_id
SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
SPOTIPY_REDIRECT_URI=http://127.0.0.1:8888/callback

# Local sync destination
SYNCIFY_ROOT=/Users/yourname/Documents/Music/spotify
```

Get Spotify API credentials here: https://developer.spotify.com/dashboard

## CLI Usage

Once installed, you can run `syncify` from anywhere:

```bash
syncify list
syncify synced
syncify add <id>
syncify remove <id>
syncify sync
```

## Folder Structure

```
/Your/Chosen/Syncify/Folder/
├── playlists.json
├── playlists/
│   ├── Chill Vibes/
│   │   ├── playlist.json
│   │   ├── Mac Miller - Circles.m4a
```

## Behavior Notes

- Only downloads tracks that are missing
- Cleans up deleted Spotify tracks locally
- Saves all music as `.m4a`
- Uses `yt-dlp` with optional FFmpeg

## Requirements

- Python 3.8+
- yt-dlp
- Optional: ffmpeg
- Spotify Developer Account + App

## Credits

- Built by https://github.com/kvnyng
- Powered by:
  - Spotipy: https://spotipy.readthedocs.io/
  - yt-dlp: https://github.com/yt-dlp/yt-dlp
  - python-dotenv: https://github.com/theskumar/python-dotenv

## License

MIT License
