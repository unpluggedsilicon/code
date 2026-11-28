# Free AI image generator on your Mac, fully offline (FLUX.2 Klein 4B + mflux)

Video: **Run FLUX Locally: Free, Offline AI Image Generator on Your Own Computer (FLUX.2 Klein Tutorial)** · deep dive: **How AI Image Generators Actually Work**

Needs an Apple silicon Mac (M1 or newer), [Homebrew](https://brew.sh) and about 20 GB of free space during setup (4.6 GB after).

## Setup

```bash
brew install uv                              # only if `uv --version` fails
mkdir flux && cd flux
uv venv -p 3.13
source .venv/bin/activate
uv pip install -r requirements.txt           # or: uv pip install mflux
hf download black-forest-labs/FLUX.2-klein-4B --exclude "flux-2-klein-4b.safetensors" --exclude "*.jpg" --local-dir klein-4b
mflux-save --model ./klein-4b --base-model flux2-klein-4b --quantize 4 --path klein-4b-q4
```

The download (about 16 GB; the excluded file is a 7.75 GB duplicate of `transformer/`) is the only step that needs the
internet. `mflux-save` writes a 4-bit copy (4.6 GB, about 25 s). Always load that copy: on a 16 GB Mac the full model
swaps and one small picture took about ten times as long. After that you can delete `klein-4b` to get 16 GB back.

`--exclude` takes one pattern per flag: `--exclude a "*.jpg"` fails with "File not found in repository".

First picture, no script needed:

```bash
mflux-generate-flux2 --model ./klein-4b-q4 --base-model flux2-klein-4b --steps 4 --width 512 --height 512 \
  --seed 1 --prompt 'A red fox sitting in fresh snow at the edge of a pine forest, soft morning light, photograph' --output fox.png
```

## Scripts and commands

| What | Run |
|---|---|
| [imagine.py](imagine.py): type a description, get a PNG (opens in Preview); optional size | `python imagine.py` or `python imagine.py 1024` |
| Four seeds of one prompt | `mflux-generate-flux2 … --seed 1 2 3 4 --prompt '…'` |
| Edit a picture by describing the change | `mflux-generate-flux2-edit --model ./klein-4b-q4 --base-model flux2-klein-4b --steps 4 --seed 1 --image-paths fox.png --prompt '…' --output fox_autumn.png` |
| Wide or tall (multiples of 16) | `mflux-generate-flux2 … --width 1024 --height 576 --prompt '…'` |

Same prompt + same seed + same settings = the same picture.

## Measured on an M4 MacBook (16 GB), offline

Measured on an idle machine (2026-11-27). Sizes in GB = 10⁹ bytes, as Finder shows them. Median of 3 runs, fresh process each, 4 steps, seed 1, mflux 0.24.0.

| Model folder | On disk | 512 × 512 | 1024 × 1024 | Peak memory (512 / 1024) |
|---|---|---|---|---|
| 4-bit (`klein-4b-q4`) | 4.6 GB | 17.6 s | 59.5 s | 4.77 / 5.39 GB |
| 8-bit | 8.6 GB | 22.7 s | 77.6 s | 8.20 / 8.88 GB |

Peak memory above is from the Python API (everything stays loaded, as in imagine.py). The `mflux-generate-flux2`
command frees the text encoder before drawing and reports about 3.0 GB at 512 × 512.

Edit (one reference picture, 512 × 512): about 30 s. Wide 1024 × 576: about 31 s.

## If something goes wrong

- Very slow, the Mac swaps → you loaded `klein-4b` (16-bit, about 16 GB). Load `klein-4b-q4`.
- It tries to download → run from the folder that contains `klein-4b-q4`.
- Text in pictures: short words usually come out right; long sentences get misspelled.
