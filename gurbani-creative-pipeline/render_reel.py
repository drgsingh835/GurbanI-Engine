import os
import json
import subprocess
import sys
import argparse

# Reconfigure stdout/stderr to UTF-8 on Windows to prevent UnicodeEncodeErrors
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

# Define base paths
WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))

# Import GurmukhiProcessor dynamically
sys.path.append(os.path.join(WORKSPACE_DIR, "03-scripts"))
try:
    from utils.gurmukhi_processor import GurmukhiProcessor
except ImportError:
    class GurmukhiProcessor:
        @staticmethod
        def is_punjabi(t): return False
        @staticmethod
        def to_legacy_ascii(t): return t

def process_text_for_ffmpeg(text):
    """
    Checks if text contains Gurmukhi, normalizes and converts it to legacy ASCII
    if needed, and selects the appropriate font path.
    Returns: (processed_text, font_path_escaped)
    """
    if not text:
        return "", "C\\:/Windows/Fonts/arial.ttf"
        
    is_pa = GurmukhiProcessor.is_punjabi(text)
    if is_pa:
        processed_text = GurmukhiProcessor.to_legacy_ascii(text)
        # Use AmrLipiHeavy font from the copied fonts
        font_file = os.path.normpath(os.path.join(WORKSPACE_DIR, "04-assets", "fonts", "AmrLipiHeavy.ttf"))
    else:
        processed_text = text
        font_file = "C:/Windows/Fonts/arial.ttf"
        
    # Format font path for FFmpeg drawtext (Windows escape)
    font_file = font_file.replace("\\", "/")
    if ":" in font_file:
        drive, rest = font_file.split(":", 1)
        font_path_escaped = f"{drive}\\:{rest}"
    else:
        font_path_escaped = font_file
        
    # Escape colon and other special characters in text for drawtext
    escaped_text = processed_text.replace("\\", "\\\\").replace("'", "'\\\\''").replace(":", "\\:")
    return escaped_text, font_path_escaped

def load_assembly(assembly_path):
    if not os.path.exists(assembly_path):
        print(f"[-] Assembly JSON not found at: {assembly_path}")
        sys.exit(1)
    with open(assembly_path, "r", encoding="utf-8") as f:
        return json.load(f)

def run_cmd(cmd):
    print(f"[*] Running command: {' '.join(cmd)}")
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print(f"[-] Command failed with error:\n{result.stderr}")
        return False
    return True

def compile_shot(shot, item_id, temp_dir, calibrate=False, no_captions=False):
    shot_num = shot["shot_number"]
    shot_type = shot["type"]
    duration = shot["duration"]
    fps = 30
    total_frames = int(duration * fps)
    
    output_clip = os.path.join(temp_dir, f"clip_{shot_num:02d}.mp4")
    print(f"[*] Compiling Shot {shot_num} ({shot_type}) -> {duration}s...")
    
    if shot_type == "AI":
        asset_path = shot["asset_path"]
        if not os.path.exists(asset_path):
            print(f"[-] Image asset not found: {asset_path}")
            return None
            
        # Check if we should apply Ken Burns animation
        anim = shot.get("animation", {})
        zoom_start = anim.get("zoom_start", 1.0)
        zoom_end = anim.get("zoom_end", 1.15)
        
        # Calculate frame-by-frame zoom increment
        zoom_step = (zoom_end - zoom_start) / total_frames if total_frames > 0 else 0.001
        
        # Build FFmpeg command to compile the static image into a zoompan clip
        # 1. Scale image to 2160x3840 (double 1080x1920) to avoid pixelation during zoom
        # 2. Apply zoompan filter
        # 3. Add text overlay (if any)
        # 4. Set pixel format and output H.264
        
        filter_parts = [
            "crop=w='min(iw\\,ih*9/16)':h='min(ih\\,iw*16/9)'",
            "scale=2160x3840",
            f"zoompan=z='{zoom_start:.4f}+on*{zoom_step:.6f}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={total_frames}:s=1080x1920",
            "setsar=1"
        ]
        
        overlay_text = shot.get("overlay_text")
        if overlay_text and not no_captions:
            text_escaped, active_font = process_text_for_ffmpeg(overlay_text)
            # drawtext filter with basic word wrapping or styling
            text_filter = (
                f"drawtext=fontfile='{active_font}':text='{text_escaped}':fontsize=48:fontcolor=white:"
                f"x=(w-text_w)/2:y=h*0.75:box=1:boxcolor=black@0.5:boxborderw=10"
            )
            filter_parts.append(text_filter)
            
        if calibrate:
            cal_font = "C\\:/Windows/Fonts/arial.ttf"
            cal_filter = f"drawtext=fontfile='{cal_font}':text='%{{pts\\:hms}}':x=100:y=100:fontsize=80:fontcolor=yellow:box=1:boxcolor=black@0.8"
            filter_parts.append(cal_filter)
            
        filter_str = ",".join(filter_parts)
        
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1",
            "-i", asset_path,
            "-vf", filter_str,
            "-t", str(duration),
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-r", str(fps),
            output_clip
        ]
        
        if run_cmd(cmd):
            return output_clip
            
    elif shot_type == "TEXT":
        overlay_text = shot.get("overlay_text", "")
        text_escaped, active_font = process_text_for_ffmpeg(overlay_text)
        
        # Create solid color clip with text overlay
        bg_color = shot.get("background_color", "#0B0E14").replace("#", "0x")
        
        text_filter = (
            f"drawtext=fontfile='{active_font}':text='{text_escaped}':fontsize=64:fontcolor=white:"
            f"x=(w-text_w)/2:y=(h-text_h)/2"
        )
        
        border_filter = ""
        border_color = shot.get("border_color")
        if border_color:
            b_color = border_color.replace("#", "0x")
            border_filter = f",drawbox=x=40:y=40:w=iw-80:h=ih-80:color={b_color}:t=3"
            
        filter_str = f"scale=1080x1920{border_filter},{text_filter}"
        
        if calibrate:
            cal_font = "C\\:/Windows/Fonts/arial.ttf"
            filter_str += f",drawtext=fontfile='{cal_font}':text='%{{pts\\:hms}}':x=100:y=100:fontsize=80:fontcolor=yellow:box=1:boxcolor=black@0.8"
            
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi",
            "-i", f"color=c={bg_color}:s=1080x1920:d={duration}",
            "-vf", filter_str,
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-r", str(fps),
            output_clip
        ]
        
        if run_cmd(cmd):
            return output_clip
            
    return None

