import os
import subprocess

WORKSPACE_DIR = r"F:\Punjabi_Guftar_Workspace"
AUDIO_DIR = os.path.join(WORKSPACE_DIR, "04_Audio_Recording_Studio", "01_Raw_VO")
IMAGE_DIR = os.path.join(WORKSPACE_DIR, "03_Visual_Laboratory", "03_Background_Media")
OUTPUT_DIR = os.path.join(WORKSPACE_DIR, "05_Video_Production_Plant", "03_Rough_Cuts")
FFMPEG_PATH = r"F:\Software\FFmpeg\bin\ffmpeg.exe"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

sections = [
    ("fc_01_intro.png", "section_01.mp3"),
    ("fc_02_mukh_varg.png", "section_02.mp3"),
    ("fc_03_kavarg.png", "section_03.mp3"),
    ("fc_04_progression.png", "section_04.mp3"),
    ("fc_05_conclusion.png", "section_05.mp3")
]

def assemble_video():
    chunk_files = []
    
    print("--- Starting Final Assembly ---")
    
    for i, (img_name, aud_name) in enumerate(sections):
        img_path = os.path.join(IMAGE_DIR, img_name)
        aud_path = os.path.join(AUDIO_DIR, aud_name)
        chunk_output = os.path.join(OUTPUT_DIR, f"chunk_{i+1:02d}.mp4")
        
        print(f"Processing Chunk {i+1}: {img_name} + {aud_name}")
        
        # FFmpeg command to loop image over audio duration
        cmd = [
            FFMPEG_PATH, "-y",
            "-loop", "1", "-i", img_path,
            "-i", aud_path,
            "-c:v", "libx264", "-tune", "stillimage",
            "-c:a", "aac", "-b:a", "192k",
            "-pix_fmt", "yuv420p",
            "-shortest",
            chunk_output
        ]
        
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        chunk_files.append(chunk_output)
        print(f"Created: {chunk_output}")

    # Create Concat List
    concat_list_path = os.path.join(OUTPUT_DIR, "concat_list.txt")
    with open(concat_list_path, "w") as f:
        for chunk in chunk_files:
            safe_path = chunk.replace('\\', '/')
            f.write(f"file '{safe_path}'\n")

    # Final Concatenation
    final_output = os.path.join(OUTPUT_DIR, "test_02_alphabets_rough_cut.mp4")
    print(f"\nConcatenating all chunks into: {final_output}")
    
    concat_cmd = [
        FFMPEG_PATH, "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_list_path,
        "-c", "copy",
        final_output
    ]
    
    subprocess.run(concat_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("\n--- Assembly Complete! ---")
    print(f"Final Video: {final_output}")

if __name__ == "__main__":
    assemble_video()
