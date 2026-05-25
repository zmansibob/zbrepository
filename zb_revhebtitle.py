import os

# VERSION TRACKING
SCRIPT_VERSION = "1.0.0-TitleOnlyWordFixer"


def reverse_line_words(line):
    """Splits a line into words, reverses their sequence, and rejoins them."""
    words = line.split()
    if not words:
        return line
    return " ".join(reversed(words))


def fix_hebrew_titles(project_root="/home/ken/Applications/python/zbpycolorscan"):
    heb_dir = os.path.join(project_root, "txt", "heb")

    if not os.path.exists(heb_dir):
        print(f"Error: Target path does not exist: {heb_dir}")
        return

    print("====================================================")
    print(f" Running Title Fixer | Version: {SCRIPT_VERSION}")
    print("====================================================")

    files_in_dir = os.listdir(heb_dir)
    fixed_count = 0

    print(f"Scanning directory: {heb_dir}")
    print(f"Found {len(files_in_dir)} files total. Fixing title lines...\n")

    for filename in files_in_dir:
        # Target only Hebrew lyric files
        if not filename.endswith("_he.txt"):
            continue

        file_path = os.path.join(heb_dir, filename)

        # 1. Read all lines from the file
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        if not lines:
            continue

        # 2. Extract and reverse only the very first line (the title)
        original_title = lines[0].strip()
        if original_title:
            fixed_title = reverse_line_words(original_title)
            lines[0] = fixed_title + "\n"

        # 3. Save the modified contents back to the file
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(lines)

        print(f" FIXED TITLE: [ {filename} ] -> New Title: {fixed_title}")
        fixed_count += 1

    print("====================================================")
    print(f"Batch Processing Complete!")
    print(f" -> Successfully Fixed Titles in: {fixed_count} files")


if __name__ == "__main__":
    fix_hebrew_titles()