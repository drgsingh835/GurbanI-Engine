import os
from PIL import Image, ImageDraw, ImageFont
from Gurmukhi_Processor import GurmukhiProcessor

# Configuration
FONT_PATH = r"f:\Punjabi_Guftar_Workspace\00_Standard_Assets\04_Fonts\AmrLipiHeavy.ttf"
BG_COLOR = (18, 18, 18)
TEXT_COLOR = (212, 175, 55)
CANVAS_SIZE = (1200, 800)

def test_words(words, output_path):
    img = Image.new("RGB", CANVAS_SIZE, BG_COLOR)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, 180)
    
    y_pos = 100
    for word in words:
        GurmukhiProcessor.render_perfect_text(draw, (100, y_pos), word, font, TEXT_COLOR)
        y_pos += 200

    img.save(output_path)
    print(f"Test generated: {output_path}")

if __name__ == "__main__":
    test_dir = r"f:\Punjabi_Guftar_Workspace\03_Visual_Laboratory\05_Tests"
    os.makedirs(test_dir, exist_ok=True)
    
    words_to_test = ["ਬ੍ਰਾਈਬ", "ਟ੍ਰਾਈਬ", "ਫ੍ਰਾਈਡ"]
    output = os.path.join(test_dir, "Multi_Consonant_Rara_Test.png")
    test_words(words_to_test, output)
