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
    
    img = Image.new("RGB", CANVAS_SIZE, BG_COLOR)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, 250)
    
    parts = ascii_text.split('®')
    current_x = 100
    y_pos = 150
    
    # 1. Draw prefix
    prefix = parts[0]
    draw.text((current_x, y_pos), prefix, font=font, fill=TEXT_COLOR)
    
    # Calculate width
    bbox = draw.textbbox((current_x, y_pos), prefix, font=font)
    prefix_w = bbox[2] - current_x
    
    # 2. Draw the '®' (Pair Rara) with nudge
    draw.text((current_x + prefix_w + nudge_x, y_pos + nudge_y), '®', font=font, fill=TEXT_COLOR)
    
    # 3. Draw the suffix
    if len(parts) > 1:
        suffix = parts[1]
        draw.text((current_x + prefix_w, y_pos), suffix, font=font, fill=TEXT_COLOR)

    img.save(output_path)

if __name__ == "__main__":
    test_dir = r"f:\Punjabi_Guftar_Workspace\03_Visual_Laboratory\05_Tests"
    os.makedirs(test_dir, exist_ok=True)
    
    word = "ਸਬਸਕ੍ਰਾਈਬ"
    
    # Moving further right (35-45) and upwards (y decreasing from 15)
    render_with_nudge(word, nudge_x=35, nudge_y=10, output_path=os.path.join(test_dir, "Nudge_35x_10y.png"))
    render_with_nudge(word, nudge_x=40, nudge_y=5, output_path=os.path.join(test_dir, "Nudge_40x_5y.png"))
    render_with_nudge(word, nudge_x=45, nudge_y=0, output_path=os.path.join(test_dir, "Nudge_45x_0y.png"))
