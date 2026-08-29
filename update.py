import subprocess
from pathlib import Path

URL = "https://www.youtube.com/watch?v=wHJHpOP7vjM"

clients = [
    "web_embedded",
    "android_vr",
    "web_safari",
]

for client in clients:
    print(f"\n=== Provo client: {client} ===")

    result = subprocess.run(
        [
            "yt-dlp",
            "--no-warnings",
            "--extractor-args",
            f"youtube:player_client={client}",
            "--get-url",
            "-f",
            "best[protocol*=m3u8]/best",
            URL,
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode == 0 and result.stdout.strip():
        stream_url = result.stdout.strip().splitlines()[-1]

        playlist = f"""#EXTM3U
#EXTINF:-1,Diretta YouTube
{stream_url}
"""

        Path("youtube.m3u8").write_text(
            playlist,
            encoding="utf-8"
        )

        print(f"OK! Client funzionante: {client}")
        print("M3U8 aggiornata.")
        break

    print("Fallito:")
    print(result.stderr[:2000])

else:
    raise SystemExit(
        "Nessun client YouTube è riuscito ad ottenere lo stream."
    )