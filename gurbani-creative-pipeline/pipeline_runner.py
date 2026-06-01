import os
import json
import urllib.request
import sys
import argparse
import subprocess
import re

# Reconfigure stdout/stderr to UTF-8 on Windows to prevent UnicodeEncodeErrors
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

# Define base paths
WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(WORKSPACE_DIR, "config", "antigravity_pipeline.json")
AGENTS_DIR = os.path.join(WORKSPACE_DIR, "02-koda-agents-adapted")

def extract_script_text(script_path):
    if not os.path.exists(script_path):
        return None
    text_blocks = []
    with open(script_path, "r", encoding="utf-8") as f:
        for line in f:
            line_str = line.strip()
            if not line_str:
                continue
            # Skip pure structural markers (headers, block labels, dividers)
            if line_str.startswith("#") or line_str.startswith("---"):
                continue
            # Skip metadata lines
            if line_str.lower().startswith("format:") or line_str.lower().startswith("tone:"):
                continue
            # Skip visual cues or block labels enclosed in brackets
            if line_str.startswith("["):
                lowered = line_str.lower()
                if "visual cue" in lowered or "block" in lowered or "sec" in lowered:
                    continue
            # Strip the "Voiceover:" prefix if it exists
            if line_str.lower().startswith("voiceover:"):
                line_str = line_str[len("voiceover:"):].strip()
            # P2 FIX: Strip bracket wrappers — fallback for bracketed speech blocks
            elif line_str.startswith("[") and line_str.endswith("]"):
                line_str = line_str[1:-1].strip()
            if line_str:
                text_blocks.append(line_str)
    return " ".join(text_blocks) if text_blocks else None




def load_config():
    if not os.path.exists(CONFIG_PATH):
        print(f"[-] Config not found at {CONFIG_PATH}")
        sys.exit(1)
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def format_path(path_template, item_id):
    if not path_template:
        return path_template
    # Replace templates (normalize backslashes for Windows compatibility)
    normalized_workspace = WORKSPACE_DIR.replace("\\", "/")
    formatted = path_template.replace("{workspace_root}", normalized_workspace).replace("{id}", item_id)
    return os.path.normpath(formatted)

def get_api_key():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        env_path = os.path.join(WORKSPACE_DIR, ".env")
        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("GEMINI_API_KEY="):
                        api_key = line.split("=", 1)[1].strip()
                        break
    return api_key

