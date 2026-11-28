import sys
from mlx_lm import load, generate

model, tokenizer = load("qwen3.5-4b")
text = open(sys.argv[1]).read()

messages = [{"role": "user", "content": "Summarise this in five short bullet points:\n\n" + text}]
prompt = tokenizer.apply_chat_template(
    messages, add_generation_prompt=True, enable_thinking=False)
generate(model, tokenizer, prompt, max_tokens=500, verbose=True)
