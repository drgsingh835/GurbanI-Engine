import os
from PIL import Image, ImageDraw, ImageFont
import subprocess

WORKSPACE_DIR = r"F:\Punjabi_Guftar_Workspace"
ASSETS_DIR = os.path.join(WORKSPACE_DIR, "00_Standard_Assets")
OUTPUT_DIR = os.path.join(WORKSPACE_DIR, "03_Visual_Laboratory", "03_Background_Media", "Animated_Chunks")
FONT_PATH = r"C:\Windows\Fonts\Nirmala.ttc"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def create_animated_chunk(name, title, main_text, sub_text, duration_sec=5, fps=30):
    width, height = 1920, 1080
    bg_color = (20, 22, 26)
    gold = (218, 165, 32)
    white = (220, 220, 220)
    gray = (150, 150, 150)
    
    title_font = ImageFont.truetype(FONT_PATH, 90)
    main_font = ImageFont.truetype(FONT_PATH, 250)
    sub_font = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 60)
    
    total_frames = int(duration_sec * fps)
    temp_frame_dir = os.path.join(OUTPUT_DIR, f"temp_{name}")
    if not os.path.exists(temp_frame_dir):
        os.makedirs(temp_frame_dir)
        
    print(f"Generating frames for {name}...")
    
    # Simple typewriter effect: calculate how many characters per frame
    # We want the text to finish appearing by 70% of the duration
    text_appear_frames = int(total_frames * 0.7)
    chars = list(main_text.replace("  ", " ")) # Handle double spaces
    num_chars = len(chars)
    
    for i in range(total_frames):
        img = Image.new("RGB", (width, height), bg_color)
        draw = ImageDraw.Draw(img)
        
        # Border
        draw.rectangle([(80, 80), (width - 80, height - 80)], outline=gold, width=4)
        
        # Static Title
        bbox = draw.textbbox((0, 0), title, font=title_font)
        draw.text(((width - (bbox[2]-bbox[0]))/2, 200), title, font=title_font, fill=white)
        
        # Animated Main Text
        current_char_count = int(min(i / text_appear_frames * num_chars, num_chars)) if i < text_appear_frames else num_chars
        current_text = "".join(chars[:current_char_count])
        if current_text:
            bbox = draw.textbbox((0, 0), current_text, font=main_font)
            draw.text(((width - (bbox[2]-bbox[0]))/2, 400), current_text, font=main_font, fill=gold)
            
        # Static Sub Text (fades in after text appears)
        if i > text_appear_frames:
            bbox = draw.textbbox((0, 0), sub_text, font=sub_font)
            draw.text(((width - (bbox[2]-bbox[0]))/2, 800), sub_text, font=sub_font, fill=gray)
            
        img.save(os.path.join(temp_frame_dir, f"frame_{i:04d}.png"))
        
    # Combine with FFmpeg
    output_video = os.path.join(OUTPUT_DIR, f"{name}.mp4")
    cmd = [
        "ffmpeg", "-y", "-framerate", str(fps),
        "-i", os.path.join(temp_frame_dir, "frame_%04d.png"),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", output_video
    ]
    subprocess.run(cmd, check=True)
    print("\nAll 5 Animated Flashcards Generated Successfully!")

if __name__ == "__main__":
    cards = [
        {
            "name": "pg002_sec01",
            "title": "ਪੰਜਾਬੀ ਗੁਫ਼ਤਾਰ",
            "main": "ਪੈਂਤੀ ਅੱਖਰ",
            "sub": "The Science of the Gurmukhi Script",
            "dur": 5
        },
        {
            "name": "pg002_sec02",
            "title": "ਮੁੱਖ ਵਰਗ",
            "main": "ੳ  ਅ  ੲ  ਸ  ਹ",
            "sub": "The Foundation Letters",
            "dur": 10
        },
        {
            "name": "pg002_sec03",
            "title": "ਕਵਰਗ",
            "main": "ਕ  ਖ  ਗ  ਘ  ਙ",
            "sub": "The Throat Letters (Larynx)",
            "dur": 10
        },
        {
            "name": "pg002_sec04",
            "title": "ਪਵਰਗ",
            "main": "ਪ  ਫ  ਬ  ਭ  ਮ",
            "sub": "The Lips (Phonetic Progression)",
            "dur": 10
        },
        {
            "name": "pg002_sec05",
            "title": "ਪੰਜਾਬੀ ਗੁਫ਼ਤਾਰ",
            "main": "ਸਬਸਕ੍ਰਾਈਬ",
            "sub": "Preserve & Study Our Mother Tongue",
            "dur": 5
        }
    ]
    
    for card in cards:
        create_animated_chunk(
            card["name"], 
            card["title"], 
            card["main"], 
            card["sub"], 
            duration_sec=card["dur"]
        )
