import subprocess
import re

def detect_silence(file_path, noise="-30dB", duration="0.5"):
    cmd = [
        "ffmpeg", "-i", file_path,
        "-af", f"silencedetect=n={noise}:d={duration}",
        "-f", "null", "-"
    ]
    result = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)
    
    silence_starts = re.findall(r"silence_start: ([\d\.]+)", result.stderr)
    silence_ends = re.findall(r"silence_end: ([\d\.]+)", result.stderr)
    
    return list(zip(silence_starts, silence_ends))

if __name__ == "__main__":
    audio_files = [
        r"f:\Punjabi_Guftar_Workspace\03_Audio_Laboratory\01_Raw_VO\PG002_M1_VO.mp3",
        r"f:\Punjabi_Guftar_Workspace\03_Audio_Laboratory\01_Raw_VO\PG002_M2_VO.mp3",
        r"f:\Punjabi_Guftar_Workspace\03_Audio_Laboratory\01_Raw_VO\PG002_M3_VO.mp3"
    ]
    
    for f in audio_files:
        print(f"\nAnalyzing {f}...")
        silences = detect_silence(f)
        for start, end in silences:
            print(f"Silence: {start}s - {end}s")
