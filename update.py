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
            "-v",
            "--no-warnings",
            "--cookies", str(cookie_file),
            "--simulate",
            "--skip-download",
            URL,
        ],
        capture_output=True,
        text=True,
    )

    print(result.stdout)
    print(result.stderr)

    if result.returncode != 0:
        raise SystemExit("Test YouTube fallito")

finally:
    cookie_file.unlink(missing_ok=True)