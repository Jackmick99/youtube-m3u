import subprocess
from pathlib import Path

URL = "https://www.youtube.com/watch?v=wHJHpOP7vjM"

result = subprocess.run(
    [
        "yt-dlp",
        "--no-warnings",
        "--extractor-args",
        "youtube:player_client=web_safari",
        "--get-url",
        "-f",
        "best[protocol*=m3u8]/best",
        URL,
    ],
    capture_output=True,
    text=True,
)

if result.returncode != 0 or not result.stdout.strip():
    print(result.stderr)
    raise SystemExit("Impossibile ottenere lo stream YouTube")

stream_url = result.stdout.strip().splitlines()[-1]

playlist = f"""#EXTM3U
#EXTINF:-1,Diretta YouTube
{stream_url}
"""

Path("youtube.m3u8").write_text(playlist, encoding="utf-8")

print("M3U8 aggiornata.")