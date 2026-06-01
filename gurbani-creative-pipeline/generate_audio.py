import os
import sys

# Reconfigure stdout/stderr to UTF-8 on Windows
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

import torch
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer
import soundfile as sf

# Load HF_TOKEN from .env
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
HF_TOKEN = ""
if os.path.exists(env_path):
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("HF_TOKEN="):
                HF_TOKEN = line.split("=", 1)[1].strip()
                break

print(f"HF_TOKEN loaded: {bool(HF_TOKEN)}")

# 1. Load the model and tokenizer onto the CPU
print("Loading model into memory (this takes a moment and will download weights on first run)...")
model_name = "ai4bharat/indic-parler-tts"
model = ParlerTTSForConditionalGeneration.from_pretrained(model_name, token=HF_TOKEN).to("cpu")
tokenizer = AutoTokenizer.from_pretrained(model_name, token=HF_TOKEN)

# 2. Define your voice style and text
description = "A male speaker with a clear, expressive voice delivers the speech at a moderate pace in a high-quality recording."
transcript = "ਸਤਿਨਾਮ ਵਾਹਿਗੁਰੂ" 

# 3. Tokenize the inputs
input_ids = tokenizer(description, return_tensors="pt").input_ids.to("cpu")
prompt_input_ids = tokenizer(transcript, return_tensors="pt").input_ids.to("cpu")

# 4. Generate the audio
print("Generating audio on CPU (this may take a few minutes)...")
try:
    generation = model.generate(input_ids=input_ids, prompt_input_ids=prompt_input_ids)
    audio_arr = generation.cpu().numpy().squeeze()

    # 5. Save the file
    output_file = "punjabi_audio.wav"
    sf.write(output_file, audio_arr, model.config.sampling_rate)
    print(f"[+] Success! Audio saved to {output_file}")
except Exception as e:
    print(f"[-] Generation error: {e}")
