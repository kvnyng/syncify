import yt_dlp
import os


def search_youtube(query, max_results=5):
    """
    Searches YouTube using yt-dlp and returns a list of results with metadata.
    """
    options = {
        "quiet": True,
        "format": "bestaudio/best",
        "default_search": "ytsearch",
        "noplaylist": True,
        "skip_download": True,
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        try:
            search_results = ydl.extract_info(
                f"ytsearch{max_results}:{query}", download=False
            )
            return search_results["entries"]
        except Exception as e:
            print(f"[YouTube] Search failed for: {query}\n{e}")
            return []


def progress_hook(d):
    """
    Displays progress updates during download.
    """
    if d["status"] == "downloading":
        percent = d.get("_percent_str", "").strip()
        speed = d.get("_speed_str", "").strip()
        eta = d.get("_eta_str", "").strip()
        print(f"\rDownloading... {percent} at {speed} (ETA: {eta})", end="", flush=True)
    elif d["status"] == "finished":
        print("\nDownload complete. Finalizing...")


def download_audio(url, output_path):
    """
    Downloads audio from YouTube and saves it as an M4A at the given path.
    """
    options = {
        "format": "bestaudio[ext=m4a]/bestaudio/best",
        "outtmpl": output_path,
        "quiet": True,
        "noplaylist": True,
        "progress_hooks": [progress_hook],
        # No postprocessing needed — keep native m4a
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        try:
            ydl.download([url])
            return True
        except Exception as e:
            print(f"\n[YouTube] Download failed: {e}")
            return False


def download_track_from_youtube(
    search_query, output_path, expected_duration_sec=None, tolerance=10
):
    """
    Finds and downloads the best YouTube match for a track, considering duration.

    :param search_query: e.g. "Artist - Song Title"
    :param output_path: Where to save the final audio file
    :param expected_duration_sec: Track duration in seconds (Spotify)
    :param tolerance: Seconds of +/- allowed mismatch
    """
    results = search_youtube(search_query)
    if not results:
        print(f"[YouTube] No results for: {search_query}")
        return False

    best_match = None
    min_duration_diff = float("inf")

    for entry in results:
        duration = entry.get("duration")
        if not duration:
            continue

        if expected_duration_sec:
            diff = abs(duration - expected_duration_sec)
            if diff <= tolerance and diff < min_duration_diff:
                best_match = entry
                min_duration_diff = diff
        else:
            best_match = entry
            break

    if not best_match:
        print(f"[YouTube] No suitable match for: {search_query}")
        return False

    print(
        f"[YouTube] Downloading: {best_match['title']} ({best_match['duration']} sec)"
    )
    return download_audio(best_match["webpage_url"], output_path)
