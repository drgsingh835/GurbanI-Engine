import os
import subprocess

WORKSPACE_DIR = r"F:\Punjabi_Guftar_Workspace"
IMAGES_DIR = os.path.join(WORKSPACE_DIR, "03_Visual_Laboratory", "03_Background_Media")
OUTPUT_DIR = os.path.join(WORKSPACE_DIR, "05_Video_Production_Plant", "03_Rough_Cuts")

# The exact visual sequence based on our Script's Visual Prompts
images = [
    "seq_01_intro.png",
    "seq_02_tongue.png",
    "seq_03_throat.png",
    "seq_04_lips.png",
    "seq_05_book.png"
]

def assemble():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    print("Starting Multi-Sequence FFmpeg Rough Cut...")
    
    # Create a list file for FFmpeg to stitch the sequence together
    list_file = os.path.join(IMAGES_DIR, "concat_list.txt")
    with open(list_file, "w", encoding="utf-8") as f:
        for img in images:
            img_path = os.path.join(IMAGES_DIR, img).replace("\\", "/")
            f.write(f"file '{img_path}'\n")
            f.write("duration 5\n") # Each image stays on screen for 5 seconds
        
        # FFmpeg requires the last file to be specified again without duration for the concat demuxer
        last_img_path = os.path.join(IMAGES_DIR, images[-1]).replace("\\", "/")
        f.write(f"file '{last_img_path}'\n")

    output_video = os.path.join(OUTPUT_DIR, "rough_cut_full.mp4")
    
    cmd = [
        r"F:\Software\FFmpeg\bin\ffmpeg.exe", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", list_file,
        "-vf", "scale=1920:1080", # Ensure all are 1080p
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        output_video
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print(f"\nRough Cut Assembly Complete! Saved to: {output_video}")
    except FileNotFoundError:
        print("\nError: FFmpeg is not in the system PATH.")

if __name__ == "__main__":
    assemble()
