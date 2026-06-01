import os
import sys
import argparse
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Setup paths to import GurmukhiProcessor
WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(WORKSPACE_DIR, "03-scripts"))
try:
    from utils.gurmukhi_processor import GurmukhiProcessor
except ImportError:
    class GurmukhiProcessor:
        @staticmethod
        def is_punjabi(t): return False
        @staticmethod
        def to_legacy_ascii(t): return t

def create_premium_thumbnail(bg_path, title_punjabi, subtitle_english, output_path):
    """
    Generates a high-end YouTube thumbnail with Gurmukhi typography.
    """
    # 1. Load Background
    if bg_path and os.path.exists(bg_path):
        try:
            img = Image.open(bg_path).convert("RGBA")
            print(f"[+] Loaded background from: {bg_path}")
        except Exception as e:
            print(f"[!] Error reading background {bg_path}: {e}. Creating fallback charcoal background.")
            img = Image.new('RGBA', (1280, 720), (11, 14, 20, 255))
    else:
        print("[*] No background specified or found. Creating a solid charcoal background.")
        img = Image.new('RGBA', (1280, 720), (11, 14, 20, 255))

    # Resize/crop to 1280x720 (standard 16:9 thumbnail)
    w, h = img.size
    if w != 1280 or h != 720:
        # Crop center to match 16:9
        target_ratio = 16.0 / 9.0
        current_ratio = float(w) / h
        if current_ratio > target_ratio:
            new_w = int(h * target_ratio)
            left = (w - new_w) // 2
            img = img.crop((left, 0, left + new_w, h))
        else:
            new_h = int(w / target_ratio)
            top = (h - new_h) // 2
            img = img.crop((0, top, w, top + new_h))
        img = img.resize((1280, 720), Image.Resampling.LANCZOS)

    # 2. Apply a dark vignette/overlay for contrast
    vignette = Image.new('RGBA', (1280, 720), (0, 0, 0, 150))
    img = Image.alpha_composite(img, vignette)
    draw = ImageDraw.Draw(img)

    # 3. Setup Fonts
    font_path_amr = os.path.normpath(os.path.join(WORKSPACE_DIR, "04-assets", "fonts", "AmrLipiHeavy.ttf"))
    font_path_nirmala = os.path.normpath(os.path.join(WORKSPACE_DIR, "04-assets", "fonts", "Nirmala.ttc"))
    
    # Try AmrLipiHeavy, fallback to Nirmala or arial
    font_main = None
    use_legacy = False
    
    if os.path.exists(font_path_amr):
        try:
            font_main = ImageFont.truetype(font_path_amr, 110)
            font_brand = ImageFont.truetype(font_path_amr, 35)
            use_legacy = True
            print("[+] Using AmrLipiHeavy font (legacy ASCII conversion enabled)")
        except Exception as e:
            print(f"[!] Warning: Could not load AmrLipiHeavy ({e})")
            
    if not font_main and os.path.exists(font_path_nirmala):
        try:
            font_main = ImageFont.truetype(font_path_nirmala, 100)
            font_brand = ImageFont.truetype(font_path_nirmala, 35)
            print("[+] Using Nirmala font (Unicode native)")
        except Exception as e:
            print(f"[!] Warning: Could not load Nirmala ({e})")
            
    if not font_main:
        print("[!] No Gurmukhi fonts found. Falling back to default system fonts.")
        font_main = ImageFont.load_default()
        font_brand = ImageFont.load_default()

    # Load English fonts
    try:
        font_sub = ImageFont.truetype("arial.ttf", 45)
    except:
        font_sub = ImageFont.load_default()

    # 4. Draw Brand Identity (Bottom Right)
    brand_text_punjabi = "ਪੰਜਾਬੀ ਗੁਫ਼ਤਾਰ"
    brand_text_english = " | Punjabi Guftar"
    
    if use_legacy:
        brand_p_proc = GurmukhiProcessor.to_legacy_ascii(brand_text_punjabi)
        brand_e_proc = brand_text_english
    else:
        brand_p_proc = brand_text_punjabi
        brand_e_proc = brand_text_english
        
    try:
        bbox_p = draw.textbbox((0, 0), brand_p_proc, font=font_brand)
        wp = bbox_p[2] - bbox_p[0]
        bbox_e = draw.textbbox((0, 0), brand_e_proc, font=font_sub)
        we = bbox_e[2] - bbox_e[0]
        
        total_brand_w = wp + we
        brand_x = 1280 - total_brand_w - 60
        brand_y = 720 - 70
        
        draw.text((brand_x, brand_y), brand_p_proc, font=font_brand, fill=(200, 200, 200, 200))
        draw.text((brand_x + wp, brand_y + 5), brand_e_proc, font=font_sub, fill=(180, 180, 180, 150))
    except Exception as e:
        print(f"[!] Error drawing brand text: {e}")

    # 5. Draw Title (Center-Left)
    title_processed = GurmukhiProcessor.to_legacy_ascii(title_punjabi) if use_legacy else title_punjabi
    
    # Shadow for Title (Offset 5,5)
    draw.text((85, 205), title_processed, font=font_main, fill=(0, 0, 0, 255))
    # Main Title (Gold)
    gold_color = (255, 215, 0, 255) # Premium Gold
    draw.text((80, 200), title_processed, font=font_main, fill=gold_color)
    
    # 6. Draw Subtitle (English)
    if subtitle_english:
        draw.text((80, 360), subtitle_english, font=font_sub, fill=(230, 230, 230, 255))
    
    # 7. Add a premium gold accent line
    draw.line([(80, 345), (600, 345)], fill=(218, 165, 32, 255), width=6)

    # 8. Save
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img = img.convert('RGB')
    img.save(output_path, "JPEG", quality=95)
    print(f"[+] Thumbnail compiled successfully! Saved to: {output_path}")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gurbani Creative Premium Thumbnail Generator")
    parser.add_argument("--id", default="gurbani_01", help="Target Concept ID")
    parser.add_argument("--title_pa", default="ਦਰਦ ਹੀ ਦਾਰੂ ਹੈ", help="Punjabi/Gurmukhi Title text")
    parser.add_argument("--subtitle_en", default="Pain is the Medicine", help="English Subtitle text")
    parser.add_argument("--bg", default=None, help="Path to custom background image")
    args = parser.parse_args()

    # Determine default paths
    output_file = os.path.join(WORKSPACE_DIR, "05-outputs", "final_reels", f"{args.id}_thumbnail.jpg")
    
    bg_img = args.bg
    if not bg_img:
        # Fallback 1: check generated images folder
        gen_dir = os.path.join(WORKSPACE_DIR, "04-assets", "generated_images", args.id)
        if os.path.exists(gen_dir):
            shots = [f for f in os.listdir(gen_dir) if f.endswith(".png")]
            if shots:
                bg_img = os.path.join(gen_dir, sorted(shots)[0]) # use shot-01
        
        # Fallback 2: check if there's any file under standard assets (e.g. check for ancient manuscript)
        if not bg_img or not os.path.exists(bg_img):
            manuscript = os.path.join(WORKSPACE_DIR, "04-assets", "standard_assets", "03_Visual_Laboratory", "03_Background_Media", "03_ancient_manuscript.png")
            if os.path.exists(manuscript):
                bg_img = manuscript

    create_premium_thumbnail(bg_img, args.title_pa, args.subtitle_en, output_file)
