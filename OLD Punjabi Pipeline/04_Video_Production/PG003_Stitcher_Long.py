import os
import subprocess

# --- CONFIGURATION ---
PROJECT_ID = "PG003"
AUDIO_PATH = r"f:\Punjabi_Guftar_Workspace\04_Audio_Recording_Studio\01_Raw_VO\PG003_Full_VO.mp3.m4a"
INTRO_VIDEO = r"f:\Punjabi_Guftar_Workspace\03_Visual_Laboratory\04_Typography_Cards\PG-003\ਮਰ ਰਹੀ ਹੈ ਮੇਰੀ ਭਾਸ਼ਾ-ਵਿਸ਼ਲੇਸ਼ਣ.mp4"
CARDS_DIR = r"f:\Punjabi_Guftar_Workspace\03_Visual_Laboratory\04_Typography_Cards\PG-003"
OUTPUT_DIR = r"f:\Punjabi_Guftar_Workspace\04_Video_Production\Drafts"

def get_audio_duration(path):
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", path]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
    return float(result.stdout.strip())

slots = [
    ("M1_S1", "PG003_M1_S1.png"), ("M1_S2", "PG003_M1_S2.png"), ("M1_S3", "PG003_M1_S3.png"), ("M1_S4", "1.png"),
    ("M2_S1", "PG003_M2_S1.png"), ("M2_S2", "PG003_M2_S2.png"), ("M2_S3", "2.png"), ("M2_S4", "3.png"),
    ("M3_S1", "4 (2).png"), ("M3_S2", "5 (2).png"), ("M3_S3", "PG003_M3_S3.png"), ("M3_S4", "PG003_M3_S4.png"),
    ("M4_S1", "6 (2).png"), ("M4_S2", "7.png"), ("M4_S3", "9 (2).png"), ("M4_S4", "10.png"),
    ("M5_S1", "13.png"), ("M5_S2", "14.png"), ("M5_S3", "PG003_M5_S3.png"), ("M5_S4", "2 (2).png"),
    ("M6_S1", "PG003_M6_S1.png"), ("M6_S2", "PG003_M6_S2.png"), ("M6_S3", "3 (2).png")
]

def assemble_long_video():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    duration = get_audio_duration(AUDIO_PATH)
    intro_dur = 56.0
    remaining_dur = duration - intro_dur
    step = remaining_dur / 23
    
    # Input 0: Black Base
    cmd = ["ffmpeg", "-y", "-f", "lavfi", "-i", f"color=c=black:s=1920x1080:d={duration}"]
    
    # Inputs 1-23: Images
    for _, img in slots:
        cmd.extend(["-i", os.path.join(CARDS_DIR, img)])
    
    # Input 24: Audio
    cmd.extend(["-i", AUDIO_PATH])
    
    # Input 25: Intro Video
    cmd.extend(["-i", INTRO_VIDEO])
    
    filter_parts = []
    
    # Process Intro Video (Index 25)
    filter_parts.append(f"[25:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2[intro_v];")
    filter_parts.append(f"[0:v][intro_v]overlay=enable='between(t,0,{intro_dur})'[v_after_intro];")
    
    last_v = "v_after_intro"
    
    # Process Images (Index 1-23)
    for i in range(23):
        start = intro_dur + (i * step)
        end = intro_dur + ((i + 1) * step) if i < 22 else duration
        
        filter_parts.append(f"[{i+1}:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2[img{i}];")
        out_v = f"v{i}"
        filter_parts.append(f"[{last_v}][img{i}]overlay=enable='between(t,{start:.2f},{end:.2f})'[{out_v}];")
        last_v = out_v

    # Calibration Text Overlay
    font_path = "C\\:/Windows/Fonts/raavi.ttf"
    filter_parts.append(f"[{last_v}]drawtext=fontfile='{font_path}':text='%{{pts\\:hms}}':x=100:y=100:fontsize=80:fontcolor=yellow:box=1:boxcolor=black@0.6[final_v]")
    
    cmd.extend([
        "-filter_complex", "".join(filter_parts),
        "-map", "[final_v]", "-map", "24:a",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
        "-c:a", "aac", "-b:a", "192k",
        os.path.join(OUTPUT_DIR, "PG003_Master_Calibration_V2.mp4")
    ])
    
    print(f"Starting assembly of 19-minute master video with Intro...")
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    assemble_long_video()
