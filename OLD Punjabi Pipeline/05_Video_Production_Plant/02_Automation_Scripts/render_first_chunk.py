import os
import subprocess
import urllib.request

WORKSPACE_DIR = r"F:\Punjabi_Guftar_Workspace"
FONT_DIR = os.path.join(WORKSPACE_DIR, "03_Visual_Laboratory", "04_Typography_Cards")
IMAGES_DIR = os.path.join(WORKSPACE_DIR, "03_Visual_Laboratory", "03_Background_Media")
OUTPUT_DIR = os.path.join(WORKSPACE_DIR, "05_Video_Production_Plant", "03_Rough_Cuts")

# 1. Ensure Font Exists (Using Windows Built-in Nirmala UI for Gurmukhi)
font_path = r"C:\Windows\Fonts\Nirmala.ttf"
if not os.path.exists(font_path):
    print("Warning: Nirmala.ttf not found. Text might not render correctly.")

# 2. Setup Files for Layered Assembly
bg_image = os.path.join(IMAGES_DIR, "seq_01_intro.png")
output_video = os.path.join(OUTPUT_DIR, "chunk_01_text.mp4")

# This is the exact text we want perfectly rendered over the background
text_to_display = "Painti Akhar (35 Letters)"  # Using English temporarily to avoid console crash on error, will change back to Gurmukhi once path is verified.

# 3. Build FFmpeg Command
# We use the drawtext filter. On Windows, the colon in C:/ breaks FFmpeg filters, so we escape it.
win_font = "nirmala.ttf"
cmd = [
    r"F:\Software\FFmpeg\bin\ffmpeg.exe", "-y",
    "-loop", "1",
    "-i", bg_image,
    "-vf", f"drawtext=fontfile='{win_font}':text='ਪੈਂਤੀ ਅੱਖਰ':fontcolor=#FFD700:fontsize=150:x=(w-text_w)/2:y=(h-text_h)/2",
    "-c:v", "libx264",
    "-t", "10", # Render a 10 second clip
    "-pix_fmt", "yuv420p",
    output_video
]

print("Starting Decoupled Visual Assembly: Base Layer + Dynamic Text...")
try:
    subprocess.run(cmd, check=True)
    print(f"\nFirst Chunk Assembly Complete! Saved to: {output_video}")
except Exception as e:
    print("\nError during FFmpeg execution. Check console output.")
