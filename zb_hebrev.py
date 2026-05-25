import os
import re

# VERSION TRACKING
SCRIPT_VERSION = "1.0.0-SentenceWordFixer"


def reverse_sentence_words(line):
    """
    Splits a line into words, reverses their sequence to fix Left-to-Right
    layout corruption, and keeps the punctuation fixed to the words.
    """
    words = line.split()
    if not words:
        return line

    # Reverse the order of the words in the list
    reversed_words = list(reversed(words))

    return " ".join(reversed_words)


def fix_existing_hebrew_files(project_root="/home/ken/Applications/python/zbpycolorscan"):
    heb_dir = os.path.join(project_root, "txt", "heb")

    if not os.path.exists(heb_dir):
        print(f"Error: Target path does not exist: {heb_dir}")
        return

    print("====================================================")
    print(f" Running Sentence Fixer | Version: {SCRIPT_VERSION}")
    print("====================================================")

    files_in_dir = os.listdir(heb_dir)
    fixed_count = 0

    print(f"Scanning directory: {heb_dir}")
    print(f"Found {len(files_in_dir)} files total. Beginning word-order correction...\n")

    for filename in files_in_dir:
        # We only target Hebrew files
        if not filename.endswith("_he.txt"):
            continue

        file_path = os.path.join(heb_dir, filename)

        # 1. Read the current reversed contents
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # 2. Process each line to flip the word positions back to normal reading order
        fixed_lines = []
        for line in lines:
            stripped = line.strip()
            if not stripped:
                fixed_lines.append("")  # Preserve empty lines/stanza breaks
            else:
                fixed_lines.append(reverse_sentence_words(stripped))

        # 3. Overwrite the file with the corrected layout
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(fixed_lines) + "\n")

        print(f" FIXED WORD ORDER: [ {filename} ]")
        fixed_count += 1

    print("====================================================")
    print(f"Batch Processing Complete!")
    print(f" -> Successfully Fixed Sentence Word Order in: {fixed_count} files")


if __name__ == "__main__":
    fix_existing_hebrew_files()