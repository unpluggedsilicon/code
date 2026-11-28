from mlx_lm import load, stream_generate
from mlx_lm.sample_utils import make_sampler

model, tokenizer = load("qwen3.5-4b")
sampler = make_sampler(temp=0.7, top_p=0.8, top_k=20)
messages = []

while True:
    messages.append({"role": "user", "content": input("\nyou: ")})
    prompt = tokenizer.apply_chat_template(
        messages, add_generation_prompt=True, enable_thinking=False)

    print("qwen: ", end="", flush=True)
    answer = ""
    for chunk in stream_generate(model, tokenizer, prompt, max_tokens=1000, sampler=sampler):
        print(chunk.text, end="", flush=True)
        answer += chunk.text
    messages.append({"role": "assistant", "content": answer})
    print(f"\n⚡ {chunk.generation_tps:.0f} tokens per second")
