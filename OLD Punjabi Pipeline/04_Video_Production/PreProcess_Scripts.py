import os
import re
import json
from Gurmukhi_Processor import GurmukhiProcessor

def preprocess_script(file_path):
    """
    Reads a script file (Markdown), normalizes all Punjabi text,
    and extracts key terms for side-car metadata.
    """
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Normalize the entire content
    normalized_content = GurmukhiProcessor.normalize(content)

    # 2. Extract Punjabi terms (heuristic: words containing Gurmukhi characters)
    # Gurmukhi Unicode range: \u0a00-\u0a7f
    punjabi_terms = set(re.findall(r'[\u0a00-\u0a7f]+', normalized_content))
    
    metadata = {}
    for term in sorted(list(punjabi_terms)):
        metadata[term] = {
            "normalized": term,
            "legacy_ascii": GurmukhiProcessor.to_legacy_ascii(term),
            # Transliteration can be added here if needed by extending GurmukhiProcessor
        }

    # 3. Save Normalized Script
    base, ext = os.path.splitext(file_path)
    normalized_path = f"{base}_Normalized{ext}"
    with open(normalized_path, 'w', encoding='utf-8') as f:
        f.write(normalized_content)
    
    # 4. Save Metadata JSON for automated tools
    metadata_path = f"{base}_Metadata.json"
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    print(f"Success!")
    print(f"Normalized script saved to: {normalized_path}")
    print(f"Metadata JSON saved to: {metadata_path}")
    print(f"Extracted {len(punjabi_terms)} unique Punjabi terms.")

if __name__ == "__main__":
    script_path = r"f:\Punjabi_Guftar_Workspace\02_Scripting_Bay\01_Active_Drafts\PG003_Script_Master.md"
    preprocess_script(script_path)
