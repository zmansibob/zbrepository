import os
import re

SCRIPT_VERSION = "4.0.0-PhoneticRename"

# Comprehensive phonetic mapping based on Hebrew pronunciation conventions
PHONETIC_MAP = {
    "1_45": "1_45",
    "3_51": "3_51",
    "אב_גיבור": "av_gibor",
    "אדם_ועם_נותרת": "adam_ve_am_notaret",
    "אדם_חשב_כך": "adam_chashav_kach",
    "אדם_עולם": "adam_olam",
    "אודי": "udi",
    "א_ועד_ת_מ_מציאות": "alef_ve_ad_tav_mi_mziut",
    "אותיות_וצבעים": "otiot_ve_tvaim",
    "אחרת_קצת": "acheret_ktzat",
    "אחרת_קצת_לעיתים": "acheret_ktzat_leitim",
    "איוב": "iyov",
    "איך_ועוד": "eich_ve_od",
    "איך_שגלגל_מסתובב": "eich_she_galgal_mistovev",
    "אינ_טימי_די": "intimidi",
    "איני_מודג": "eini_mudag",
    "אני_אתה,_הוא_והיא": "ani_ata_hu_ve_hi",
    "אני_הצרצר_והנמלה_והכבשים": "ani_ha_tzartzar_ve_ha_nemala_ve_ha_kvasim",
    "אני_ואז": "ani_ve_az",
    "אנרגיה_זמני": "energia_zmani",
    "אסטרונאוט_–_כרונואוט": "astronaut_chrononaut",
    "א׳_פרק_אנו_צועדים": "perek_alef_anu_tzoadim",
    "אפשרי": "efshari",
    "אקורד_סיום": "akord_siyum",
    "ארס_לא_שיר": "lo_shir_eres",
    "בארץ_זרה": "be_eretz_zara",
    "בבקשה_ת.ז.": "bevakasha_teudat_zehut",
    "בהדמפ": "be_hemdep",
    "בועות": "buot",
    "בוערת_לונדון": "london_boeret",
    "בחאלמא": "be_chalma",
    "בחירת_שלום": "bchirat_shalom",
    "בחנות_של_החי": "ba_chanut_shel_ha_chai",
    "יומית": "yomit",
    "סיפור_תספורת": "sipur_tisporet",
    "ספרים_ספרן": "sfarim_safran",
    "ספרן_ספרים": "safran_sfarim",
    "סרק_פחד": "pachad_srak",
    "עבה_פיל": "pil_abe",
    "עוד_יום_שכזה": "od_yom_she_kaze",
    "עוד_שילוט_שילוש": "od_shilut_shilush",
    "עולם_אדם": "olam_adam",
    "עולם_כמנהגו": "olam_ke_minhago",
    "עידו_לא_יודע_שלכם": "ido_lo_yodea_shelachem",
    "עיניים_מֵאחֶז": "einaim_meachez",
    "עיר_משבר": "ir_mashber",
    "עלה_רוח_קרקע": "ale_ruach_karka",
    "עם_בוא_הברורים": "im_bo_ha_brurim",
    "עמוד_ריק": "amud_rik",
    "פחד_סרק": "pachad_srak",
    "פיל_עבה": "pil_ave",
    "פינה_קסומה": "pina_ksuma",
    "פסיעה_נוספת_בשביל": "psia_nosefet_ba_shvil",
    "פרד_או_זוג": "zug_o_pered",
    "פשוט_מסר": "pashut_mesar",
    "פתוחה_שאלה": "sheela_ptucha",
    "צבעים_מילים": "miling_tzevaim",
    "צועדים_אנו_פרק_א׳": "anu_tzoadim_perek_alef",
    "צוק_ברחוב": "tzuk_ba_rchov",
    "ציור_לכתוב": "lichtov_tziur",
    "צמד_חמד": "tzemed_chemed",
    "קירוב_לבבות": "kiruv_levavot",
    "קלפים_מִשְחק": "mischak_klafim",
    "קסומה_פינה": "pina_ksuma",
    "קפה_ןחולי_שכינה": "kafe_ve_choli_shchina",
    "קפה_סיםני": "kafe_simanei",
    "תפאורה": "tefura",
    "תעתועים_רגעי": "rgei_taatuim",
    "רגעי_תעתועים": "rgei_taatuim"
}


def sanitize_english_filename(name):
    """
    Removes remaining punctuation, Hebrew Nikud artifacts, dashes,
    or spaces, enforcing completely clean English snake_case conventions.
    """
    # Replace remaining dashes or dots with underscores
    clean = re.sub(r'[\s\-\.\–\‘\׳\,\’\:\'\"]+', '_', name)
    # Remove any character that isn't alphanumeric or underscore
    clean = re.sub(r'[^a-zA-Z0-9_]', '', clean)
    # Collapse multiple consecutive underscores
    clean = re.sub(r'_+', '_', clean)
    return clean.strip('_').lower()


def rename_hebrew_files_phonetically(project_root="/home/ken/Applications/python/zbpycolorscan"):
    heb_dir = os.path.join(project_root, "txt", "heb")

    if not os.path.exists(heb_dir):
        print(f"Error: Target path does not exist: {heb_dir}")
        return

    print("====================================================")
    # Read files physically in the target directory
    files_in_dir = os.listdir(heb_dir)
    rename_count = 0
    skipped_count = 0

    print(f"Scanning directory: {heb_dir}")
    print(f"Found {len(files_in_dir)} files total. Beginning translation mapping...\n")

    for filename in files_in_dir:
        # We only look for files ending with our original suffix
        if not filename.endswith("_he.txt"):
            continue

        # Extract the core base name without the extension or target marker
        base_name = filename.replace("_he.txt", "")

        # Strip invisible Hebrew vowel pointing (Nikud) or punctuation for exact dictionary lookups
        normalized_lookup = re.sub(r'[\u05B0-\u05C7]', '', base_name)

        new_english_base = None

        # Check if we have an explicit phonetic translation mapped out
        if normalized_lookup in PHONETIC_MAP:
            new_english_base = PHONETIC_MAP[normalized_lookup]
        else:
            # Fallback optimization if an unmapped file appears
            # It replaces illegal characters and leaves a tracer tag
            new_english_base = "unmapped_" + sanitize_english_filename(normalized_lookup)

        # Enforce standard English naming format
        clean_english_base = sanitize_english_filename(new_english_base)
        new_filename = f"{clean_english_base}_he.txt"

        old_file_path = os.path.join(heb_dir, filename)
        new_file_path = os.path.join(heb_dir, new_filename)

        if filename == new_filename:
            skipped_count += 1
            continue

        # Handle edge cases where multiple files map to the same name to prevent overwrites
        if os.path.exists(new_file_path) and old_file_path != new_file_path:
            counter = 1
            while os.path.exists(os.path.join(heb_dir, f"{clean_english_base}_{counter}_he.txt")):
                counter += 1
            new_filename = f"{clean_english_base}_{counter}_he.txt"
            new_file_path = os.path.join(heb_dir, new_filename)

        # Execute system rename operation on Ubuntu file system
        try:
            os.rename(old_file_path, new_file_path)
            print(f" RENAME: [ {filename} ] \n     --> [ {new_filename} ]\n")
            rename_count += 1
        except Exception as e:
            print(f" Fail to rename {filename}: {str(e)}")

    print("====================================================")
    print(f"Batch Processing Complete!")
    print(f" -> Successfully Renamed: {rename_count} files")
    print(f" -> Already Standardized/Skipped: {skipped_count} files")


if __name__ == "__main__":
    rename_hebrew_files_phonetically()