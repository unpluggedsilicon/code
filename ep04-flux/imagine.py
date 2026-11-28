import subprocess, sys, time
from mflux.models.common.config import ModelConfig
from mflux.models.flux2.variants import Flux2Klein

model = Flux2Klein(model_path="klein-4b-q4", model_config=ModelConfig.flux2_klein_4b())
size = int(sys.argv[1]) if len(sys.argv) > 1 else 512
seed = 1

while True:
    prompt = input("\ndescribe an image: ")
    start = time.time()
    image = model.generate_image(prompt=prompt, seed=seed, width=size, height=size)
    name = f"image_{seed}.png"
    image.save(name)
    print(f"🖼  saved {name} in {time.time() - start:.0f} seconds")
    subprocess.run(["open", name])
    seed += 1
