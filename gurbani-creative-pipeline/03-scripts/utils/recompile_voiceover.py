import subprocess
import os
import sys
import json

# Reconfigure stdout/stderr to UTF-8
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
scratch_dir = os.path.join(WORKSPACE_DIR, "scratch_blocks")
vo_dir = os.path.join(WORKSPACE_DIR, "04-assets", "voiceover")
output_audio = os.path.join(vo_dir, "gurbani_pa_01_vo_track.mp3")
sidecar_path = os.path.join(vo_dir, "gurbani_pa_01_vo_track_duration.json")

def run_cmd(cmd):
    print(f"[*] Running: {' '.join(cmd)}")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print(f"[-] Error: {res.stderr}")
        return False
    return True

def get_audio_duration(audio_path):
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "json",
        audio_path
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode == 0:
        try:
            probe_data = json.loads(result.stdout)
            return float(probe_data["format"]["duration"])
        except:
            pass
    return None

def main():
    print("====================================================")
    print("  Gurbani Creative Pipeline - Audio Recompiler")
    print("====================================================")
    
    trimmed_files = []
    
    # 1. Trim leading and trailing silences
    for i in range(1, 6):
        inp = os.path.join(scratch_dir, f"block_{i}.mp3")
        out = os.path.join(scratch_dir, f"block_{i}_trimmed.mp3")
        
        if not os.path.exists(inp):
            print(f"[-] Raw block file not found: {inp}")
            sys.exit(1)
            
        filter_str = "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse"
        
        cmd = [
            "ffmpeg", "-y",
            "-i", inp,
            "-af", filter_str,
            "-c:a", "libmp3lame",
            "-q:a", "2",
            out
        ]
        print(f"[*] Trimming silence from Block {i}...")
        if run_cmd(cmd):
            dur = get_audio_duration(out)
            print(f"[+] Trimmed Block {i} duration: {dur:.2f}s")
            trimmed_files.append(out)
        else:
            print(f"[-] Trimming failed for block {i}")
            sys.exit(1)
            
    # 2. Concatenate blocks using complex filtergraph (click-free PCM mix)
    print(f"\n[*] Concatenating {len(trimmed_files)} trimmed blocks...")
    os.makedirs(os.path.dirname(output_audio), exist_ok=True)
    
    concat_cmd = ["ffmpeg", "-y"]
    for f in trimmed_files:
        concat_cmd.extend(["-i", f])
        
    inputs_str = "".join(f"[{idx}:a]" for idx in range(len(trimmed_files)))
    filter_complex_str = f"{inputs_str}concat=n={len(trimmed_files)}:v=0:a=1[a];[a]highpass=f=80,lowpass=f=12000[out_a]"
    
    concat_cmd.extend([
        "-filter_complex", filter_complex_str,
        "-map", "[out_a]",
        "-c:a", "libmp3lame",
        "-q:a", "2",
        output_audio
    ])
    
    if run_cmd(concat_cmd):
        duration = get_audio_duration(output_audio)
        if duration:
            with open(sidecar_path, "w", encoding="utf-8") as df:
                json.dump({"audio_duration_seconds": round(duration, 3)}, df)
            print(f"[+] Voiceover compiled successfully! Path: {output_audio}")
            print(f"[+] Total duration: {duration:.2f}s (sidecar JSON saved)")
        else:
            print("[-] Failed to probe conformed audio duration.")
            sys.exit(1)
    else:
        print("[-] FFmpeg concatenation failed.")
        sys.exit(1)
        
    # Clean up trimmed temporary files
    for f in trimmed_files:
        try:
            os.remove(f)
        except:
            pass
            
    # 3. Render video reel using render_reel.py
    print("\n[*] Compiling final vertical reel using render_reel.py...")
    render_cmd = ["py", os.path.join(WORKSPACE_DIR, "render_reel.py"), "--id", "gurbani_pa_01"]
    if run_cmd(render_cmd):
        print("[+] Video compilation succeeded!")
    else:
        print("[-] Video compilation failed.")
        sys.exit(1)
        
    # 4. Rebuild the HTML dashboard
    print("\n[*] Rebuilding Studio Dashboard...")
    dashboard_cmd = ["py", os.path.join(WORKSPACE_DIR, "05-outputs", "generate_dashboard.py")]
    if run_cmd(dashboard_cmd):
        print("[+] Dashboard rebuilt successfully!")
    else:
        print("[-] Dashboard rebuild failed.")
        sys.exit(1)
        
    print("\n[+] ALL DONE! Clean, artifact-free video is ready at 05-outputs/final_reels/gurbani_pa_01_final_reel.mp4")

if __name__ == "__main__":
    main()
