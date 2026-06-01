import os
from PIL import Image, ImageDraw, ImageFont

WORKSPACE_DIR = r"F:\Punjabi_Guftar_Workspace"
OUTPUT_DIR = os.path.join(WORKSPACE_DIR, "05_Video_Production_Plant", "03_Rough_Cuts")
FONT_PATH = "nirmala.ttf" # The Gurmukhi font we downloaded

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def create_flashcard():
    # 1. Create a clean 1920x1080 Canvas (Solid Dark Academic Blue/Charcoal)
    width, height = 1920, 1080
    bg_color = (20, 22, 26) # Very dark slate grey
    image = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(image)
    
    # Optional: Draw a subtle, premium gold border
    border_color = (218, 165, 32) # Goldenrod
    border_width = 4
    draw.rectangle(
        [(80, 80), (width - 80, height - 80)],
        outline=border_color, width=border_width
    )
    
    try:
        # Load fonts at different sizes for hierarchy
        title_font = ImageFont.truetype(FONT_PATH, 90)
        main_font = ImageFont.truetype(FONT_PATH, 280)
        # Use standard Arial for English text so it doesn't render as boxes
        sub_font = ImageFont.truetype("arial.ttf", 60)
    except IOError:
        print("Error: Could not load fonts.")
        return

    # Text to display based on our Script's 'Mukh Varg' section
    title_text = "ਪੈਂਤੀ ਅੱਖਰ: ਮੁੱਖ ਵਰਗ"
    main_text = "ੳ  ਅ  ੲ  ਸ  ਹ"
    sub_text = "The Foundation Letters (Neutral Tongue Position)"
    
    # 2. Draw Title (Top Center)
    try:
        bbox = draw.textbbox((0, 0), title_text, font=title_font)
        t_w = bbox[2] - bbox[0]
    except AttributeError:
        t_w, _ = draw.textsize(title_text, font=title_font)
        
    draw.text(((width - t_w) / 2, 200), title_text, font=title_font, fill=(220, 220, 220))
    
    # 3. Draw Main Gurmukhi Letters (Center, Gold)
    try:
        bbox = draw.textbbox((0, 0), main_text, font=main_font)
        m_w = bbox[2] - bbox[0]
    except AttributeError:
        m_w, _ = draw.textsize(main_text, font=main_font)
        
    draw.text(((width - m_w) / 2, 380), main_text, font=main_font, fill=(255, 215, 0))
    
    # 4. Draw English/Context Subtext (Bottom Center)
    try:
        bbox = draw.textbbox((0, 0), sub_text, font=sub_font)
        s_w = bbox[2] - bbox[0]
    except AttributeError:
        s_w, _ = draw.textsize(sub_text, font=sub_font)
        
    draw.text(((width - s_w) / 2, 800), sub_text, font=sub_font, fill=(150, 150, 150))
    
    # Save the Flash Card
    output_path = os.path.join(OUTPUT_DIR, "flashcard_sample.png")
    image.save(output_path)
    print(f"Flashcard successfully generated: {output_path}")

if __name__ == "__main__":
    create_flashcard()
