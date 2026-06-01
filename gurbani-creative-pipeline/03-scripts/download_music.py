import os
import urllib.request

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_DIR = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(WORKSPACE_DIR, "04-assets", "bgm")
MP3_URL = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"

def download_music():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    print("Downloading background music...")
    dest = os.path.join(OUTPUT_DIR, "bg_music.mp3")
    urllib.request.urlretrieve(MP3_URL, dest)
    print(f"\nBackground Music Downloaded Successfully to: {dest}")

if __name__ == "__main__":
    download_music()
