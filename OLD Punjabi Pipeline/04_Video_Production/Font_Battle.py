import os
from PIL import Image, ImageDraw, ImageFont
from Gurmukhi_Processor import GurmukhiProcessor

# Configuration
FONTS_DIR = r"f:\Punjabi_Guftar_Workspace\00_Standard_Assets\04_Fonts"
TEST_DIR = r"f:\Punjabi_Guftar_Workspace\03_Visual_Laboratory\05_Tests"
CANVAS_SIZE = (1920, 1080)
BG_COLOR = (18, 18, 18)
TEXT_COLOR = (212, 175, 55)
WORD = "ਸਬਸਕ੍ਰਾਈਬ"

def generate_font_comparison():
    os.makedirs(TEST_DIR, exist_ok=True)
    fonts = [f for f in os.listdir(FONTS_DIR) if f.lower().endswith(('.ttf', '.ttc'))]
    
    # We will generate a separate image for each font to allow high-res inspection
    for font_file in fonts:
        font_path = os.path.join(FONTS_DIR, font_file)
        
        # Test 1: Unicode
        try:
            img_u = Image.new("RGB", (1000, 400), BG_COLOR)
            draw_u = ImageDraw.Draw(img_u)
            font_u = ImageFont.truetype(font_path, 180)
            norm_word = GurmukhiProcessor.normalize(WORD)
            
            bbox = draw_u.textbbox((0, 0), norm_word, font=font_u)
            w, h = bbox[2]-bbox[0], bbox[3]-bbox[1]
            draw_u.text(((1000-w)//2, (400-h)//2), norm_word, font=font_u, fill=TEXT_COLOR)
            draw_u.text((20, 20), f"Unicode: {font_file}", font=ImageFont.load_default(), fill=(255,255,255))
            
            img_u.save(os.path.join(TEST_DIR, f"Battle_{font_file}_Unicode.png"))
        except Exception as e:
            print(f"Unicode failed for {font_file}: {e}")

        # Test 2: Legacy
        try:
            img_l = Image.new("RGB", (1000, 400), BG_COLOR)
            draw_l = ImageDraw.Draw(img_l)
            font_l = ImageFont.truetype(font_path, 180)
            legacy_word = GurmukhiProcessor.to_legacy_ascii(WORD)
            
            bbox = draw_l.textbbox((0, 0), legacy_word, font=font_l)
            w, h = bbox[2]-bbox[0], bbox[3]-bbox[1]
            draw_l.text(((1000-w)//2, (400-h)//2), legacy_word, font=font_l, fill=TEXT_COLOR)
            draw_l.text((20, 20), f"Legacy: {font_file}", font=ImageFont.load_default(), fill=(255,255,255))
            
            img_l.save(os.path.join(TEST_DIR, f"Battle_{font_file}_Legacy.png"))
        except Exception as e:
            print(f"Legacy failed for {font_file}: {e}")

    print(f"Comparison images generated in {TEST_DIR}")

if __name__ == "__main__":
    generate_font_comparison()
