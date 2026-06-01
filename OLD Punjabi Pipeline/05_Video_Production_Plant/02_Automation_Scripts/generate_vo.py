import os
import re
import asyncio
import edge_tts

# Paths
WORKSPACE_DIR = r"F:\Punjabi_Guftar_Workspace"
SCRIPT_PATH = os.path.join(WORKSPACE_DIR, "01_Scripts_and_Research", "test_03_next.md")
# Punjabi Voice Option (Male: pa-IN-OjasNeural, Female: pa-IN-SalmaNeural)
VOICE = "pa-IN-OjasNeural"
OUTPUT_DIR = os.path.join(WORKSPACE_DIR, "03_Audio_Laboratory", "01_Raw_VO")

def extract_audio_lines(filepath):
    print(f"Reading script: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Extract lines starting with **Audio:** "..."
    pattern = r'\*\*Audio:\*\*\s*"([^"]+)"'
    lines = re.findall(pattern, content)
    with open("vo_debug.log", "w", encoding="utf-8") as log:
        for l in lines:
            log.write(l + "\n")
    return lines

async def generate_tts(text, output_path):
    print("Generating TTS for section...")
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(output_path)
    print(f"Saved: {output_path}")

async def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    lines = extract_audio_lines(SCRIPT_PATH)
    if not lines:
        print("No audio lines found in the script.")
        return
        
    # Generate a single combined VO or multiple chunks
    for i, line in enumerate(lines):
        filename = f"section_{i+1:02d}.mp3"
        output_path = os.path.join(OUTPUT_DIR, filename)
        await generate_tts(line, output_path)
        
    print("\nAll Voiceovers generated successfully!")

if __name__ == "__main__":
    asyncio.run(main())
