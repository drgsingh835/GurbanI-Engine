import subprocess
import os

AUDIO_PATH = r"f:\Punjabi_Guftar_Workspace\04_Audio_Recording_Studio\01_Raw_VO\PG003_Full_VO.mp3.m4a"
OUTPUT_DIR = r"f:\Punjabi_Guftar_Workspace\03_Audio_Laboratory\01_Raw_VO\PG003_Movements"

# Timestamps in (start, end) seconds
movements = [
    (0, 180),      # M1: 0-3:00
    (180, 360),    # M2: 3:00-6:00
    (360, 540),    # M3: 6:00-9:00
    (540, 720),    # M4: 9:00-12:00
    (720, 960),    # M5: 12:00-16:00
    (960, None)    # M6: 16:00-end
]

def split_audio():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    for i, (start, end) in enumerate(movements):
        output_file = os.path.join(OUTPUT_DIR, f"PG003_M{i+1}_VO.mp3")
        cmd = ["ffmpeg", "-y", "-i", AUDIO_PATH, "-ss", str(start)]
        if end:
            duration = end - start
            cmd.extend(["-t", str(duration)])
        
        cmd.extend(["-c:a", "libmp3lame", "-q:a", "2", output_file])
        
        print(f"Splitting Movement {i+1}...")
        subprocess.run(cmd, check=True)

if __name__ == "__main__":
    split_audio()
