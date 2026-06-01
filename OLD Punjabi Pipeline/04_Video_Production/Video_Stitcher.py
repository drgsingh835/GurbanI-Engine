import os
import subprocess
import json

# --- CONFIGURATION ---
CALIBRATION_MODE = True  # Set to True to burn timestamps into the video for easy sync editing
SYNC_OFFSET = 0.0        # Global offset (seconds)
SYNC_SHEET_PATH = r"f:\Punjabi_Guftar_Workspace\04_Video_Production\sync_sheet.json"

def create_movement_video(image_duration_list, audio_path, output_path):
    """
    Stitches images into a video and adds audio.
    image_duration_list: list of (image_path, duration)
    """
    concat_file = f"temp_concat_{os.path.basename(output_path)}.txt"
    with open(concat_file, "w") as f:
        for img, duration in image_duration_list:
            f.write(f"file '{img}'\n")
            f.write(f"duration {max(0.01, float(duration))}\n")
        # Final file entry (no duration) for the concat filter to know where to stop
        f.write(f"file '{image_duration_list[-1][0]}'\n")

    # FFmpeg Filters
    video_filters = []
    
    # Calibration Overlay: Burns the current timestamp (00:00:00.000)
    if CALIBRATION_MODE:
        # Using a more robust font path for Windows FFmpeg
        font_path = "C\\:/Windows/Fonts/raavi.ttf"
        video_filters.append(f"drawtext=fontfile='{font_path}':text='%{{pts\\:hms}}':x=100:y=100:fontsize=100:fontcolor=yellow:box=1:boxcolor=black@0.8")

    filter_str = ",".join(video_filters) if video_filters else ""

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", concat_file,
        "-i", audio_path,
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30"
    ]
    
    if filter_str:
        cmd.extend(["-vf", filter_str])
        
    cmd.extend([
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        output_path
    ])
    
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)
    os.remove(concat_file)

def get_audio_duration(path):
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", path]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
    return float(result.stdout.strip())

def load_sync_sheet(path):
    with open(path, "r") as f:
        return json.load(f)

if __name__ == "__main__":
    cards_dir = r"f:\Punjabi_Guftar_Workspace\03_Visual_Laboratory\04_Typography_Cards"
    audio_dir = r"f:\Punjabi_Guftar_Workspace\03_Audio_Laboratory\01_Raw_VO"
    output_dir = r"f:\Punjabi_Guftar_Workspace\04_Video_Production\Drafts"
    os.makedirs(output_dir, exist_ok=True)

    try:
        sync_data = load_sync_sheet(SYNC_SHEET_PATH)
    except Exception as e:
        print(f"Error loading sync sheet: {e}")
        exit(1)

    movements = ["M1", "M2", "M3"]
    draft_files = []

    for mv in movements:
        if mv in sync_data:
            print(f"\n--- Processing {mv} ---")
            audio_file = os.path.join(audio_dir, f"PG002_{mv}_VO.mp3")
            audio_end = get_audio_duration(audio_file)
            
            # Convert start_times to durations
            items = sync_data[mv]
            img_list = []
            for i in range(len(items)):
                img_path = os.path.join(cards_dir, items[i]["image"])
                
                # If "start_time" exists, calculate duration from the next entry
                if "start_time" in items[i]:
                    start = float(items[i]["start_time"])
                    if i + 1 < len(items) and "start_time" in items[i+1]:
                        next_start = float(items[i+1]["start_time"])
                    else:
                        next_start = audio_end
                    duration = next_start - start
                # Backward compatibility for "duration"
                elif "duration" in items[i]:
                    duration = items[i]["duration"]
                else:
                    duration = 1.0 # Fallback
                
                img_list.append((img_path, duration))
            
            output_file = os.path.join(output_dir, f"{mv}_Draft.mp4")
            create_movement_video(img_list, audio_file, output_file)
            draft_files.append(output_file)

    # --- Final Concatenation ---
    final_output = os.path.join(output_dir, "PG002_Master_Calibration.mp4" if CALIBRATION_MODE else "PG002_Master_Final.mp4")
    concat_list = os.path.join(output_dir, "concat.txt")
    with open(concat_list, "w") as f:
        for df in draft_files:
            f.write(f"file '{os.path.basename(df)}'\n")
    
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list,
        "-c", "copy", final_output
    ], check=True)
    
    print(f"\nMaster Video generated: {final_output}")
    if CALIBRATION_MODE:
        print("NOTE: Calibration Mode is ON. Watch the video and use the on-screen clock to adjust sync_sheet.json.")
