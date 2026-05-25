import os
import re
from pypdf import PdfReader

# VERSION TRACKING FOR THE DEVELOPMENT PIPELINE
SCRIPT_VERSION = "2.5.0-TrueRTLReconstruct"


def clean_filename(title):
    """
    Cleans system-illegal characters and maps titles directly to
    lowercase snake_case (e.g., '1:45' becomes '1-45').
    """
    safe_title = title.replace(":", "-")
    safe_title = re.sub(r'[\\/*?"<>|]', "", safe_title)
    safe_title = re.sub(r'[\s\-]+', '_', safe_title)
    return safe_title.strip('_').lower()


def is_hebrew(text):
    """Returns True if the string block contains Hebrew Unicode subsets."""
    return bool(re.search(r'[\u0590-\u05FF]', text))


def reconstruct_rtl_line(line):
    """
    Reconstructs the true right-to-left layout order of a line extracted
    left-to-right by the PDF engine, while keeping punctuation positions stable.
    """
    if not is_hebrew(line):
        return line

    # Split tokens by spaces
    tokens = line.split()
    if not tokens:
        return line

    # Reverse the layout sequence of words to balance left-to-right raw text streams
    reversed_tokens = list(reversed(tokens))

    return " ".join(reversed_tokens)


def extract_lyrics_to_newtxt(pdf_path, project_root="/home/ken/Applications/python/zbpycolorscan"):
    base_dir = os.path.join(project_root, "txt")
    heb_dir = os.path.join(base_dir, "heb")
    eng_dir = os.path.join(base_dir, "eng")

    os.makedirs(heb_dir, exist_ok=True)
    os.makedirs(eng_dir, exist_ok=True)

    reader = PdfReader(pdf_path)
    song_directory = {}

    print("Parsing Table of Contents pages using encoding-fallback logic (Pages 2 to 7)...")

    for page_num in range(1, 7):
        if page_num >= len(reader.pages):
            break

        page_text = reader.pages[page_num].extract_text()
        if not page_text:
            continue

        lines = page_text.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue

            match = re.search(r'(\d+)\s*$', line)
            if match:
                page_num_val = int(match.group(1))

                if page_num_val <= 7 or page_num_val >= len(reader.pages):
                    continue

                raw_title_part = line[:match.start()].strip()
                clean_title = raw_title_part.strip('", ').replace('""', '"').strip()

                if not clean_title or set(clean_title) == {'?'}:
                    clean_title = f"song_{page_num_val}"
                else:
                    # Parse table of contents correctly if reversed in stream layout
                    clean_title = reconstruct_rtl_line(clean_title)

                song_directory[page_num_val] = clean_title

    start_pages = sorted(song_directory.keys())

    if not start_pages:
        print("Error: Fallback parser could not establish structural page maps.")
        return

    print(f"Identified {len(song_directory)} songs total. Separating files into target folders...")

    for i, start_page in enumerate(start_pages):
        title = song_directory[start_page]
        next_song_start_page = start_pages[i + 1] if i + 1 < len(start_pages) else len(reader.pages) + 1

        lyric_lines = []
        for current_p in range(start_page, next_song_start_page):
            physical_index = current_p - 1
            if physical_index >= len(reader.pages):
                break

            page_text = reader.pages[physical_index].extract_text()
            if not page_text:
                continue

            raw_lines = page_text.split('\n')

            # Reconstruct every single lyric sentence line to flip memory dump reading order
            lines = [reconstruct_rtl_line(l.strip()) for l in raw_lines if l.strip()]

            # Remove structural text headers matching Title or current index indicators
            if current_p == start_page:
                cleaned_lines = []
                for line in lines:
                    if line == str(start_page) or line == title or line == reconstruct_rtl_line(title):
                        continue
                    cleaned_lines.append(line)
                lines = cleaned_lines

            lyric_lines.extend(lines)

        full_lyric_text = "\n".join(lyric_lines).strip()
        full_lyric_text = re.sub(r'\n\s*\d+\s*\n', '\n', full_lyric_text)

        if is_hebrew(title) or is_hebrew(full_lyric_text):
            target_dir = heb_dir
            suffix = "_he.txt"
        else:
            target_dir = eng_dir
            suffix = "_en.txt"

        safe_title = clean_filename(title)
        filename = f"{safe_title}{suffix}"
        file_path = os.path.join(target_dir, filename)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"{title}\n\n")
            f.write(full_lyric_text)

    print(f"\nSuccess! Found and written {len(start_pages)} files successfully inside:\n -> {base_dir}")


if __name__ == "__main__":
    print("=========================================")
    print(f" Running zb_readpdf.py | Version: {SCRIPT_VERSION}")
    print("=========================================\n")

    pdf_filename = "zblyrics.pdf"

    if os.path.exists(pdf_filename):
        extract_lyrics_to_newtxt(pdf_filename)
    else:
        alternative_path = os.path.join("/home/ken/Applications/python/zbpycolorscan", pdf_filename)
        if os.path.exists(alternative_path):
            extract_lyrics_to_newtxt(alternative_path)
        else:
            print(f"Error: Could not locate '{pdf_filename}' in current workspace paths.")