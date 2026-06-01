import subprocess
import re
import sys
import os

def detect_silence(file_path, noise="-30dB", duration="0.5"):
    """
    Runs FFmpeg silencedetect filter and parses timestamps of silent ranges.
    Returns: A list of (silence_start, silence_end) strings/floats.
    """
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        return []
        
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
    if len(sys.argv) < 2:
        print("Usage: py analyze_audio.py <audio_file_path> [noise_threshold] [duration]")
        sys.exit(1)
        
    path = sys.argv[1]
    noise = sys.argv[2] if len(sys.argv) > 2 else "-30dB"
    dur = sys.argv[3] if len(sys.argv) > 3 else "0.5"
    
    print(f"Analyzing {path} for silence (threshold={noise}, duration={dur}s)...")
    silences = detect_silence(path, noise, dur)
    for start, end in silences:
        print(f"Silence detected: {start}s to {end}s")