def main():
    parser = argparse.ArgumentParser(description="Gurbani Video Assembler (FFmpeg)")
    parser.add_argument("--id", "-i", default="gurbani_01", help="Unique ID of the shabad/concept (default: gurbani_01)")
    parser.add_argument("--calibrate", action="store_true", help="Burn timestamps into the video for sync QA")
    parser.add_argument("--no-watermark", action="store_true", help="Disable brand logo circular watermark overlay")
    parser.add_argument("--intro", default=os.path.join(WORKSPACE_DIR, "04-assets", "standard_assets", "02_Intros", "ਤੁਹਾਡਾ ਸਵਾਗਤ ਹੈ.mp4"), help="Path to intro video clip")
    parser.add_argument("--no-intro", action="store_true", help="Disable prepending the intro video clip")
    parser.add_argument("--outro", default=os.path.join(WORKSPACE_DIR, "04-assets", "standard_assets", "03_Outros", "PG002_SEC05_OUTRO.mp4.mp4"), help="Path to outro video clip")
    parser.add_argument("--no-outro", action="store_true", help="Disable appending the outro video clip")
    parser.add_argument("--no-captions", action="store_true", help="Disable burning hard captions/subtitles onto the image shots")
    args = parser.parse_args()
    
    assembly_file = os.path.normpath(os.path.join(WORKSPACE_DIR, "05-outputs", "final_reels", f"{args.id}_reel_assembly.json"))
    suffix = "_calibration_reel.mp4" if args.calibrate else "_final_reel.mp4"
    output_video = os.path.normpath(os.path.join(WORKSPACE_DIR, "05-outputs", "final_reels", f"{args.id}{suffix}"))
    
    print("====================================================")
    print(f"  Gurbani Video Assembler - Render")
    print(f"  Concept ID: {args.id}")
    print(f"  Output Video: {output_video}")
    print("====================================================")
    
    assembly = load_assembly(assembly_file)
    
    # --- P4 FIX: Audio/Video Timeline Sync Correction ---
    # The storyboard uses LLM-guessed shot durations. After TTS generation,
    # pipeline_runner.py saves the exact audio duration to a sidecar JSON.
    # We read it here and adjust the last shot's duration so the compiled
    # visual track matches the audio track length before any clip is encoded.
    vo_audio_path_raw = assembly.get("audio_track", "")
    sidecar_path = os.path.splitext(os.path.normpath(vo_audio_path_raw))[0] + "_duration.json"
    if os.path.exists(sidecar_path):
        try:
            with open(sidecar_path, "r", encoding="utf-8") as sf:
                sidecar = json.load(sf)
            measured_audio_duration = sidecar.get("audio_duration_seconds")
            timeline = assembly.get("timeline", [])
            if measured_audio_duration and timeline:
                visual_total = sum(shot.get("duration", 0) for shot in timeline)
                delta = measured_audio_duration - visual_total
                if abs(delta) > 0.1:
                    print(f"[!] Timeline sync correction: Visual={visual_total:.2f}s, "
                          f"Audio={measured_audio_duration:.2f}s, Delta={delta:+.2f}s")
                    timeline[-1]["duration"] = max(0.5, timeline[-1]["duration"] + delta)
                    print(f"[+] Last shot duration adjusted to {timeline[-1]['duration']:.2f}s to match audio.")
                else:
                    print(f"[+] Timeline sync OK: Visual={visual_total:.2f}s, Audio={measured_audio_duration:.2f}s")
        except (json.JSONDecodeError, KeyError, ValueError, TypeError) as e:
            print(f"[!] Could not parse duration sidecar ({e}). Proceeding without sync correction.")
    else:
        print("[!] No audio duration sidecar found. Run step 7 first for accurate sync.")
    
    # Create temp directory inside workspace
    temp_dir = os.path.join(WORKSPACE_DIR, "05-outputs", "final_reels", f"temp_{args.id}")
    os.makedirs(temp_dir, exist_ok=True)
    
    clips = []
    
    for shot in assembly.get("timeline", []):
        clip = compile_shot(shot, args.id, temp_dir, calibrate=args.calibrate, no_captions=args.no_captions)
        if clip:
            clips.append(clip)
        else:
            print(f"[-] Failed to compile Shot {shot['shot_number']}. Exiting.")
            sys.exit(1)
            
    if not clips:
        print("[-] No clips compiled.")
        sys.exit(1)
        
    # Concatenate the video clips
    print("\n[*] Concatenating video clips...")
    concat_list_path = os.path.join(temp_dir, "concat_list.txt")
    with open(concat_list_path, "w", encoding="utf-8") as f:
        for clip in clips:
            # Normalize path slashes for FFmpeg demuxer
            safe_path = clip.replace("\\", "/")
            f.write(f"file '{safe_path}'\n")
            
    temp_video_only = os.path.join(temp_dir, "temp_video_only.mp4")
    
    cmd_concat = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_list_path,
        "-c", "copy",
        temp_video_only
    ]
    
    if not run_cmd(cmd_concat):
        print("[-] Failed to concatenate video clips.")
        sys.exit(1)
        
    # Merge Audio (Voiceover + BGM) for the main content block
    print("\n[*] Mixing voiceover audio, background music, and rendering temporary content clip...")
    vo_audio = os.path.normpath(assembly.get("audio_track", ""))
    bgm_track_raw = assembly.get("bgm_track", "")
    bgm_volume = float(assembly.get("bgm_volume", 0.15))
    
    # Try the specified BGM path, fallback to default bg_music.mp3
    bgm_audio = None
    if bgm_track_raw:
        bgm_path_temp = os.path.normpath(bgm_track_raw)
        if os.path.exists(bgm_path_temp):
            bgm_audio = bgm_path_temp
            
    if not bgm_audio:
        fallback_bgm = os.path.normpath(os.path.join(WORKSPACE_DIR, "04-assets", "bgm", "bg_music.mp3"))
        if os.path.exists(fallback_bgm):
            bgm_audio = fallback_bgm
            print(f"[+] BGM file found (fallback): {bgm_audio}")
            
    temp_content_mixed = os.path.join(temp_dir, "temp_content_mixed.mp4")
            
    if not os.path.exists(vo_audio) or os.path.getsize(vo_audio) == 0:
        print("[!] Voiceover audio not found or empty. Content will be video only.")
        cmd_final = [
            "ffmpeg", "-y",
            "-i", temp_video_only,
            "-c:v", "copy",
            temp_content_mixed
        ]
    elif not bgm_audio:
        print("[!] Background music not found. Content will be video with voiceover only.")
        cmd_final = [
            "ffmpeg", "-y",
            "-i", temp_video_only,
            "-i", vo_audio,
            "-c:v", "copy",
            "-af", "apad",
            "-c:a", "aac",
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-shortest",
            temp_content_mixed
        ]
    else:
        print(f"[+] Mixing Voiceover + BGM (Volume: {bgm_volume})...")
        cmd_final = [
            "ffmpeg", "-y",
            "-i", temp_video_only,
            "-i", vo_audio,
            "-stream_loop", "-1", "-i", bgm_audio,
            "-filter_complex", f"[1:a]volume=1.0,apad[vo];[2:a]volume={bgm_volume}[bgm];[vo][bgm]amix=inputs=2:duration=first:dropout_transition=2[a]",
            "-c:v", "copy",
            "-c:a", "aac",
            "-map", "0:v:0",
            "-map", "[a]",
            "-shortest",
            temp_content_mixed
        ]
        
    if not run_cmd(cmd_final):
        print("[-] Failed to merge audio and render temporary content clip.")
        sys.exit(1)

    # --- SPLICING (Intro / Outro) and Watermark Logo Overlay ---
    def has_audio(file_path):
        if not os.path.exists(file_path):
            return False
        cmd = [
            "ffprobe", "-v", "error",
            "-select_streams", "a",
            "-show_entries", "stream=codec_type",
            "-of", "csv=p=0",
            file_path
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return "audio" in result.stdout.strip()

    input_clips = []
    
    # 1. Add Intro if active and exists
    intro_active = not args.no_intro and args.intro and os.path.exists(args.intro)
    if intro_active:
        input_clips.append(args.intro)
        print(f"[+] Intro clip included: {args.intro}")
        
    # 2. Add Main content
    input_clips.append(temp_content_mixed)
    
    # 3. Add Outro if active and exists
    outro_active = not args.no_outro and args.outro and os.path.exists(args.outro)
    if outro_active:
        input_clips.append(args.outro)
        print(f"[+] Outro clip included: {args.outro}")
        
    # 4. Watermark logo
    logo_path = os.path.normpath(os.path.join(WORKSPACE_DIR, "04-assets", "standard_assets", "01_Logos", "logo.mp4"))
    watermark_active = not args.no_watermark and os.path.exists(logo_path)
    
    if len(input_clips) == 1 and not watermark_active:
        print("[*] No intro, outro, or watermark logo active. Writing final output directly...")
        if os.path.exists(output_video):
            os.remove(output_video)
        os.rename(temp_content_mixed, output_video)
        splicing_success = True
    else:
        print(f"[*] Compiling final video (Clips={len(input_clips)}, Watermark={watermark_active}) -> {output_video}")
        cmd_splice = ["ffmpeg", "-y"]
        for clip in input_clips:
            cmd_splice.extend(["-i", clip])
            
        if watermark_active:
            cmd_splice.extend(["-stream_loop", "-1", "-i", logo_path])
            print(f"[+] Watermark logo active: {logo_path}")
            
        filter_parts = []
        concat_in = ""
        N = len(input_clips)
        
        for idx in range(N):
            # Conform video stream to 1080x1920 portrait (letterbox padding if landscape)
            filter_parts.append(
                f"[{idx}:v]scale=1080:1920:force_original_aspect_ratio=decrease,"
                f"pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1[v{idx}]"
            )
            # Ensure audio stream exists and resample to standard format
            if has_audio(input_clips[idx]):
                filter_parts.append(
                    f"[{idx}:a]aresample=async=1,aformat=sample_rates=44100:channel_layouts=stereo[a{idx}]"
                )
            else:
                # Fallback: Generate a silent stereo audio stream
                filter_parts.append(
                    f"anullsrc=r=44100:cl=stereo[silent_a{idx}]"
                )
                filter_parts.append(
                    f"[silent_a{idx}]aformat=sample_rates=44100:channel_layouts=stereo[a{idx}]"
                )
            concat_in += f"[v{idx}][a{idx}]"
            
        # Concatenate conform video/audio tracks
        filter_parts.append(f"{concat_in}concat=n={N}:v=1:a=1[concatv][concata]")
        
        # Apply circular watermark overlay if active
        if watermark_active:
            logo_idx = N  # Logo is the last input stream
            filter_parts.append(
                f"[{logo_idx}:v]format=rgba,geq=lum='p(X,Y)':a='if(gt(sqrt(pow(X-W/2,2)+pow(Y-H/2,2)),W/2),0,255)'[mask]"
            )
            filter_parts.append(
                f"[{logo_idx}:v][mask]alphamerge,scale=150:150[logo_circle]"
            )
            filter_parts.append(
                f"[concatv][logo_circle]overlay=W-w-50:H-h-50:shortest=1[outv]"
            )
            
            filter_complex_str = ";".join(filter_parts)
            cmd_splice.extend([
                "-filter_complex", filter_complex_str,
                "-map", "[outv]",
                "-map", "[concata]"
            ])
        else:
            filter_complex_str = ";".join(filter_parts)
            cmd_splice.extend([
                "-filter_complex", filter_complex_str,
                "-map", "[concatv]",
                "-map", "[concata]"
            ])
            
        cmd_splice.extend([
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-shortest",
            output_video
        ])
        
        splicing_success = run_cmd(cmd_splice)
        
    if splicing_success:
        print("\n[+] SUCCESS! Final video compiled successfully.")
        print(f"[+] Output file: {output_video}")
        
        # Clean up temp files
        print("[*] Cleaning up temporary files...")
        for clip in clips:
            try:
                os.remove(clip)
            except:
                pass
        try:
            os.remove(concat_list_path)
            os.remove(temp_video_only)
            if os.path.exists(temp_content_mixed):
                os.remove(temp_content_mixed)
            os.rmdir(temp_dir)
        except Exception as e:
            print(f"[!] Cleanup warning: {e}")
            pass
        print("[+] Cleanup complete.")
    else:
        print("[-] Splicing and final assembly failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
