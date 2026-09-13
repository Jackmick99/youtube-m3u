import os
import subprocess
from pathlib import Path

CHANNELS = [
    {
        "name": "TRM H24",
        "url": "https://www.youtube.com/watch?v=_nd_bpGoMVE",
        "output": "trm.m3u8",
    },
    {
        "name": "Sky TG24",
        "url": "https://www.youtube.com/watch?v=DBkiOifHkVE",
        "output": "skytg24.m3u8",
    },
]

cookies = os.environ.get("YOUTUBE_COOKIES")

if not cookies:
    raise SystemExit("Secret YOUTUBE_COOKIES non trovato")

cookie_file = Path("cookies.txt")
cookie_file.write_text(cookies, encoding="utf-8")

try:
    for channel in CHANNELS:
        print(f"--- Aggiornamento {channel['name']} ---")

        result = subprocess.run(
            [
                "yt-dlp",
                "--no-warnings",
                "--cookies", str(cookie_file),
                "--get-url",
                "-f", "best[protocol*=m3u8]/best",
                channel["url"],
            ],
            capture_output=True,
            text=True,
            timeout=120,
        )

        if result.returncode != 0:
            print(result.stderr)
            print(f"ERRORE: {channel['name']} non aggiornato")
            continue

        urls = [
            line.strip()
            for line in result.stdout.splitlines()
            if line.strip().startswith("http")
        ]

        if not urls:
            print(f"ERRORE: nessun URL trovato per {channel['name']}")
            continue

        stream_url = urls[-1]

        playlist = (
            "#EXTM3U\n"
            f"#EXTINF:-1,{channel['name']}\n"
            f"{stream_url}\n"
        )

        Path(channel["output"]).write_text(
            playlist,
            encoding="utf-8"
        )

        print(f"{channel['name']} aggiornato -> {channel['output']}")

finally:
    cookie_file.unlink(missing_ok=True)
