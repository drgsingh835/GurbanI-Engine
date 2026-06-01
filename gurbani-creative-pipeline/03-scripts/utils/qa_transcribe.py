import os
import sys
import json
import argparse
import requests

# Reconfigure stdout/stderr to UTF-8 on Windows
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

# Define base paths
WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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

def main():
    parser = argparse.ArgumentParser(description="Gurbani Creative Pipeline - Audio Transcription QA")
    parser.add_argument("--id", "-i", default="gurbani_01", help="Unique ID of the project to transcribe (default: gurbani_01)")
    args = parser.parse_args()
    
    audio_path = os.path.normpath(os.path.join(WORKSPACE_DIR, "04-assets", "voiceover", f"{args.id}_vo_track.mp3"))
    output_path = os.path.normpath(os.path.join(WORKSPACE_DIR, "05-outputs", "final_reels", f"{args.id}_vo_transcription.txt"))
    
    print("====================================================")
    print("  Gurbani Voiceover Transcription QA")
    print(f"  Target ID: {args.id}")
    print(f"  Audio Path: {audio_path}")
    print("====================================================")
    
    if not os.path.exists(audio_path):
        print(f"[-] Voiceover track not found at: {audio_path}")
        print("[!] Please make sure step 7 of the pipeline has executed successfully.")
        sys.exit(1)
        
    hf_token = get_hf_token()
    if not hf_token:
        print("[-] Hugging Face token (HF_TOKEN) not found in environment or .env file.")
        print("[!] Please set HF_TOKEN in your .env file to authorize the Hugging Face API.")
        sys.exit(1)
        
    API_URL = "https://router.huggingface.co/hf-inference/models/openai/whisper-large-v3-turbo"
    headers = {
        "Content-Type": "audio/mpeg"
    }
    headers["Authorization"] = f"Bearer {hf_token}"
    
    print("[*] Reading audio file...")
    with open(audio_path, "rb") as f:
        audio_data = f.read()
        
    print(f"[*] Sending {len(audio_data)} bytes to Hugging Face Whisper Large-v3-Turbo ASR API...")
    try:
        response = requests.post(API_URL, headers=headers, data=audio_data, timeout=60)
        if response.status_code == 200:
            result = response.json()
            transcription = result.get("text", "")
            print("\n[+] Transcription completed successfully!")
            print("----------------------------------------------------")
            print(transcription)
            print("----------------------------------------------------")
            
            # Save output to text file
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as out_f:
                out_f.write(transcription)
            print(f"[+] Saved transcription text file to: {output_path}")
        else:
            print(f"[-] API error (HTTP {response.status_code}): {response.text}")
            sys.exit(1)
    except Exception as e:
        print(f"[-] Exception during API call: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
