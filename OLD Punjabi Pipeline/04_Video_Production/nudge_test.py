import os
from PIL import Image, ImageDraw, ImageFont
from Gurmukhi_Processor import GurmukhiProcessor

# Configuration
FONT_PATH = r"f:\Punjabi_Guftar_Workspace\00_Standard_Assets\04_Fonts\AmrLipiHeavy.ttf"
BG_COLOR = (18, 18, 18)
TEXT_COLOR = (212, 175, 55)
CANVAS_SIZE = (1200, 600)

def render_with_nudge(text, nudge_x=0, nudge_y=0, output_path="nudge.png"):
    ascii_text = GurmukhiProcessor.to_legacy_ascii(text)
    print(f"ASCII: {ascii_text}")
    
    img = Image.new("RGB", CANVAS_SIZE, BG_COLOR)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, 250)
    
    # We want to find '®' and nudge it
    # For AmrLipi, '®' is the pair-rara
    parts = ascii_text.split('®')
    
    current_x = 100
    y_pos = 150
    
    # 1. Draw prefix
    prefix = parts[0]
    draw.text((current_x, y_pos), prefix, font=font, fill=TEXT_COLOR)
    
    # Calculate width of prefix to position the nudge
    bbox = draw.textbbox((current_x, y_pos), prefix, font=font)
    prefix_w = bbox[2] - current_x
    
    # 2. Draw the '®' (Pair Rara) with nudge
    nudge_char = '®'
    # The pair-rara usually overlaps the previous character. 
    # By default it has its own offset. We add ours.
    draw.text((current_x + prefix_w + nudge_x, y_pos + nudge_y), nudge_char, font=font, fill=TEXT_COLOR)
    
    # 3. Draw the suffix
    # We need to know where the '®' would have ended to place the suffix correctly
    # But usually, vowels after pair-rara are also sensitive.
    if len(parts) > 1:
        suffix = parts[1]
        # In legacy fonts, the pair-rara often has ZERO width (it just hangs)
        # So we place the suffix as if '®' wasn't there, or based on the consonant width.
        draw.text((current_x + prefix_w, y_pos), suffix, font=font, fill=TEXT_COLOR)

    img.save(output_path)
    print(f"Saved: {output_path}")

if __name__ == "__main__":
    test_dir = r"f:\Punjabi_Guftar_Workspace\03_Visual_Laboratory\05_Tests"
    os.makedirs(test_dir, exist_ok=True)
    
    word = "ਸਬਸਕ੍ਰਾਈਬ"
    
    # Try different nudges
    render_with_nudge(word, nudge_x=-10, nudge_y=5, output_path=os.path.join(test_dir, "Nudge_M10_P5.png"))
    render_with_nudge(word, nudge_x=-20, nudge_y=10, output_path=os.path.join(test_dir, "Nudge_M20_P10.png"))
    render_with_nudge(word, nudge_x=-30, nudge_y=15, output_path=os.path.join(test_dir, "Nudge_M30_P15.png"))
