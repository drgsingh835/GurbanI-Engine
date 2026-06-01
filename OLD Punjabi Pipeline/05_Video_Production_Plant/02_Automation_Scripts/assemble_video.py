import os
import subprocess

WORKSPACE_DIR = r"F:\Punjabi_Guftar_Workspace"
IMAGES_DIR = os.path.join(WORKSPACE_DIR, "03_Visual_Laboratory", "03_Background_Media")
OUTPUT_DIR = os.path.join(WORKSPACE_DIR, "05_Video_Production_Plant", "03_Rough_Cuts")

# We will use the first cinematic image we generated
image_path = os.path.join(IMAGES_DIR, "01_parchment_calligraphy.png")

def assemble():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    print("🎬 Starting FFmpeg Visual Assembly (Ken Burns Effect)...")
    
    output_video = os.path.join(OUTPUT_DIR, "test_assembly.mp4")
    
    # FFmpeg command to loop a static image for 15 seconds,
    # apply a slow zoom effect (Ken Burns), and export as mp4
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1",
        "-i", image_path,
        "-vf", "zoompan=z='min(zoom+0.001,1.5)':d=450:s=1920x1080",
        "-c:v", "libx264",
        "-t", "15",
        "-pix_fmt", "yuv420p",
        output_video
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print(f"\nVideo Assembly Complete! Saved to: {output_video}")
    except FileNotFoundError:
        print("\n❌ Error: FFmpeg is not in the system PATH. Please ensure Step 2 was completed.")

if __name__ == "__main__":
    assemble()
