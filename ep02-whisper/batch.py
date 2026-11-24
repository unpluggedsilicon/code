# Transcribe every mp3 in a folder called "recordings" and save a .txt next to each one.
# Usage: python batch.py
from pathlib import Path
import mlx_whisper

for f in sorted(Path("recordings").glob("*.mp3")):
    result = mlx_whisper.transcribe(str(f), path_or_hf_repo="whisper-turbo")
    f.with_suffix(".txt").write_text(result["text"].strip())
    print("✓", f.name)
