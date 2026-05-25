import os
import json
import re

TXT_ROOT = "/home/ken/Applications/python/zbpycolorscan/txt"
HEB_PATH = os.path.join(TXT_ROOT, "heb")
ENG_PATH = os.path.join(TXT_ROOT, "eng")

catalog = []


def clean_fallback_title(filename, suffix_len=7):
    """Converts a snake_case filename back into a clean, readable presentation title."""
    # Strip the suffix (e.g., '_he.txt' or '_en.txt')
    base = filename[:-suffix_len]
    # Replace underscores with spaces, replace hyphens back to colons for time/indices, and titlecase words
    clean = base.replace("_", " ").replace("-", ":").strip()
    return clean


# Process English directory
if os.path.exists(ENG_PATH):
    for filename in sorted(os.listdir(ENG_PATH)):
        if filename.endswith("_en.txt"):
            file_path = os.path.join(ENG_PATH, filename)
            title = ""

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    first_line = f.readline().strip()
                    # Verify the title isn't empty or a broken question-mark artifact
                    if first_line and not set(first_line) == {'?'}:
                        title = first_line
            except Exception as e:
                print(f"Error reading first line of {filename}: {e}")

            if not title or title.startswith("song_"):
                title = clean_fallback_title(filename, suffix_len=7)

            catalog.append({
                "title": title,
                "path": f"txt/eng/{filename}",
                "lang": "en"
            })

# Process Hebrew directory
if os.path.exists(HEB_PATH):
    for filename in sorted(os.listdir(HEB_PATH)):
        if filename.endswith("_he.txt"):
            file_path = os.path.join(HEB_PATH, filename)
            title = ""

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    first_line = f.readline().strip()
                    # Verify the line contains real characters and isn't a string of question marks
                    if first_line and not set(first_line) == {'?'}:
                        title = first_line
            except Exception as e:
                print(f"Error reading first line of {filename}: {e}")

            # If the extracted title was unreadable or a structural page fallback, use the filename map
            if not title or title.startswith("song_"):
                title = clean_fallback_title(filename, suffix_len=7)

            catalog.append({
                "title": title,
                "path": f"txt/heb/{filename}",
                "lang": "he"
            })

# Write out the completed clean JSON map
output_json = "zb_poatharry.json"
with open(output_json, "w", encoding="utf-8") as f:
    json.dump(catalog, f, ensure_ascii=False, indent=4)

print(f"Success! Created {output_json} with {len(catalog)} items using sanitized title names.")