def call_gemini(system_prompt, user_content, api_key, model="gemini-2.5-flash"):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    
    combined_prompt = f"{system_prompt}\n\n=== INPUT CONTENT ===\n{user_content}\n\n=== RESPONSE ==="
    
    body = {
        "contents": [
            {
                "parts": [
                    {"text": combined_prompt}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.2
        }
    }
    
    req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            if "candidates" in res_data and len(res_data["candidates"]) > 0:
                part = res_data["candidates"][0]["content"]["parts"][0]
                return part.get("text", "")
            else:
                print("[-] Empty response from Gemini API.")
                return None
    except Exception as e:
        print(f"[-] Exception occurred during Gemini API call: {e}")
        return None

def get_audio_duration(audio_path):
    """Use ffprobe to measure an audio file's duration in seconds."""
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
        except (json.JSONDecodeError, KeyError, ValueError):
            pass
    return None

def get_hf_token():
    token = os.environ.get("HF_TOKEN")
    if not token:
        env_path = os.path.join(WORKSPACE_DIR, ".env")
        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("HF_TOKEN="):
                        token = line.split("=", 1)[1].strip()
                        break
    return token

def parse_script_blocks(script_path):
    if not os.path.exists(script_path):
        return None
    blocks = []
    current_block = None
    with open(script_path, "r", encoding="utf-8") as f:
        for line in f:
            line_str = line.strip()
            if not line_str:
                continue
            # Skip script header
            if line_str.startswith("#") or line_str.startswith("---"):
                continue
            if line_str.lower().startswith("format:") or line_str.lower().startswith("tone:"):
                continue
            # Check if block header, e.g., [0:00 - 0:08] BLOCK 1 — HOOK
            if line_str.startswith("[") and "block" in line_str.lower():
                current_block = {
                    "header": line_str,
                    "text_lines": []
                }
                blocks.append(current_block)
            else:
                if current_block is not None:
                    # Strip prefixes if they exist
                    if line_str.lower().startswith("voiceover:"):
                        line_str = line_str[len("voiceover:"):].strip()
                    elif line_str.startswith("[") and line_str.endswith("]"):
                        line_str = line_str[1:-1].strip()
                    if line_str:
                        current_block["text_lines"].append(line_str)
    
    result = []
    for b in blocks:
        text = " ".join(b["text_lines"]).strip()
        if text:
            match = re.search(r"block\s+(\d+)", b["header"], re.IGNORECASE)
            b_num = int(match.group(1)) if match else 1
            result.append({
                "block_num": b_num,
                "header": b["header"],
                "text": text
            })
    return result

def query_gradio_tts(text, description, token):
    base_url = "https://ai4bharat-indic-parler-tts.hf.space/gradio_api"
    call_url = f"{base_url}/call/generate_finetuned"
    
    import requests
    import time
    import json
    
    tokens_to_try = [token] if token else [None]
    if token:
        tokens_to_try.append(None)  # Add Guest Mode fallback
        
    for t in tokens_to_try:
        headers = {"Content-Type": "application/json"}
        if t:
            headers["Authorization"] = f"Bearer {t}"
            print("    Querying TTS using HF Token...")
        else:
            print("    Querying TTS in Guest Mode...")
            
        payload = {"data": [text, description]}
        
        max_retries = 3
        success = False
        audio_content = None
        
        for attempt in range(1, max_retries + 1):
            try:
                if attempt > 1:
                    print(f"    TTS call attempt {attempt}/{max_retries}...")
                response = requests.post(call_url, headers=headers, json=payload, timeout=30)
                if response.status_code != 200:
                    print(f"    [-] Error calling Gradio API on attempt {attempt}: {response.status_code}")
                    if attempt < max_retries:
                        time.sleep(2)
                        continue
                    break
                event_id = response.json().get("event_id")
                
                stream_url = f"{call_url}/{event_id}"
                stream_resp = requests.get(stream_url, headers=headers, stream=True, timeout=60)
                
                for line_bytes in stream_resp.iter_lines():
                    if line_bytes:
                        line = line_bytes.decode('utf-8').strip()
                        if line.startswith("data:"):
                            data_str = line[5:].strip()
                            # Print a short debug snippet of raw data
                            print(f"    [debug] Raw data event: {data_str[:150]}")
                            try:
                                data_json = json.loads(data_str)
                                if data_json is None:
                                    print("    [debug] Received data: null event (rate limit/quota error).")
                                    break
                                    
                                file_info = None
                                # Check if the structure is a direct list (generating/complete event for files)
                                if isinstance(data_json, list) and len(data_json) > 0:
                                    file_info = data_json[0]
                                # Also check if it's a dict containing output (Gradio v5 complete event)
                                elif isinstance(data_json, dict):
                                    if "msg" in data_json and data_json["msg"] == "process_completed":
                                        output = data_json.get("output", {})
                                        data_list = output.get("data", [])
                                        if isinstance(data_list, list) and len(data_list) > 0:
                                            file_info = data_list[0]
                                            
                                if file_info and isinstance(file_info, dict) and "path" in file_info:
                                    path = file_info["path"]
                                    download_url = f"https://ai4bharat-indic-parler-tts.hf.space/gradio_api/file={path}"
                                    print(f"    [+] Found audio path. Downloading from HF Space...")
                                    dl_resp = requests.get(download_url, headers=headers, timeout=30)
                                    if dl_resp.status_code == 200:
                                        audio_content = dl_resp.content
                                        success = True
                                        break
                                    else:
                                        print(f"    [-] Download failed: {dl_resp.status_code}")
                            except Exception as parse_err:
                                print(f"    [debug] JSON parse error: {parse_err}")
                if success:
                    break
                # If we received a null event or rate limit, break early from retrying this token
                if not success and 'data_json' in locals() and data_json is None:
                    break
                if attempt < max_retries:
                    time.sleep(2)
            except Exception as e:
                print(f"    [-] Exception during attempt {attempt}: {e}")
                if attempt < max_retries:
                    time.sleep(2)
                    
        if success:
            return audio_content
            
    return None

def execute_step(step_cfg, item_id, api_key, model):
    agent_name = step_cfg["agent"]
    step_num = step_cfg["step"]
    desc = step_cfg["description"]
    
    print(f"\n[+] Executing Step {step_num}: {agent_name} ({desc}) [ID: {item_id}]")
    
    # Load agent prompt definition
    agent_prompt_path = os.path.join(AGENTS_DIR, f"{agent_name}.md")
    if not os.path.exists(agent_prompt_path):
        print(f"[-] Agent system prompt file not found: {agent_prompt_path}")
        return False
        
    with open(agent_prompt_path, "r", encoding="utf-8") as f:
        system_prompt = f.read()
        
    # Read input file (format template first)
    raw_input_path = step_cfg.get("input_file")
    if not raw_input_path:
        print(f"[!] No direct input file defined for step {step_num}. Skipping LLM process.")
        return True
        
    input_file = format_path(raw_input_path, item_id)
    if not os.path.exists(input_file):
        print(f"[-] Input file not found: {input_file}")
        print(f"[!] Please ensure previous steps have executed successfully.")
        return False
        
    with open(input_file, "r", encoding="utf-8") as f:
        input_content = f.read().strip()
        
    if not input_content:
        print(f"[-] Input file is empty: {input_file}")
        return False
        
    # Get outputs formatted
    raw_output_file = step_cfg.get("output_file")
    output_file = format_path(raw_output_file, item_id) if raw_output_file else None
    
    raw_output_dir = step_cfg.get("output_dir")
    output_dir = format_path(raw_output_dir, item_id) if raw_output_dir else None
        
    # Check if this is an API-based generator step
    if agent_name == "06_assets_producer":
        # P1 FIX: Generate real, FFmpeg-decodeable PNG placeholders instead of
        # text stubs. The old code wrote "MOCK_IMAGE_DATA" in text mode, which
        # FFmpeg cannot decode and would crash on the zoompan filter step.
        print(f"[*] Step {step_num} is an asset generator step (Image Producer). Ensuring shot files exist...")
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            for i in range(1, 10):
                shot_filename = f"{item_id}_shot-{i:02d}.png"
                shot_path = os.path.join(output_dir, shot_filename)
                if not os.path.exists(shot_path):
                    # Generate a valid dark-background 1080x1920 PNG via FFmpeg lavfi
                    cmd = [
                        "ffmpeg", "-y",
                        "-f", "lavfi",
                        "-i", "color=c=0x0B0E14:s=1080x1920:d=1",
                        "-vframes", "1",
                        shot_path
                    ]
                    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    if result.returncode == 0:
                        print(f"[+] Generated placeholder image: {shot_filename}")
                    else:
                        print(f"[-] FFmpeg failed to generate placeholder for {shot_filename}: {result.stderr[:200]}")
                        return False
        return True
        
    elif agent_name == "07_voiceover_generator":
        print(f"[*] Parsing script for voice synthesis...")
        script_text = extract_script_text(input_file)
        if not script_text:
            print("[-] Failed to extract text from script file. Check that the script has content inside [brackets].")
            return False
            
        # Check if the script contains Punjabi characters
        is_punjabi = any('\u0a00' <= char <= '\u0a7f' for char in script_text)
        
        if is_punjabi:
            print("[+] Punjabi language detected. Synthesizing using ai4bharat/indic-parler-tts via Hugging Face...")
            hf_token = get_hf_token()
            if not hf_token:
                print("[!] Warning: Hugging Face token (HF_TOKEN) not found in environment or .env file.")
                print("    Falling back to Guest Mode (rate limits may apply).")
                
            blocks = parse_script_blocks(input_file)
            if not blocks:
                print("[-] Failed to parse script blocks.")
                return False
                
            print(f"[+] Successfully parsed {len(blocks)} script blocks. Starting block-by-block synthesis...")
            temp_files = []
            
            # 80/20 Descriptions
            desc_secular = "A male speaker with a clear, warm, conversational voice delivers the speech at a moderate pace in a studio-quality recording with no background noise."
            desc_sacred = "A male speaker with a deep, resonant, authoritative voice delivers the speech at a slow pace in a high-quality recording with no background noise."
            
            for b in blocks:
                b_num = b["block_num"]
                text = b["text"]
                
                # Blocks 1 to 3: Secular; Blocks 4 and 5: Sacred (Turn & Citation)
                is_sacred = b_num >= 4
                desc = desc_sacred if is_sacred else desc_secular
                
                print(f"[*] Generating Block {b_num} ({'SACRED' if is_sacred else 'SECULAR'}):")
                print(f"    Text: {text}")
                
                audio_content = query_gradio_tts(text, desc, hf_token)
                if audio_content:
                    temp_file = os.path.normpath(os.path.join(os.path.dirname(output_file), f"temp_block_{b_num}.mp3"))
                    with open(temp_file, "wb") as f:
                        f.write(audio_content)
                    print(f"    [+] Saved block to: {temp_file}")
                    temp_files.append(temp_file)
                else:
                    print(f"[-] Failed to generate audio for Block {b_num}")
                    # Clean up temp files
                    for f in temp_files:
                        try: os.remove(f)
                        except: pass
                    return False
                    
            # Trim leading and trailing silence on each individual block before concatenating
            print("[*] Trimming leading and trailing silence from generated blocks...")
            trimmed_files = []
            for f in temp_files:
                trimmed_f = f.replace(".mp3", "_trimmed.mp3")
                # Apply double-reverse silence trimming filter (threshold: -45dB)
                filter_str = "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse"
                cmd_trim = [
                    "ffmpeg", "-y",
                    "-i", f,
                    "-af", filter_str,
                    "-c:a", "libmp3lame",
                    "-q:a", "2",
                    trimmed_f
                ]
                result_trim = subprocess.run(cmd_trim, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if result_trim.returncode == 0:
                    trimmed_files.append(trimmed_f)
                else:
                    print(f"[-] Trimming failed for {f}: {result_trim.stderr.decode('utf-8', errors='ignore')}")
                    # Fallback to untrimmed
                    trimmed_files.append(f)
                    
            print(f"[*] Concatenating {len(trimmed_files)} blocks using complex filtergraph...")
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            # Concatenate using FFmpeg complex filtergraph to prevent click/pop artifacts
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
                output_file
            ])
            
            result = subprocess.run(concat_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # Clean up temp files (both original and trimmed)
            for f in temp_files:
                try: os.remove(f)
                except: pass
            for f in trimmed_files:
                try: os.remove(f)
                except: pass
                
            if result.returncode == 0:
                print(f"[+] Successfully concatenated and saved voiceover audio at: {output_file}")
            else:
                print(f"[-] FFmpeg concatenation failed: {result.stderr}")
                return False
                
            # Measure duration
            duration = get_audio_duration(output_file)
            if duration:
                sidecar_path = os.path.splitext(output_file)[0] + "_duration.json"
                with open(sidecar_path, "w", encoding="utf-8") as df:
                    json.dump({"audio_duration_seconds": round(duration, 3)}, df)
                print(f"[+] Audio duration: {duration:.2f}s (saved sidecar for render sync)")
            else:
                print("[!] Could not measure audio duration via ffprobe. Sync correction will be skipped.")
                
            return True
            
        else:
            # Fallback to edge_tts for non-Punjabi text
            print(f"[*] Synthesizing non-Punjabi voice via edge-tts...")
            if output_file:
                os.makedirs(os.path.dirname(output_file), exist_ok=True)
                selected_voice = "en-US-ChristopherNeural"
                print(f"[+] Using voice: {selected_voice}")
                
                import asyncio
                import edge_tts
                
                async def run_tts():
                    communicate = edge_tts.Communicate(script_text, selected_voice)
                    await communicate.save(output_file)
                    
                print(f"[*] Running edge_tts Communicate locally in Python loop...")
                try:
                    asyncio.run(run_tts())
                except Exception as e:
                    print(f"[-] edge-tts failed: {e}")
                    return False
                print(f"[+] Successfully generated voiceover audio at: {output_file}")
                
                duration = get_audio_duration(output_file)
                if duration:
                    sidecar_path = os.path.splitext(output_file)[0] + "_duration.json"
                    with open(sidecar_path, "w", encoding="utf-8") as df:
                        json.dump({"audio_duration_seconds": round(duration, 3)}, df)
                    print(f"[+] Audio duration: {duration:.2f}s (saved sidecar for render sync)")
                else:
                    print("[!] Could not measure audio duration via ffprobe. Sync correction will be skipped.")
            return True

        
    # Standard LLM execution
    if not api_key:
        print("[-] GEMINI_API_KEY environment variable or config not found.")
        print("[!] Please set your GEMINI_API_KEY to execute standard LLM agents.")
        return False
        
    print(f"[*] Sending prompt to Gemini API ({model})...")
    output_text = call_gemini(system_prompt, input_content, api_key, model)
    
    if not output_text:
        print(f"[-] Failed to get response for {agent_name}")
        return False
        
    # Write output file
    if output_file:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(output_text)
        print(f"[+] Success! Output saved to: {output_file}")
        
        # Script Preprocessing hook: automatically normalize and extract terms on step 1
        if step_num == 1:
            print("[*] Hook: Automatically running Gurmukhi script preprocessor on generated script...")
            try:
                sys.path.append(os.path.join(WORKSPACE_DIR, "03-scripts"))
                from preprocess_script import preprocess_script
                preprocess_script(output_file)
            except Exception as e:
                print(f"[!] Error running script preprocessor: {e}")
    else:
        print(f"[!] No output file configured for step {step_num}. Displaying response:")
        print(output_text)
        
    return True

def run_thumbnail_generation(item_id):
    print(f"\n[*] Generating premium thumbnail for ID '{item_id}'...")
    script_path = os.path.normpath(os.path.join(WORKSPACE_DIR, "03-scripts", "audio_scripts", f"{item_id}_script.md"))
    title_en = "Gurbani Reflection"
    title_pa = "ਗੁਰਬਾਣੀ"
    
    if os.path.exists(script_path):
        with open(script_path, "r", encoding="utf-8") as f:
            first_line = f.readline().strip()
            match = re.search(r"SCRIPT:\s*([^|#]+)", first_line, re.IGNORECASE)
            if match:
                title_en = match.group(1).strip()
            
            f.seek(0)
            content = f.read()
            pa_words = re.findall(r"[\u0a00-\u0a7f]+", content)
            if pa_words:
                long_words = [w for w in pa_words if len(w) > 1]
                if long_words:
                    title_pa = long_words[0]
                    
    known_titles = {
        "gurbani_01": ("ਦਰਦ ਹੀ ਦਾਰੂ ਹੈ", "Pain is the Medicine"),
        "gurbani_02": ("ਸਬਰ ਅਤੇ ਸਿਦਕ", "Patience and Faith"),
    }
    if item_id in known_titles:
        title_pa, title_en = known_titles[item_id]
        
    print(f"[+] Text selected: Punjabi='{title_pa}', English='{title_en}'")
    
    try:
        sys.path.append(os.path.join(WORKSPACE_DIR, "03-scripts", "utils"))
        from thumbnail_generator import create_premium_thumbnail
        
        output_file = os.path.normpath(os.path.join(WORKSPACE_DIR, "05-outputs", "final_reels", f"{item_id}_thumbnail.jpg"))
        
        bg_img = None
        gen_dir = os.path.join(WORKSPACE_DIR, "04-assets", "generated_images", item_id)
        if os.path.exists(gen_dir):
            shots = [f for f in os.listdir(gen_dir) if f.endswith(".png")]
            if shots:
                bg_img = os.path.join(gen_dir, sorted(shots)[0])
                
        create_premium_thumbnail(bg_img, title_pa, title_en, output_file)
    except Exception as e:
        print(f"[!] Error generating thumbnail: {e}")

def run_youtube_upload(item_id, privacy):
    print(f"\n[*] Uploading final video for ID '{item_id}' to YouTube (privacy={privacy})...")
    video_path = os.path.normpath(os.path.join(WORKSPACE_DIR, "05-outputs", "final_reels", f"{item_id}_final_reel.mp4"))
    thumbnail_path = os.path.normpath(os.path.join(WORKSPACE_DIR, "05-outputs", "final_reels", f"{item_id}_thumbnail.jpg"))
    
    if not os.path.exists(video_path):
        print(f"[-] Video file not found: {video_path}")
        return
        
    metadata_path = os.path.normpath(os.path.join(WORKSPACE_DIR, "05-outputs", "final_reels", f"{item_id}_publish_metadata.md"))
    title = f"Gurbani Reflection: {item_id}"
    description = "Gurbani Creative Pipeline Upload."
    tags = "Gurbani, Reflection, Meditation"
    
    if os.path.exists(metadata_path):
        with open(metadata_path, "r", encoding="utf-8") as f:
            content = f.read()
            title_match = re.search(r"#\s*PUBLISH\s*METADATA:\s*(.+)", content, re.IGNORECASE)
            if title_match:
                title = f"Gurbani: {title_match.group(1).strip()}"
            
            caption_match = re.search(r"###\s*Caption\s*\n+(.+?)\n+###", content, re.DOTALL | re.IGNORECASE)
            if caption_match:
                description = caption_match.group(1).strip()
            else:
                caption_match2 = re.search(r"###\s*Caption\s*\n+(.+?)(?:###|$)", content, re.DOTALL | re.IGNORECASE)
                if caption_match2:
                    description = caption_match2.group(1).strip()
                    
            tags_match = re.search(r"###\s*Hashtags\s*\n+(.+?)(?:###|$)", content, re.DOTALL | re.IGNORECASE)
            if tags_match:
                tags = tags_match.group(1).strip().replace("#", "").replace("\n", ",").replace(" ", "")
                
    print(f"[+] YouTube metadata: Title='{title}'")
    
    try:
        sys.path.append(os.path.join(WORKSPACE_DIR, "03-scripts", "utils"))
        import youtube_uploader
        
        service = youtube_uploader.get_authenticated_service()
        tag_list = [t.strip() for t in tags.split(",") if t.strip()]
        
        video_id = youtube_uploader.upload_video(
            service,
            video_path,
            title=title,
            description=description,
            tags=tag_list,
            privacy=privacy
        )
        
        if os.path.exists(thumbnail_path):
            youtube_uploader.set_thumbnail(service, video_id, thumbnail_path)
            
        print(f"[+] Video uploaded successfully! URL: https://youtu.be/{video_id}")
    except Exception as e:
        print(f"[!] Error uploading to YouTube: {e}")

def main():
    config = load_config()
    
    # Configure Argument Parser
    parser = argparse.ArgumentParser(description="Gurbani Creative Pipeline Orchestrator")
    parser.add_argument("step", nargs="?", default="help", help="Step number (1-10), 'all', or 'help'")
    parser.add_argument("--id", "-i", default="gurbani_01", help="Unique ID of the shabad/concept (default: gurbani_01)")
    parser.add_argument("--thumbnail", action="store_true", help="Generate premium thumbnail after step execution")
    parser.add_argument("--upload", action="store_true", help="Upload final video to YouTube after step execution")
    parser.add_argument("--privacy", default="private", choices=["private", "unlisted", "public"], help="Privacy status for YouTube upload (default: private)")
    
    args = parser.parse_args()
    
    print("====================================================")
    print(f"  {config['pipeline_name']} - Runner")
    print(f"  Target Concept ID: {args.id}")
    print("====================================================")
    
    api_key = get_api_key()
    model = config.get("default_model", "gemini-2.5-flash")
    
    if not api_key:
        print("[!] Warning: GEMINI_API_KEY not found in environment or .env file.")
        print("    You can run steps, but LLM API calls will fail.")
        print("    Please set the GEMINI_API_KEY environment variable.")
        print("----------------------------------------------------")
    
    pipeline_flow = config.get("pipeline_flow", [])
    
    # Process actions
    step_input = args.step.lower()
    
    if step_input.isdigit():
        step_num = int(step_input)
        step_cfg = next((s for s in pipeline_flow if s["step"] == step_num), None)
        if step_cfg:
            success = execute_step(step_cfg, args.id, api_key, model)
            if success:
                if args.thumbnail:
                    run_thumbnail_generation(args.id)
                if args.upload:
                    run_youtube_upload(args.id, args.privacy)
            sys.exit(0 if success else 1)
        else:
            print(f"[-] Invalid step number: {step_num}")
            sys.exit(1)
            
    elif step_input == "all":
        print(f"[*] Running all pipeline steps sequentially for ID '{args.id}'...")
        for step_cfg in pipeline_flow:
            success = execute_step(step_cfg, args.id, api_key, model)
            if not success:
                print(f"[-] Pipeline stopped at step {step_cfg['step']} due to error.")
                sys.exit(1)
        print(f"[+] Entire pipeline executed successfully for ID '{args.id}'!")
        if args.thumbnail:
            run_thumbnail_generation(args.id)
        if args.upload:
            run_youtube_upload(args.id, args.privacy)
        sys.exit(0)
        
    else:
        # Default: Show help and steps
        print("Available Steps:")
        for step in pipeline_flow:
            # Format inputs/outputs temporarily for display
            formatted_input = format_path(step.get("input_file"), args.id)
            formatted_output = format_path(step.get("output_file"), args.id)
            print(f"  {step['step']}. {step['description']} (Agent: {step['agent']})")
            if formatted_input:
                print(f"     In:  {os.path.basename(formatted_input)}")
            if formatted_output:
                print(f"     Out: {os.path.basename(formatted_output)}")
        print("\nUsage:")
        print("  py pipeline_runner.py [step_number] --id [name]  - Execute a specific step for ID")
        print("  py pipeline_runner.py all --id [name]            - Execute the whole pipeline for ID")
        print("====================================================")

if __name__ == "__main__":
    main()
