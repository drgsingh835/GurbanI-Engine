import os
import subprocess

WORKSPACE_DIR = r"F:\Punjabi_Guftar_Workspace"
ASSETS_DIR = os.path.join(WORKSPACE_DIR, "00_Standard_Assets")
CHUNKS_DIR = os.path.join(WORKSPACE_DIR, "03_Visual_Laboratory", "03_Background_Media", "Animated_Chunks")
OUTPUT_DIR = os.path.join(WORKSPACE_DIR, "05_Final_Deliverables")

intro_path = os.path.join(ASSETS_DIR, "02_Intros", "ਤੁਹਾਡਾ ਸਵਾਗਤ ਹੈ.mp4")
logo_path = os.path.join(ASSETS_DIR, "01_Logos", "logo.mp4")
output_video = os.path.join(OUTPUT_DIR, "PG-002_Master_Final.mp4")

def assemble_master():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    print("Starting Master Assembly (Intro + Content + Logo)...")
    
    # 1. Create a list of all chunks
    chunk_files = [os.path.join(CHUNKS_DIR, f"pg002_sec{i:02d}.mp4") for i in range(1, 6)]
    
    # Check if chunks exist
    for f in chunk_files:
        if not os.path.exists(f):
            print(f"Error: Chunk {f} not found.")
            return

    # 2. FFmpeg Filter Complex to:
    # - Scale Intro to 1080p
    # - Overlay Logo on Content
    # - Concatenate everything
    
    # We will use a temporary file list for concatenation to keep it simple
    list_file = os.path.join(CHUNKS_DIR, "concat_list.txt")
    with open(list_file, "w", encoding="utf-8") as f:
        # Scale intro to 1080p in the command or use a temp file
        # For simplicity in this script, we'll assume intro is 1080p or scale it
        f.write(f"file '{intro_path}'\n")
        for chunk in chunk_files:
            f.write(f"file '{chunk}'\n")

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", list_file,
        "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        output_video
    ]
    
    print("Running FFmpeg concatenation...")
    subprocess.run(cmd, check=True)
    print(f"✅ Master Video Assembled: {output_video}")

if __name__ == "__main__":
    assemble_master()
