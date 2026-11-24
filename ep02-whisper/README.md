# Free speech-to-text on your Mac, fully offline (Whisper)

Video: **Free Speech-to-Text on Your Mac, Fully Offline: Whisper Tutorial** · deep dive: **How Whisper Actually Works**

Needs an Apple silicon Mac (M1 or newer), [Homebrew](https://brew.sh) and about 3 GB of free space.

## Setup

```bash
brew install uv ffmpeg
mkdir whisper && cd whisper
uv venv -p 3.13
source .venv/bin/activate
uv pip install -r requirements.txt          # or: uv pip install mlx-whisper
hf download mlx-community/whisper-large-v3-turbo --local-dir whisper-turbo
```

The download (1.6 GB) is the only step that needs the internet. Put the scripts in the same folder as `whisper-turbo`.

## Scripts

| File | What it does | Run |
|---|---|---|
| [transcribe.py](transcribe.py) | audio or video file → `.txt` next to it, prints language and speed | `python transcribe.py jfk.flac` |
| [prompt.py](prompt.py) | same, with an initial prompt that brings back capitals and full stops on long recordings | `python prompt.py chapter.mp3` |
| [segments.py](segments.py) | prints every line with its start time | `python segments.py jfk.flac` |
| [batch.py](batch.py) | transcribes every mp3 in `recordings/` | `python batch.py` |

Subtitles need no script:

```bash
mlx_whisper jfk.flac --model whisper-turbo -f srt --verbose False
```

## Measured on an M4 MacBook (16 GB), offline

| Audio | Length | Time (median of 3) |
|---|---|---|
| Kennedy inaugural clip | 11 s | 2.0 s |
| Alice in Wonderland, ch. 1 (LibriVox) | 14 min 24 s | 54.4 s (≈16× real time) |
| Don Quixote, ch. 1 (LibriVox, Spanish, auto-detected) | 14 min 38 s | 68.2 s (≈13× real time) |

Model: 1.6 GB on disk, about 2.6 GB memory at peak. Tested with mlx-whisper 0.4.3.

Turbo transcribes many languages but does not translate them into English (OpenAI says it wasn't trained for
translation; `--task translate` returned the original Spanish here).

## If something goes wrong

- `ffmpeg` missing → `brew install ffmpeg`; Whisper needs it to open mp3, m4a and video files.
- "repository not found" / it tries to download → run from the folder that contains `whisper-turbo`.
- Using a prompt? Check the first lines: Whisper can leave out a short spoken intro.
