import os
import urllib.request

WORKSPACE_DIR = r"F:\Punjabi_Guftar_Workspace"
OUTPUT_DIR = os.path.join(WORKSPACE_DIR, "04_Audio_Recording_Studio", "03_Soundscapes")
MP3_URL = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"

def download_music():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    print("Downloading background music...")
    dest = os.path.join(OUTPUT_DIR, "bg_music.mp3")
    urllib.request.urlretrieve(MP3_URL, dest)
    print("\nBackground Music Downloaded Successfully!")

if __name__ == "__main__":
    download_music()
