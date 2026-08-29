import os
import subprocess
from pathlib import Path

URL = "https://www.youtube.com/watch?v=wHJHpOP7vjM"
OUTPUT = Path("trm.m3u8")

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
        timeout=120,
    )

    if result.returncode != 0:
        print(result.stderr)
        raise SystemExit("YouTube non ha restituito uno stream")

    urls = [
        line.strip()
        for line in result.stdout.splitlines()
        if line.strip().startswith("http")
    ]

    if not urls:
        raise SystemExit("Nessun URL dello stream trovato")

    stream_url = urls[-1]

    playlist = (
        "#EXTM3U\n"
        "#EXTINF:-1, Diretta YouTube\n"
        f"{stream_url}\n"
    )

    # Scrive il file SOLO dopo aver ottenuto un URL valido.
    OUTPUT.write_text(playlist, encoding="utf-8")

    print("Stream trovato e playlist aggiornata.")

finally:
    cookie_file.unlink(missing_ok=True)