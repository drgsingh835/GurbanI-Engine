import os
from PIL import Image, ImageDraw, ImageFont

WORKSPACE_DIR = r"F:\Punjabi_Guftar_Workspace"
OUTPUT_DIR = os.path.join(WORKSPACE_DIR, "03_Visual_Laboratory", "03_Background_Media")
FONT_PATH = r"C:\Windows\Fonts\Nirmala.ttc" 

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Defining the 5 exact flashcards based on our script structure
cards = [
    {
        "filename": "fc_01_intro.png",
        "title": "ਪੰਜਾਬੀ ਗੁਫ਼ਤਾਰ",
        "main": "ਪੈਂਤੀ ਅੱਖਰ",
        "sub": "The Science of the Gurmukhi Script"
    },
    {
        "filename": "fc_02_mukh_varg.png",
        "title": "ਮੁੱਖ ਵਰਗ",
        "main": "ੳ  ਅ  ੲ  ਸ  ਹ",
        "sub": "The Foundation Letters"
    },
    {
        "filename": "fc_03_kavarg.png",
        "title": "ਕਵਰਗ",
        "main": "ਕ  ਖ  ਗ  ਘ  ਙ",
        "sub": "The Throat Letters (Larynx)"
    },
    {
        "filename": "fc_04_progression.png",
        "title": "ਪਵਰਗ",
        "main": "ਪ  ਫ  ਬ  ਭ  ਮ",
        "sub": "The Lips (Phonetic Progression)"
    },
    {
        "filename": "fc_05_conclusion.png",
        "title": "ਪੰਜਾਬੀ ਗੁਫ਼ਤਾਰ",
        "main": "ਸਬਸਕ੍ਰਾਈਬ",
        "sub": "Preserve & Study Our Mother Tongue"
    }
]

def generate_flashcards():
    width, height = 1920, 1080
    bg_color = (20, 22, 26) 
    border_color = (218, 165, 32)
    border_width = 4
    
    try:
        title_font = ImageFont.truetype(FONT_PATH, 90)
        main_font = ImageFont.truetype(FONT_PATH, 250)
        sub_font = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 60)
    except IOError:
        print("Error loading fonts.")
        return

    print("Generating Academic Flash Cards...")
    for card in cards:
        image = Image.new("RGB", (width, height), bg_color)
        draw = ImageDraw.Draw(image)
        
        # Draw Border
        draw.rectangle(
            [(80, 80), (width - 80, height - 80)],
            outline=border_color, width=border_width
        )
        
        # Draw Title
        try:
            bbox = draw.textbbox((0, 0), card["title"], font=title_font)
            t_w = bbox[2] - bbox[0]
        except AttributeError:
            t_w, _ = draw.textsize(card["title"], font=title_font)
        draw.text(((width - t_w) / 2, 200), card["title"], font=title_font, fill=(220, 220, 220))
        
        # Draw Main Gurmukhi
        try:
            bbox = draw.textbbox((0, 0), card["main"], font=main_font)
            m_w = bbox[2] - bbox[0]
        except AttributeError:
            m_w, _ = draw.textsize(card["main"], font=main_font)
        draw.text(((width - m_w) / 2, 400), card["main"], font=main_font, fill=(255, 215, 0))
        
        # Draw Sub English
        try:
            bbox = draw.textbbox((0, 0), card["sub"], font=sub_font)
            s_w = bbox[2] - bbox[0]
        except AttributeError:
            s_w, _ = draw.textsize(card["sub"], font=sub_font)
        draw.text(((width - s_w) / 2, 800), card["sub"], font=sub_font, fill=(150, 150, 150))
        
        output_path = os.path.join(OUTPUT_DIR, card["filename"])
        image.save(output_path)
        print(f"Generated: {card['filename']}")
        
    print("\nAll 5 Flashcards Generated Successfully!")

if __name__ == "__main__":
    generate_flashcards()
