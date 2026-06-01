import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from Gurmukhi_Processor import GurmukhiProcessor

# Configuration
BG_COLOR = (18, 18, 18)  # Deep Charcoal
GOLD_COLOR = (212, 175, 55)  # Metallic Gold
DIM_COLOR = (80, 80, 80)  # Dim Grey for non-active letters
FONT_PATH = r"f:\Punjabi_Guftar_Workspace\00_Standard_Assets\04_Fonts\AmrLipiHeavy.ttf"
CANVAS_SIZE = (1920, 1080)

def create_flashcard_frame(letters, highlight_idx=None, title=None, output_path="frame.png"):
    """
    Creates a 16:9 flashcard frame with a row of letters.
    """
    img = Image.new("RGB", CANVAS_SIZE, BG_COLOR)
    draw = ImageDraw.Draw(img)
    width, height = CANVAS_SIZE

    # Setup Font
    try:
        font_main = ImageFont.truetype(FONT_PATH, 280)
        font_title = ImageFont.truetype(FONT_PATH, 60)
        font_brand = ImageFont.truetype(FONT_PATH, 40)
    except Exception as e:
        print(f"Error loading font: {e}")
        return

    # Draw Title
    if title:
        legacy_title = GurmukhiProcessor.to_legacy_ascii(title)
        title_bbox = draw.textbbox((0, 0), legacy_title, font=font_title)
        title_w = title_bbox[2] - title_bbox[0]
        draw.text(((width - title_w) // 2, 80), legacy_title, font=font_title, fill=(200, 200, 200, 150))

    # Calculate Layout
    spacing = 80
    legacy_letters = [GurmukhiProcessor.to_legacy_ascii(l) for l in letters]
    letter_widths = [draw.textbbox((0, 0), l, font=font_main)[2] for l in legacy_letters]
    total_content_width = sum(letter_widths) + (len(letters) - 1) * spacing
    
    start_x = (width - total_content_width) // 2
    y_pos = (height - 280) // 2 + 50

    # Draw Letters
    current_x = start_x
    for i, char in enumerate(letters):
        is_highlighted = (i == highlight_idx)
        color = GOLD_COLOR if is_highlighted else DIM_COLOR
        legacy_char = GurmukhiProcessor.to_legacy_ascii(char)
        draw.text((current_x, y_pos), legacy_char, font=font_main, fill=color)
        char_w = draw.textbbox((0, 0), legacy_char, font=font_main)[2]
        current_x += char_w + spacing

    # Branding
    brand_legacy = GurmukhiProcessor.to_legacy_ascii("ਪੰਜਾਬੀ ਗੁਫ਼ਤਾਰ")
    draw.text((50, height - 80), brand_legacy, font=font_brand, fill=(255, 255, 255, 40))

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG")

def create_title_card(main_text, sub_text, output_path):
    img = Image.new("RGB", CANVAS_SIZE, BG_COLOR)
    draw = ImageDraw.Draw(img)
    width, height = CANVAS_SIZE
    
    font_main = ImageFont.truetype(FONT_PATH, 180)
    font_sub = ImageFont.truetype(FONT_PATH, 80)
    
    legacy_main = GurmukhiProcessor.to_legacy_ascii(main_text)
    bbox = draw.textbbox((0, 0), legacy_main, font=font_main)
    w, h = bbox[2]-bbox[0], bbox[3]-bbox[1]
    draw.text(((width - w) // 2, (height - h) // 2 - 100), legacy_main, font=font_main, fill=GOLD_COLOR)
    
    legacy_sub = GurmukhiProcessor.to_legacy_ascii(sub_text)
    bbox_s = draw.textbbox((0, 0), legacy_sub, font=font_sub)
    ws, hs = bbox_s[2]-bbox_s[0], bbox_s[3]-bbox_s[1]
    draw.text(((width - ws) // 2, (height - hs) // 2 + 100), legacy_sub, font=font_sub, fill=(255,255,255,180))
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG")

if __name__ == "__main__":
    base_dir = r"f:\Punjabi_Guftar_Workspace\03_Visual_Laboratory\04_Typography_Cards"
    
    # --- MOVEMENT 1 ---
    m1_dir = os.path.join(base_dir, "M1")
    create_title_card("ਗੁਰਮੁਖੀ: ਧੁਨੀ ਵਿਗਿਆਨ", "The Science of Phonetics", os.path.join(m1_dir, "intro.png"))
    
    mukh_varg = ["ੳ", "ਅ", "ੲ", "ਸ", "ਹ"]
    create_flashcard_frame(mukh_varg, None, "ਮੁੱਖ ਵਰਗ (Foundation)", os.path.join(m1_dir, "mukh_still.png"))
    for i in range(len(mukh_varg)):
        create_flashcard_frame(mukh_varg, i, "ਮੁੱਖ ਵਰਗ (Foundation)", os.path.join(m1_dir, f"mukh_{i}.png"))
    
    kavarg = ["ਕ", "ਖ", "ਗ", "ਘ", "ਙ"]
    create_flashcard_frame(kavarg, None, "ਕਵਰਗ (Gutturals - Throat)", os.path.join(m1_dir, "kavarg_still.png"))
    for i in range(len(kavarg)):
        create_flashcard_frame(kavarg, i, "ਕਵਰਗ (Gutturals - Throat)", os.path.join(m1_dir, f"kavarg_{i}.png"))
    
    create_title_card("ਕੰਠ (Throat)", "Phonetic Origin: Kavarg", os.path.join(m1_dir, "anatomy.png"))

    # --- MOVEMENT 2 ---
    m2_dir = os.path.join(base_dir, "M2")
    chavarg = ["ਚ", "ਛ", "ਜ", "ਝ", "ਞ"]
    create_flashcard_frame(chavarg, None, "ਚਵਰਗ (Palatal - Talva)", os.path.join(m2_dir, "chavarg_still.png"))
    for i in range(len(chavarg)):
        create_flashcard_frame(chavarg, i, "ਚਵਰਗ (Palatal - Talva)", os.path.join(m2_dir, f"chavarg_{i}.png"))
        
    tavarg_r = ["ਟ", "ਠ", "ਡ", "ਢ", "ਣ"]
    create_flashcard_frame(tavarg_r, None, "ਟਵਰਗ (Retroflex - Murda)", os.path.join(m2_dir, "tavarg_r_still.png"))
    for i in range(len(tavarg_r)):
        create_flashcard_frame(tavarg_r, i, "ਟਵਰਗ (Retroflex - Murda)", os.path.join(m2_dir, f"tavarg_r_{i}.png"))
        
    tavarg_d = ["ਤ", "ਥ", "ਦ", "ਧ", "ਨ"]
    create_flashcard_frame(tavarg_d, None, "ਤਵਰਗ (Dental - Dand)", os.path.join(m2_dir, "tavarg_d_still.png"))
    for i in range(len(tavarg_d)):
        create_flashcard_frame(tavarg_d, i, "ਤਵਰਗ (Dental - Dand)", os.path.join(m2_dir, f"tavarg_d_{i}.png"))

    # --- MOVEMENT 3 ---
    m3_dir = os.path.join(base_dir, "M3")
    pavarg = ["ਪ", "ਫ", "ਬ", "ਭ", "ਮ"]
    create_flashcard_frame(pavarg, None, "ਪਵਰਗ (Labial - Lips)", os.path.join(m3_dir, "pavarg_still.png"))
    for i in range(len(pavarg)):
        create_flashcard_frame(pavarg, i, "ਪਵਰਗ (Labial - Lips)", os.path.join(m3_dir, f"pavarg_{i}.png"))
        
    antam = ["ਯ", "ਰ", "ਲ", "ਵਾ", "ੜ"]
    create_flashcard_frame(antam, None, "ਅੰਤਮ ਵਰਗ (Final)", os.path.join(m3_dir, "antam_still.png"))
    for i in range(len(antam)):
        create_flashcard_frame(antam, i, "ਅੰਤਮ ਵਰਗ (Final)", os.path.join(m3_dir, f"antam_{i}.png"))
        
    naveen = ["ਸ਼", "ਖ਼", "ਗ਼", "ਜ਼", "ਫ਼", "ਲ਼"]
    create_flashcard_frame(naveen, None, "ਨਵੀਨ ਵਰਗ (Modern/Persian)", os.path.join(m3_dir, "naveen_still.png"))
    for i in range(len(naveen)):
        create_flashcard_frame(naveen, i, "ਨਵੀਨ ਵਰਗ (Modern/Persian)", os.path.join(m3_dir, f"naveen_{i}.png"))

    create_title_card("ਪੰਜਾਬੀ ਗੁਫ਼ਤਾਰ", "Subscribe for more Linguistic Science", os.path.join(m3_dir, "outro.png"))

    print("All frames (including still cards) generated successfully.")

