import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from Gurmukhi_Processor import GurmukhiProcessor

def create_premium_thumbnail(bg_path, text, output_path, font_path=r"f:\Punjabi_Guftar_Workspace\00_Standard_Assets\04_Fonts\AmrLipiHeavy.ttf"):
    """
    Generates a high-end YouTube thumbnail with Gurmukhi typography.
    """
    # 1. Load Background
    if not os.path.exists(bg_path):
        print(f"Error: Background {bg_path} not found.")
        return

    img = Image.open(bg_path).convert("RGBA")
    draw = ImageDraw.Draw(img)
    width, height = img.size

    # 2. Setup Font
    try:
        font_main = ImageFont.truetype(font_path, 140)
        font_sub = ImageFont.truetype(font_path, 40)
    except Exception as e:
        print(f"Error loading font: {e}")
        return

    # 3. Calculate Layout (Legacy conversion for standard draw.text)
    legacy_text = GurmukhiProcessor.to_legacy_ascii(text)
    bbox = draw.textbbox((0, 0), legacy_text, font=font_main)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    pos = ((width - text_w) // 2, (height - text_h) // 2 - 50)

    # 4. Main Text (Default Font Rendering)
    text_color = (197, 160, 89, 255) # Premium Gold
    draw.text(pos, legacy_text, font=font_main, fill=text_color)

    # 5. Add Branding
    brand_text = "ਪੰਜਾਬੀ ਗੁਫ਼ਤਾਰ | Punjabi Guftar"
    brand_legacy = GurmukhiProcessor.to_legacy_ascii(brand_text)
    brand_bbox = draw.textbbox((0, 0), brand_legacy, font=font_sub)
    brand_pos = (width - (brand_bbox[2]-brand_bbox[0]) - 50, height - 80)
    draw.text(brand_pos, brand_legacy, font=font_sub, fill=(255, 255, 255, 100))

    # 6. Save
    img = img.convert("RGB")
    img.save(output_path, "JPEG", quality=95)

if __name__ == "__main__":
    # Test Run for PG-002
    bg = r"C:\Users\gsing\.gemini\antigravity\brain\39e5852a-b4b4-4c25-8798-7f09b805741b\punjabi_guftar_thumbnail_base_1778610377334.png"
    output = r"f:\Punjabi_Guftar_Workspace\03_Visual_Laboratory\01_Thumbnails\PG-002_Thumbnail.jpg"
    title = "ਪੈਂਤੀ ਅੱਖਰ ਦਾ ਵਿਗਿਆਨ"
    
    os.makedirs(os.path.dirname(output), exist_ok=True)
    create_premium_thumbnail(bg, title, output)

