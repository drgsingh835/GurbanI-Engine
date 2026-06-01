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
    
    chunk_files = [os.path.join(CHUNKS_DIR, f"pg002_sec{i:02d}.mp4") for i in range(1, 6)]
    list_file = os.path.join(CHUNKS_DIR, "concat_list.txt")
    with open(list_file, "w", encoding="utf-8") as f:
        f.write(f"file '{intro_path}'\n")
        for chunk in chunk_files:
            f.write(f"file '{chunk}'\n")

    # Final Command: Concatenate then overlay Circular Logo
    # [1:v] is the logo. We apply a circular mask using a 'geq' filter on the alpha channel.
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", list_file,
        "-stream_loop", "-1", "-i", logo_path,
        "-filter_complex", 
        "[1:v]format=rgba,geq=lum='p(X,Y)':a='if(gt(sqrt(pow(X-W/2,2)+pow(Y-H/2,2)),W/2),0,255)'[mask];" +
        "[1:v][mask]alphamerge,scale=150:150[logo_circle];" +
        "[0:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2[main];" +
        "[main][logo_circle]overlay=W-w-50:H-h-50:shortest=1[out]",
        "-map", "[out]", "-map", "0:a?",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        output_video
    ]
    
    print("Running FFmpeg concatenation and Logo overlay...")
    subprocess.run(cmd, check=True)
    print(f"Master Video Assembled: {output_video}")

if __name__ == "__main__":
    assemble_master()
