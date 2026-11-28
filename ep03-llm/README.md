# Free AI chat on your Mac, fully offline (Qwen3.5-4B + MLX)

Video: **Run a Free AI Chatbot on Your Mac, Fully Offline: Qwen3.5 Tutorial** · deep dive: **How an LLM Actually Works**

Needs an Apple silicon Mac (M1 or newer), [Homebrew](https://brew.sh) and about 4 GB of free space.

## Setup

```bash
brew install uv                              # only if `uv --version` fails
mkdir llm && cd llm
uv venv -p 3.13
source .venv/bin/activate
uv pip install -r requirements.txt           # or: uv pip install mlx-lm
hf download mlx-community/Qwen3.5-4B-MLX-4bit --local-dir qwen3.5-4b
```

The download (about 3 GB) is the only step that needs the internet. Put the scripts in the same folder as `qwen3.5-4b`.

First answer, no script needed:

```bash
mlx_lm.generate --model qwen3.5-4b --chat-template-config '{"enable_thinking":false}' --prompt 'Why is the sky blue?'
```

## Scripts

| File | What it does | Run |
|---|---|---|
| [chat.py](chat.py) | streaming chat in the terminal that remembers the conversation | `python chat.py` |
| [summarize.py](summarize.py) | five-bullet summary of any text file, then speed stats | `python summarize.py alice_ch1.txt` |
| [think.py](think.py) | one question with thinking `on` or `off`, prints the time | `python think.py on 'How many times does the letter r appear in strawberry? Answer with just a number.'` |

Local OpenAI-style server (any app that lets you change the OpenAI base URL can use it):

```bash
mlx_lm.server --model qwen3.5-4b --chat-template-args '{"enable_thinking":false}' &
curl -s localhost:8080/v1/chat/completions \
  -d '{"messages":[{"role":"user","content":"Say good morning in French, Spanish and Japanese."}]}' \
  | jq -r '.choices[0].message.content'
```

## Measured on an M4 MacBook (16 GB), offline

Median of 3 runs, fresh process each, thinking off, mlx-lm 0.32.2.

| Job | Prompt | Reading | Writing | Peak memory |
|---|---|---|---|---|
| "Why is the sky blue?" | 23 tokens | 91 tokens/s | 35 tokens/s | 2.55 GB |
| Alice in Wonderland ch. 1 (2,186 words) → summary | 2,955 tokens | 359 tokens/s (≈ 8.4 s) | 34 tokens/s | 3.91 GB |

Model: 2.9 GB on disk; loading takes about 2.7 s.
Strawberry test: thinking off answered "2" in 0.5 s (3 of 3 runs); thinking on answered "3" in 10–13 s (2 of 2).

Qwen3.5 thinks by default. The scripts pass `enable_thinking=False` unless you ask for thinking.

## If something goes wrong

- It tries to download, or "repository not found" → run from the folder that contains `qwen3.5-4b`.
- Slow, or the Mac starts swapping → close big apps; a long document needs more memory (3.9 GB for a 3,000-token chapter).
- It can sound sure and still be wrong (the Alice summary once said she was back to normal size; she is still ten inches tall). Check facts that matter.
