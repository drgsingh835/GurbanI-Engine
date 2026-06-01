from PIL import Image
import os

def crop_thumbnail(input_path, output_path):
    # Load the Canva capture
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found")
        return

    img = Image.open(input_path)
    # The design area in the 1280x665 capture is centered.
    # Coordinates for the 16:9 design area (estimated based on Canva layout)
    # Canva designs usually sit in the middle of the editor.
    # Left: ~356, Top: ~322, Right: ~923, Bottom: ~641 (approx for the canvas)
    # Actually, looking at the screenshot, the design is the large central landscape.
    
    # Precise Crop for the Design Canvas only
    # Based on the verification screenshot:
    left = 356
    top = 322
    right = 923
    bottom = 641
    
    # Wait, the 1280x665 is the viewport. Let's adjust to get the cleanest look.
    # I will perform a slightly larger crop and then refine.
    # Or, I'll just use the full capture if the user is okay, but a crop is better.
    
    # Let's try to crop the exact landscape area:
    cropped = img.crop((left, top, right, bottom))
    cropped = cropped.resize((1280, 720), Image.LANCZOS) # Upscale to standard HD
    
    cropped.save(output_path, "PNG")
    print(f"Clean master thumbnail saved to: {output_path}")

if __name__ == "__main__":
    src = r"C:\Users\gsing\.gemini\antigravity\brain\39e5852a-b4b4-4c25-8798-7f09b805741b\canva_design_pg002_final_1778612182707.png"
    dest = r"f:\Punjabi_Guftar_Workspace\03_Visual_Laboratory\01_Thumbnails\PG-002_Master_Thumbnail.png"
    crop_thumbnail(src, dest)
