import os
from PIL import Image, ImageDraw, ImageFont
from Gurmukhi_Processor import GurmukhiProcessor

# Configuration
FONT_PATH = r"f:\Punjabi_Guftar_Workspace\00_Standard_Assets\04_Fonts\AmrLipiHeavy.ttf"
BG_COLOR = (18, 18, 18)
TEXT_COLOR = (212, 175, 55)
CANVAS_SIZE = (1200, 800)

def test_offsets(word, offsets, output_path):
    img = Image.new("RGB", CANVAS_SIZE, BG_COLOR)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, 180)
    
    y_pos = 100
    for offset in offsets:
        # Manually override the logic for this test to show different offsets
        ascii_text = GurmukhiProcessor.to_legacy_ascii(word)
        current_x = 100
        
        # Render first char (Consonant)
        char = ascii_text[0]
        draw.text((current_x, y_pos), char, font=font, fill=TEXT_COLOR)
        
        # Render second char (Pair Rara) with the specific offset
        pair_char = ascii_text[1]
        draw.text((current_x + offset, y_pos), pair_char, font=font, fill=TEXT_COLOR)
        
        # Render the rest
        bbox = draw.textbbox((current_x, y_pos), char, font=font)
        draw.text((current_x + (bbox[2]-current_x), y_pos), ascii_text[2:], font=font, fill=TEXT_COLOR)
        
        draw.text((800, y_pos), f"Offset: {offset}", font=ImageFont.load_default(), fill=(255,255,255))
        y_pos += 150

    img.save(output_path)

if __name__ == "__main__":
    test_dir = r"f:\Punjabi_Guftar_Workspace\03_Visual_Laboratory\05_Tests"
    os.makedirs(test_dir, exist_ok=True)
    
    word = "ਬ੍ਰਾਈਬ"
    offsets = [60, 80, 100, 120, 140]
    output = os.path.join(test_dir, "Offset_Comparison_Bribe.png")
    test_offsets(word, offsets, output)
