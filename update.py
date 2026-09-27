import os
import subprocess
from pathlib import Path

CHANNELS = [
    {
        "name": "TRM H24",
        "url": "https://www.youtube.com/watch?v=_nd_bpGoMVE",
        "output": "trm.m3u8",
        "pot": False,
    },
    {
        "name": "Sky TG24",
        "url": "https://www.youtube.com/watch?v=DBkiOifHkVE",
        "output": "skytg24.m3u8",
        "pot": True,
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

        command = [
            "yt-dlp",
            "--no-warnings",
            "--cookies", str(cookie_file),
        ]

        # Solo Sky TG24 usa mweb + PO Token provider.
        if channel["pot"]:
            command.extend([
                "--extractor-args",
                "youtube:player_client=mweb",
                "--extractor-args",
                "youtubepot-bgutilscript:server_home=bgutil-ytdlp-pot-provider/server",
            ])

        command.extend([
            "--get-url",
            "-f", "best[protocol*=m3u8]/best",
            channel["url"],
        ])

        result = subprocess.run(
            command,
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
            encoding="utf-8",
        )

        print(f"{channel['name']} aggiornato -> {channel['output']}")

finally:
    cookie_file.unlink(missing_ok=True)
