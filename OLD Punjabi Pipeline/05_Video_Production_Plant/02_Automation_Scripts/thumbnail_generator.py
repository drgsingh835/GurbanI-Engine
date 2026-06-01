import os
from PIL import Image, ImageDraw, ImageFont

# Paths
WORKSPACE_DIR = r"f:\Punjabi_Guftar_Workspace"
ASSETS_DIR = os.path.join(WORKSPACE_DIR, "03_Visual_Laboratory")
SCRIPTS_DIR = os.path.join(WORKSPACE_DIR, "05_Video_Production_Plant", "02_Automation_Scripts")
OUTPUT_DIR = os.path.join(ASSETS_DIR, "01_Thumbnails")
FONT_PATH = os.path.join(SCRIPTS_DIR, "nirmala.ttf")
BG_PATH = os.path.join(ASSETS_DIR, "03_Background_Media", "03_ancient_manuscript.png")

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def create_thumbnail(project_id, title_punjabi, subtitle_english):
    # 1. Load and prepare background
    try:
        bg = Image.open(BG_PATH)
    except FileNotFoundError:
        print(f"Background not found at {BG_PATH}. Creating a solid charcoal background.")
        bg = Image.new('RGB', (1024, 1024), (20, 22, 26))

    # Target 1280x720
    # Crop center 1024x576 from 1024x1024 (if square)
    w, h = bg.size
    if w == h:
        left = 0
        top = (h - (w * 9 // 16)) // 2
        right = w
        bottom = top + (w * 9 // 16)
        bg = bg.crop((left, top, right, bottom))
    
    bg = bg.resize((1280, 720), Image.Resampling.LANCZOS)
    
    # 2. Apply a dark vignette/overlay for contrast
    overlay = Image.new('RGBA', (1280, 720), (0, 0, 0, 160))
    bg = bg.convert('RGBA')
    bg = Image.alpha_composite(bg, overlay)
    
    draw = ImageDraw.Draw(bg)
    
    # 3. Load Fonts
    try:
        title_font = ImageFont.truetype(FONT_PATH, 110) # Gurmukhi
        sub_font = ImageFont.truetype("arial.ttf", 50) # English
        brand_font = ImageFont.truetype("arial.ttf", 40) # Mixed/English
        # Re-load brand font for Punjabi part if needed, but Nirmala usually has it.
        # Actually, let's keep brand font as Nirmala but handle English separately if needed.
        # For simplicity, let's just use Arial for English subtitles.
    except Exception as e:
        print(f"Font error: {e}. Using default.")
        title_font = ImageFont.load_default()
        sub_font = ImageFont.load_default()
        brand_font = ImageFont.load_default()

    # 4. Draw Brand Identity (Bottom Right)
    brand_text_punjabi = "ਪੰਜਾਬੀ ਗੁਫ਼ਤਾਰ"
    brand_text_english = " | Punjabi Guftar"
    
    # Measure Punjabi part
    bbox_p = draw.textbbox((0, 0), brand_text_punjabi, font=title_font) # Use Nirmala
    # Actually let's just use a smaller size of Nirmala for Brand
    brand_font_punjabi = ImageFont.truetype(FONT_PATH, 40)
    brand_font_english = ImageFont.truetype("arial.ttf", 35)
    
    bbox_p = draw.textbbox((0, 0), brand_text_punjabi, font=brand_font_punjabi)
    wp = bbox_p[2] - bbox_p[0]
    
    bbox_e = draw.textbbox((0, 0), brand_text_english, font=brand_font_english)
    we = bbox_e[2] - bbox_e[0]
    
    total_w = wp + we
    start_x = 1280 - total_w - 60
    start_y = 720 - 60
    
    draw.text((start_x, start_y), brand_text_punjabi, font=brand_font_punjabi, fill=(200, 200, 200, 200))
    draw.text((start_x + wp, start_y + 5), brand_text_english, font=brand_font_english, fill=(180, 180, 180, 200))

    # 5. Draw Title (Center-Left)
    # Shadow for Title
    draw.text((85, 205), title_punjabi, font=title_font, fill=(0, 0, 0, 255))
    # Main Title (Gold)
    draw.text((80, 200), title_punjabi, font=title_font, fill=(255, 215, 0, 255))
    
    # 6. Draw Subtitle (English)
    draw.text((80, 360), subtitle_english, font=sub_font, fill=(230, 230, 230, 255))
    
    # 7. Add a premium gold accent line
    draw.line([(80, 345), (600, 345)], fill=(218, 165, 32, 255), width=6)

    # Save
    output_path = os.path.join(OUTPUT_DIR, f"{project_id}_Auto_Thumbnail.png")
    bg = bg.convert('RGB')
    bg.save(output_path, quality=95)
    print(f"Thumbnail saved: {output_path}")

if __name__ == "__main__":
    create_thumbnail("PG-002", "ਪੈਂਤੀ ਅੱਖਰ ਦਾ ਵਿਗਿਆਨ", "The Science of 35 Letters")
