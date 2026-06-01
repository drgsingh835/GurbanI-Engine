import os
from Flashcard_Animator import create_title_card
from Gurmukhi_Processor import GurmukhiProcessor

# Create a test directory for rendering comparison
test_dir = r"f:\Punjabi_Guftar_Workspace\03_Visual_Laboratory\05_Tests"
os.makedirs(test_dir, exist_ok=True)

word = "ਸਬਸਕ੍ਰਾਈਬ"
output_path = os.path.join(test_dir, "Subscribe_Test.png")

# Generate the card using Nirmala UI
output_path_nirmala = os.path.join(test_dir, "Subscribe_Test_Nirmala.png")
create_title_card(word, "Nirmala UI Test", output_path_nirmala)

print(f"Nirmala image generated at: {output_path_nirmala}")
