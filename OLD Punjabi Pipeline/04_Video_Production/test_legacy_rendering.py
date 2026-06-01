import os
from PIL import Image, ImageDraw, ImageFont
from Gurmukhi_Processor import GurmukhiProcessor

# Configuration
BG_COLOR = (18, 18, 18)
GOLD_COLOR = (212, 175, 55)
LEGACY_FONT_PATH = r"f:\Punjabi_Guftar_Workspace\00_Standard_Assets\04_Fonts\AmrLipiHeavy.ttf"
CANVAS_SIZE = (1920, 1080)

def test_legacy_rendering(text, output_path):
    # 1. Convert to Legacy ASCII
    legacy_text = GurmukhiProcessor.to_legacy_ascii(text)
    print(f"Original: {text}")
    print(f"Legacy ASCII: {legacy_text}")

    # 2. Render with Legacy Font
    img = Image.new("RGB", CANVAS_SIZE, BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype(LEGACY_FONT_PATH, 280)
        
        # Center text
        bbox = draw.textbbox((0, 0), legacy_text, font=font)
        w, h = bbox[2]-bbox[0], bbox[3]-bbox[1]
        draw.text(((CANVAS_SIZE[0]-w)//2, (CANVAS_SIZE[1]-h)//2), legacy_text, font=font, fill=GOLD_COLOR)
        
        img.save(output_path)
        print(f"Legacy image saved to: {output_path}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_dir = r"f:\Punjabi_Guftar_Workspace\03_Visual_Laboratory\05_Tests"
    os.makedirs(test_dir, exist_ok=True)
    
    word = "ਸਬਸਕ੍ਰਾਈਬ"
    output = os.path.join(test_dir, "Subscribe_Legacy_AmrLipi.png")
    test_legacy_rendering(word, output)
