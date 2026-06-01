import os
import re
import json
import sys

# Add current folder to path to load gurmukhi_processor
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from utils.gurmukhi_processor import GurmukhiProcessor
except ImportError:
    class GurmukhiProcessor:
        @staticmethod
        def is_punjabi(t): return False
        @staticmethod
        def normalize(t): return t
        @staticmethod
        def to_legacy_ascii(t): return t

def preprocess_script(file_path):
    """
    Reads a script file (Markdown), normalizes all Punjabi text,
    and extracts key terms for side-car metadata.
    """
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        return False

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
        }

    # 3. Save Normalized Script (overwrite original script to normalize inline)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(normalized_content)
    
    # 4. Save Metadata JSON for automated tools
    base, _ = os.path.splitext(file_path)
    metadata_path = f"{base}_Metadata.json"
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    print(f"[+] Script preprocessed successfully!")
    print(f"[+] Script normalized in place: {file_path}")
    print(f"[+] Glossary metadata JSON saved to: {metadata_path}")
    print(f"[+] Extracted {len(punjabi_terms)} unique Punjabi terms.")
    return True

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Gurmukhi Script Preprocessor")
    parser.add_argument("script_path", help="Path to the script markdown file")
    args = parser.parse_args()
    preprocess_script(args.script_path)
