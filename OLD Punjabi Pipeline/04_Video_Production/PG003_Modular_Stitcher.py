import os
import subprocess

# --- CONFIGURATION ---
PROJECT_ID = "PG003"
AUDIO_DIR = r"f:\Punjabi_Guftar_Workspace\03_Audio_Laboratory\01_Raw_VO\PG003_Movements"
INTRO_VIDEO = r"f:\Punjabi_Guftar_Workspace\03_Visual_Laboratory\04_Typography_Cards\PG-003\ਮਰ ਰਹੀ ਹੈ ਮੇਰੀ ਭਾਸ਼ਾ-ਵਿਸ਼ਲੇਸ਼ਣ.mp4"
CARDS_DIR = r"f:\Punjabi_Guftar_Workspace\03_Visual_Laboratory\04_Typography_Cards\PG-003"
OUTPUT_DIR = r"f:\Punjabi_Guftar_Workspace\04_Video_Production\Drafts\Movements"
FONT_PATH = "C\\:/Windows/Fonts/raavi.ttf"

# Mapping: (Movement_Name, Audio_File, Image_List, Intro_Duration_If_Any)
movements_config = [
    ("M1", "PG003_M1_VO.mp3", ["PG003_M1_S1.png", "PG003_M1_S2.png", "PG003_M1_S3.png", "1.png"], 25.0),
    ("M2", "PG003_M2_VO.mp3", ["PG003_M2_S1.png", "PG003_M2_S2.png", "2.png", "3.png"], 0),
    ("M3", "PG003_M3_VO.mp3", ["4 (2).png", "5 (2).png", "PG003_M3_S3.png", "PG003_M3_S4.png"], 0),
    ("M4", "PG003_M4_VO.mp3", ["6 (2).png", "7.png", "9 (2).png", "10.png"], 0),
    ("M5", "PG003_M5_VO.mp3", ["13.png", "14.png", "PG003_M5_S3.png", "2 (2).png"], 0),
    ("M6", "PG003_M6_VO.mp3", ["PG003_M6_S1.png", "PG003_M6_S2.png", "3 (2).png"], 0)
]

def get_duration(path):
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", path]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
    return float(result.stdout.strip())

def render_movement(name, audio_file, images, intro_dur):
    audio_path = os.path.join(AUDIO_DIR, audio_file)
    total_dur = get_duration(audio_path)
    output_path = os.path.join(OUTPUT_DIR, f"{PROJECT_ID}_{name}_Draft.mp4")
    
    # Base black color
    cmd = ["ffmpeg", "-y", "-f", "lavfi", "-i", f"color=c=black:s=1920x1080:d={total_dur}"]
    
    # Image inputs
    for img in images:
        cmd.extend(["-i", os.path.join(CARDS_DIR, img)])
    
    # Audio input
    cmd.extend(["-i", audio_path])
    
    input_idx = 1
    filter_parts = []
    
    # Intro Video handling for M1
    if intro_dur > 0:
        cmd.extend(["-i", INTRO_VIDEO])
        intro_idx = len(images) + 2 # 0:bg, 1..N:imgs, N+1:audio, N+2:intro
        filter_parts.append(f"[{intro_idx}:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2[intro_v];")
        filter_parts.append(f"[0:v][intro_v]overlay=enable='between(t,0,{intro_dur})'[v_after_intro];")
        last_v = "v_after_intro"
        start_offset = intro_dur
    else:
        last_v = "0:v"
        start_offset = 0
        
    # Images overlay
    rem_dur = total_dur - start_offset
    step = rem_dur / len(images)
    
    for i in range(len(images)):
        start = start_offset + (i * step)
        end = start_offset + ((i + 1) * step) if i < len(images) - 1 else total_dur
        filter_parts.append(f"[{i+1}:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2[img{i}];")
        out_v = f"v{name}_{i}"
        filter_parts.append(f"[{last_v}][img{i}]overlay=enable='between(t,{start:.2f},{end:.2f})'[{out_v}];")
        last_v = out_v

    # Calibration Text
    filter_parts.append(f"[{last_v}]drawtext=fontfile='{FONT_PATH}':text='%{{pts\\:hms}}':x=100:y=100:fontsize=80:fontcolor=yellow:box=1:boxcolor=black@0.6[final_v]")
    
    audio_idx = len(images) + 1
    cmd.extend([
        "-filter_complex", "".join(filter_parts),
        "-map", "[final_v]", "-map", f"{audio_idx}:a",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
        "-c:a", "aac", "-b:a", "192k",
        output_path
    ])
    
    print(f"Rendering {name}...")
    subprocess.run(cmd, check=True)
    return output_path

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    draft_files = []
    for config in movements_config:
        path = render_movement(*config)
        draft_files.append(path)
        
    # Final Concatenation
    concat_list = os.path.join(OUTPUT_DIR, "concat.txt")
    with open(concat_list, "w") as f:
        for df in draft_files:
            f.write(f"file '{os.path.basename(df)}'\n")
            
    final_output = os.path.join(os.path.dirname(OUTPUT_DIR), "PG003_Master_Modular_Draft.mp4")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list,
        "-c", "copy", final_output
    ], check=True)
    print(f"\nModular Master Draft generated: {final_output}")

if __name__ == "__main__":
    main()
