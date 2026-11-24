# transcribe.py with an initial prompt: on long recordings this brings back capitals and full stops.
# Usage: python prompt.py alice_ch1.mp3
import sys
import mlx_whisper

audio = sys.argv[1]
result = mlx_whisper.transcribe(audio, path_or_hf_repo="whisper-turbo",
    initial_prompt="Hello, and welcome. This is a chapter of a book, read aloud.")

text = result["text"].strip()
open(audio.rsplit(".", 1)[0] + ".txt", "w").write(text)
print(text)
