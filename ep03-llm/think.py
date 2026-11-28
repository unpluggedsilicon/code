import sys, time
from mlx_lm import load, stream_generate
from mlx_lm.sample_utils import make_sampler

model, tokenizer = load("qwen3.5-4b")
think = sys.argv[1] == "on"
question = sys.argv[2]

prompt = tokenizer.apply_chat_template([{"role": "user", "content": question}],
    add_generation_prompt=True, enable_thinking=think)
sampler = make_sampler(temp=1.0 if think else 0.7, top_p=0.95 if think else 0.8, top_k=20)

start = time.time()
for chunk in stream_generate(model, tokenizer, prompt, max_tokens=4000, sampler=sampler):
    print(chunk.text, end="", flush=True)
print(f"\n⏱ {time.time() - start:.1f} seconds")
