import sys, time
import mlx_whisper
from mlx_whisper.audio import load_audio, SAMPLE_RATE

audio = sys.argv[1]
start = time.time()
result = mlx_whisper.transcribe(audio, path_or_hf_repo="whisper-turbo")
took = time.time() - start

text = result["text"].strip()
open(audio.rsplit(".", 1)[0] + ".txt", "w").write(text)
print(text)
print("🌍 language:", result["language"])

secs = len(load_audio(audio)) / SAMPLE_RATE
print(f"📝 {secs:.1f}s of audio in {took:.1f}s  →  {secs/took:.0f}× realtime")
