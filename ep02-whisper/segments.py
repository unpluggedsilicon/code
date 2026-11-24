# Print every segment with its start time, so you can jump to any line in the recording.
# Usage: python segments.py jfk.flac
import sys
import mlx_whisper

result = mlx_whisper.transcribe(sys.argv[1], path_or_hf_repo="whisper-turbo")

for seg in result["segments"]:
    print(f'{seg["start"]:7.1f}s  {seg["text"].strip()}')
