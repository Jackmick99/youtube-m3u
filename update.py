import subprocess

URL = "https://www.youtube.com/watch?v=wHJHpOP7vjM"

result = subprocess.run(
    [
        "yt-dlp",
        "-v",
        "--no-warnings",
        "--simulate",
        "--skip-download",
        URL,
    ],
    capture_output=True,
    text=True,
)

print("========== STDOUT ==========")
print(result.stdout)

print("========== STDERR ==========")
print(result.stderr)

print("========== EXIT CODE ==========")
print(result.returncode)

if result.returncode != 0:
    raise SystemExit("Test YouTube fallito")