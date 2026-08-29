import os
import subprocess
from pathlib import Path

URL = "https://www.youtube.com/watch?v=wHJHpOP7vjM"

cookies = os.environ.get("YOUTUBE_COOKIES")

if not cookies:
    raise SystemExit("Secret YOUTUBE_COOKIES non trovato")

cookie_file = Path("cookies.txt")
cookie_file.write_text(cookies, encoding="utf-8")

try:
    result = subprocess.run(
        [
            "yt-dlp",
            "--no-warnings",
            "--cookies", str(cookie_file),
            "--get-url",
            "-f", "best[protocol*=m3u8]/best",
            URL,
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(result.stderr)
        raise SystemExit("Impossibile ottenere lo stream")

    urls = [
        line.strip()
        for line in result.stdout.splitlines()
        if line.strip().startswith("http")
    ]

    if not urls:
        print(result.stdout)
        raise SystemExit("Nessun URL dello stream trovato")

    stream_url = urls[-1]

    playlist = f"""#EXTM3U
#EXTINF:-1,Diretta YouTube
{stream_url}
"""

    Path("youtube.m3u8").write_text(
        playlist,
        encoding="utf-8"
    )

    print("===================================")
    print("STREAM TROVATO!")
    print("Playlist youtube.m3u8 aggiornata.")
    print("===================================")

finally:
    cookie_file.unlink(missing_ok=True)