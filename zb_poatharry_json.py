import os
import json

HEB_PATH = "txt/heb"
ENG_PATH = "txt/eng"

catalog = []

# Process English directory
if os.path.exists(ENG_PATH):
    for filename in os.listdir(ENG_PATH):
        if filename.endswith("_en.txt"):
            file_path = os.path.join(ENG_PATH, filename)

            title = ""
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    first_line = f.readline().strip()
                    if first_line:
                        title = first_line
            except Exception as e:
                print(f"Error reading first line of {filename}: {e}")

            if not title:
                title = filename[:-7].replace("_", " ").strip()

            catalog.append({
                "title": title,
                "path": f"{ENG_PATH}/{filename}",
                "lang": "en"
            })

# Process Hebrew directory
if os.path.exists(HEB_PATH):
    for filename in os.listdir(HEB_PATH):
        if filename.endswith("_he.txt"):
            file_path = os.path.join(HEB_PATH, filename)

            title = ""
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    first_line = f.readline().strip()
                    if first_line:
                        title = first_line
            except Exception as e:
                print(f"Error reading first line of {filename}: {e}")

            if not title:
                title = filename[:-7].replace("_", " ").strip()

            catalog.append({
                "title": title,
                "path": f"{HEB_PATH}/{filename}",
                "lang": "he"
            })

# Write out the JSON map
with open("zb_poatharry.json", "w", encoding="utf-8") as f:
    json.dump(catalog, f, ensure_ascii=False, indent=4)

print(f"Success! Created zb_poatharry.json with {len(catalog)} items using internal text titles.")