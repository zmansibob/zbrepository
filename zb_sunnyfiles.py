import os
import re

# VERSION TRACKING
SCRIPT_VERSION = "1.0.0-FilenameSanitizer"


def strip_nikud(text):
    """Removes invisible Hebrew vocal pointing pointing (Nikud)."""
    return re.sub(r'[\u05B0-\u05C7]', '', text)


def clean_system_filename(filename, is_hebrew_folder=False):
    """
    Strips system-unfriendly symbols like quotes, smart apostrophes,
    ellipses, and exotic dashes, returning a clean snake_case filename.
    """
    # Isolate name base and extension
    name, ext = os.path.splitext(filename)

    # Strip Hebrew vocal signs out right away if applicable
    if is_hebrew_folder:
        name = strip_nikud(name)

    # 1. Replace commas, dashes, en-dashes, dots, ellipses, and quotes with underscores
    clean = re.sub(r'[\s\-\–\—\.\…\,\'\"’‘׳״\(\)\[\]\{\}\:]+', '_', name)

    # 2. Strict character filtering
    if is_hebrew_folder:
        # Allow standard Hebrew range, English alphanumerics, and underscores
        clean = re.sub(r'[^a-zA-Z0-9_\u0590-\u05FF]', '', clean)
    else:
        # Strictly English alphanumerics and underscores
        clean = re.sub(r'[^a-zA-Z0-9_]', '', clean)

    # 3. Collapse multiple consecutive underscores and clean edges
    clean = re.sub(r'_+', '_', clean).strip('_')

    # Restore the extension in clean lowercase
    return f"{clean}{ext.lower()}"


def sanitize_project_directories(project_root="/home/ken/Applications/python/zbpycolorscan"):
    txt_dir = os.path.join(project_root, "txt")

    targets = [
        {"path": os.path.join(txt_dir, "eng"), "is_heb": False},
        {"path": os.path.join(txt_dir, "heb"), "is_heb": True}
    ]

    print("====================================================")
    print(f" Running Filename Sanitizer | Version: {SCRIPT_VERSION}")
    print("====================================================\n")

    for target in targets:
        target_dir = target["path"]
        is_heb = target["is_heb"]

        if not os.path.exists(target_dir):
            print(f"Skipping: Directory path does not exist: {target_dir}")
            continue

        print(f"Scanning directory: {target_dir}")
        files = os.listdir(target_dir)
        rename_count = 0

        for filename in files:
            if not os.path.isfile(os.path.join(target_dir, filename)):
                continue

            # Generate the sanitized clean name
            new_filename = clean_system_filename(filename, is_hebrew_folder=is_heb)

            if filename == new_filename:
                continue

            old_path = os.path.join(target_dir, filename)
            new_path = os.path.join(target_dir, new_filename)

            # Prevent overwriting accidental duplicates
            if os.path.exists(new_path):
                name, ext = os.path.splitext(new_filename)
                counter = 1
                while os.path.exists(os.path.join(target_dir, f"{name}_{counter}{ext}")):
                    counter += 1
                new_filename = f"{name}_{counter}{ext}"
                new_path = os.path.join(target_dir, new_filename)

            try:
                os.rename(old_path, new_path)
                print(f" SANITIZED: [ {filename} ]\n          --> [ {new_filename} ]")
                rename_count += 1
            except Exception as e:
                print(f" Failed to sanitize '{filename}': {str(e)}")

        print(f"-> Completed folder! Cleaned {rename_count} filenames.\n")


if __name__ == "__main__":
    sanitize_project_directories()