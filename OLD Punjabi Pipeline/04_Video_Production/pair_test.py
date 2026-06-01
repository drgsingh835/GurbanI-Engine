import os
from PIL import Image, ImageDraw, ImageFont
from Gurmukhi_Processor import GurmukhiProcessor

# Configuration
FONT_PATH = r"f:\Punjabi_Guftar_Workspace\00_Standard_Assets\04_Fonts\AmrLipiHeavy.ttf"
BG_COLOR = (18, 18, 18)
TEXT_COLOR = (212, 175, 55)
CANVAS_SIZE = (1200, 400)

def render_test(word, output_path):
    ascii_text = GurmukhiProcessor.to_legacy_ascii(word)
    print(f"{word} -> {ascii_text}")
    
    img = Image.new("RGB", CANVAS_SIZE, BG_COLOR)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, 180)
    
    # Just standard rendering first to see if they need nudging
    draw.text((100, 100), f"{word}: {ascii_text}", font=font, fill=TEXT_COLOR)
    img.save(output_path)

if __name__ == "__main__":
    test_dir = r"f:\Punjabi_Guftar_Workspace\03_Visual_Laboratory\05_Tests"
    os.makedirs(test_dir, exist_ok=True)
    
    # Test cases for common pair letters
    render_test("ਪੜ੍ਹ", os.path.join(test_dir, "Pair_Haha_Test.png"))
    render_test("ਸ੍ਵੈ", os.path.join(test_dir, "Pair_Vava_Test.png"))
    render_test("ਪ੍ਰੇਮ", os.path.join(test_dir, "Pair_Rara_Test_2.png"))
    render_test("ਵਿਦ੍ਯਾ", os.path.join(test_dir, "Pair_Yaya_Test.png"))
