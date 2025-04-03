from utils.youtube import download_track_from_youtube

# Example test
search_query = "Daft Punk - Harder Better Faster Stronger"
output_path = "test_download.mp3"
expected_duration = 224  # seconds

success = download_track_from_youtube(search_query, output_path, expected_duration)
print("Download successful:", success)
