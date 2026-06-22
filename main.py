#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════
  WorkSpace AutoClean Pro — Freelance Automation Portfolio Demo
  Author  : Senior Python Automation Engineer
  Version : 2.0.0
  Platform: Khamsat / Freelance Services
  Purpose : Portfolio demonstration of real client automation work
═══════════════════════════════════════════════════════════════════
  SERVICE OFFERED:
  "I will automate your file organization and data cleaning
   so you save hours of manual work every week."
═══════════════════════════════════════════════════════════════════
"""

import os
import json
import time
import datetime
from typing import Dict, List, Tuple

# ─────────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────────

VERSION      = "2.0.0"
WIDTH        = 64          # terminal column width for all dividers
EXPORT_DIR   = "exports"   # folder where TXT / JSON reports are saved

# ─────────────────────────────────────────────────────────────────
# SAMPLE DATA  (simulates a real client's messy environment)
# ─────────────────────────────────────────────────────────────────

SAMPLE_FILES: List[str] = [
    "invoice_march.pdf",
    "profile_photo.jpg",
    "meeting_notes.txt",
    "product_demo.mp4",
    "contract_2024.docx",
    "screenshot_001.png",
    "annual_report.pdf",
    "vacation.jpg",
    "tutorial_python.mp4",
    "README.txt",
    "proposal_client_A.docx",
    "logo_final_v3.png",
    "team_photo.jpg",
    "webinar_recording.mp4",
    "budget_Q1.pdf",
    "notes_random.txt",
    "banner_design.png",
    "onboarding_guide.docx",
    "backup_old.pdf",
    "screen_record.mp4",
]

SAMPLE_MESSY_DATA: List[str] = [
    "  Hello   World  this is   a TEST string  ",
    "Python is GREAT for   automation and scripting.",
    "  freelance   developers   save   clients   TIME and MONEY  ",
    "Clean  data   leads   to   better   decisions.",
    "Python is GREAT for   automation and scripting.",   # duplicate
    "  automation   tools   reduce   human   error  ",
    "  Hello   World  this is   a TEST string  ",        # duplicate
    "Every   business   needs   digital   TOOLS   in 2025.",
    "data cleaning IS the first step   in any PIPELINE.",
    "  automation   tools   reduce   human   error  ",   # duplicate
]

# ─────────────────────────────────────────────────────────────────
# FILE CATEGORY DEFINITIONS
# Key  : human-readable label (emoji + name)
# Value: list of file extensions that belong to this category
# ─────────────────────────────────────────────────────────────────

FILE_CATEGORIES: Dict[str, List[str]] = {
    "📸  Images":    [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "📄  Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".csv"],
    "🎬  Videos":    [".mp4", ".avi", ".mov", ".mkv", ".wmv", ".flv"],
    "🎵  Audio":     [".mp3", ".wav", ".aac", ".flac"],
    "📦  Archives":  [".zip", ".rar", ".tar", ".gz"],
    "❓  Unknown":   [],
}

# Pre-build a flat extension → category lookup for O(1) categorisation
# Built once at import time; never recomputed during a run.
_EXT_LOOKUP: Dict[str, str] = {
    ext: cat
    for cat, exts in FILE_CATEGORIES.items()
    for ext in exts
}

UNKNOWN_LABEL = "❓  Unknown"

# ─────────────────────────────────────────────────────────────────
# DISPLAY HELPERS
# ─────────────────────────────────────────────────────────────────

def clear() -> None:
    """Clear the terminal screen on Windows and Unix/macOS."""
    os.system("cls" if os.name == "nt" else "clear")


def divider(char: str = "─", width: int = WIDTH) -> None:
    print(char * width)


def header(title: str) -> None:
    """Print a centred, double-bordered section header."""
    divider("═")
    # Clamp padding so titles longer than WIDTH still render cleanly
    inner = WIDTH - 2
    centred = title.center(inner)
    print(f"═{centred}═")
    divider("═")


def section(title: str) -> None:
    """Print a thin-bordered sub-section label."""
    print()
    divider("─")
    print(f"  {title}")
    divider("─")


def step(msg: str, delay: float = 0.15) -> None:
    """Print a processing step with a short animated delay."""
    print(f"  ▸  {msg}")
    time.sleep(delay)


def success(msg: str) -> None:
    print(f"  ✔  {msg}")


def warn(msg: str) -> None:
    print(f"  ⚠  {msg}")


def info(msg: str) -> None:
    print(f"  ℹ  {msg}")


def elapsed(seconds: float) -> str:
    """Return a human-readable elapsed-time string."""
    if seconds < 1:
        return f"{seconds * 1000:.0f} ms"
    return f"{seconds:.2f} s"


# ─────────────────────────────────────────────────────────────────
# INPUT HELPER
# ─────────────────────────────────────────────────────────────────

def get_valid_choice(prompt: str, valid: List[str]) -> str:
    """
    Loop until the user enters one of the accepted values.
    Strips whitespace; case-insensitive for single letters.
    """
    while True:
        try:
            raw = input(prompt).strip().lower()
        except (EOFError, KeyboardInterrupt):
            # Graceful Ctrl-C / piped input termination
            print()
            return valid[0]
        if raw in [v.lower() for v in valid]:
            return raw
        warn(f"Invalid input. Please enter one of: {', '.join(valid)}")


# ─────────────────────────────────────────────────────────────────
# EXPORT ENGINE
# ─────────────────────────────────────────────────────────────────

def _ensure_export_dir() -> bool:
    """Create the exports directory if it does not exist. Returns True on success."""
    try:
        os.makedirs(EXPORT_DIR, exist_ok=True)
        return True
    except OSError as exc:
        warn(f"Cannot create export folder '{EXPORT_DIR}': {exc}")
        return False


def export_report(payload: dict, module_tag: str) -> None:
    """
    Write *payload* to both a human-readable TXT file and a
    machine-readable JSON file inside EXPORT_DIR.

    Parameters
    ----------
    payload    : structured dict produced by each run_ function
    module_tag : short tag used in the filename, e.g. 'files', 'data', 'full'
    """
    if not _ensure_export_dir():
        return

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = f"autoclean_{module_tag}_{timestamp}"

    # ── JSON export ───────────────────────────────────────────
    json_path = os.path.join(EXPORT_DIR, f"{base_name}.json")
    try:
        with open(json_path, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2)
        success(f"JSON report saved  →  {json_path}")
    except OSError as exc:
        warn(f"Could not write JSON report: {exc}")

    # ── TXT export ────────────────────────────────────────────
    txt_path = os.path.join(EXPORT_DIR, f"{base_name}.txt")
    try:
        lines: List[str] = []
        lines.append("═" * WIDTH)
        lines.append(f"  WorkSpace AutoClean Pro  ·  v{VERSION}")
        lines.append(f"  Generated : {payload.get('generated_at', 'N/A')}")
        lines.append(f"  Module    : {payload.get('module', 'N/A')}")
        lines.append("═" * WIDTH)

        for section_key, section_data in payload.get("sections", {}).items():
            lines.append("")
            lines.append(f"  {section_key.upper()}")
            lines.append("─" * WIDTH)
            if isinstance(section_data, dict):
                for k, v in section_data.items():
                    lines.append(f"    {k:<30} {v}")
            elif isinstance(section_data, list):
                for item in section_data:
                    lines.append(f"    • {item}")
            else:
                lines.append(f"    {section_data}")

        lines.append("")
        lines.append("═" * WIDTH)
        lines.append("")

        with open(txt_path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines))
        success(f"TXT report saved   →  {txt_path}")
    except OSError as exc:
        warn(f"Could not write TXT report: {exc}")


def prompt_export(payload: dict, module_tag: str) -> None:
    """Ask the user whether to export the report, then act on the answer."""
    print()
    divider()
    choice = get_valid_choice(
        "  Export results to file? [y / n]: ",
        valid=["y", "n"],
    )
    if choice == "y":
        export_report(payload, module_tag)
    else:
        info("Export skipped.")


# ─────────────────────────────────────────────────────────────────
# MODULE 1 — FILE ORGANIZATION
# ─────────────────────────────────────────────────────────────────

def get_category(filename: str) -> str:
    """
    Return the display-category label for *filename*.

    Uses the pre-built _EXT_LOOKUP dict for O(1) lookup instead of
    iterating over FILE_CATEGORIES on every call.
    """
    if not isinstance(filename, str) or not filename.strip():
        return UNKNOWN_LABEL
    _, ext = os.path.splitext(filename.lower())
    return _EXT_LOOKUP.get(ext, UNKNOWN_LABEL)


def organize_files(files: List[str]) -> Dict[str, List[str]]:
    """
    Group *files* by category.

    Returns a dict of {category_label: [filenames]}.
    Empty categories are included so callers can iterate all labels.
    """
    organized: Dict[str, List[str]] = {cat: [] for cat in FILE_CATEGORIES}
    for filename in files:
        cat = get_category(filename)
        organized[cat].append(filename)
    return organized


def run_file_organization() -> None:
    t_start = time.monotonic()
    header("MODULE 1 — FILE ORGANIZATION")
    now_str = datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
    print()
    info(f"Source  : Simulated client downloads folder")
    info(f"Files   : {len(SAMPLE_FILES)} items detected")
    info(f"Started : {now_str}")

    # ── Scan ──────────────────────────────────────────────────
    section("SCANNING FILES")
    for f in SAMPLE_FILES:
        step(f"Scanning  →  {f}")

    # ── Organise ──────────────────────────────────────────────
    section("ORGANISING INTO FOLDERS")
    organized = organize_files(SAMPLE_FILES)

    categorized_count = 0
    unknown_files: List[str] = organized.get(UNKNOWN_LABEL, [])

    for category, files in organized.items():
        if not files or category == UNKNOWN_LABEL:
            continue
        folder_name = category.split("  ", 1)[-1]   # strip emoji prefix
        step(f"Creating folder  →  /{folder_name}/")
        for f in files:
            step(f"Moving           →  /{folder_name}/{f}")
            categorized_count += 1

    if unknown_files:
        warn(f"Flagging {len(unknown_files)} unrecognised file(s) for manual review")

    # ── Tree view ─────────────────────────────────────────────
    section("ORGANISED STRUCTURE")
    print()
    print("  📁  Downloads/")
    categories_with_files = [(c, f) for c, f in organized.items() if f]
    for idx, (category, files) in enumerate(categories_with_files):
        is_last_cat = idx == len(categories_with_files) - 1
        branch = "└──" if is_last_cat else "├──"
        print(f"  │")
        print(f"  {branch} {category}  ({len(files)} files)")
        for i, f in enumerate(files):
            connector = "└──" if i == len(files) - 1 else "├──"
            prefix = "        " if is_last_cat else "│       "
            print(f"  {prefix}{connector} {f}")
    print()

    # ── Bar chart summary ─────────────────────────────────────
    section("FILE ORGANISATION SUMMARY")
    max_bar = 20
    total_moved = sum(
        len(v) for k, v in organized.items() if k != UNKNOWN_LABEL
    )
    print()
    for category, files in organized.items():
        if not files:
            continue
        filled = min(len(files), max_bar)
        bar = "█" * filled + "░" * (max_bar - filled)
        print(f"  {category:<22}  [{bar}]  {len(files):>2} file(s)")

    t_elapsed = time.monotonic() - t_start
    print()
    divider()
    success(f"Total files processed  : {len(SAMPLE_FILES)}")
    success(f"Successfully organised : {categorized_count}")
    if unknown_files:
        warn(f"Flagged for review     : {len(unknown_files)}")
    info(f"Time elapsed           : {elapsed(t_elapsed)}")

    # ── Build export payload ──────────────────────────────────
    payload: dict = {
        "module"       : "File Organisation",
        "generated_at" : now_str,
        "sections": {
            "Statistics": {
                "Total files processed"  : len(SAMPLE_FILES),
                "Successfully organised" : categorized_count,
                "Flagged for review"     : len(unknown_files),
                "Time elapsed"           : elapsed(t_elapsed),
            },
            "Organised categories": {
                cat: files
                for cat, files in organized.items()
                if files
            },
        },
    }

    prompt_export(payload, "files")
    print()
    input("  Press ENTER to return to menu...")


# ─────────────────────────────────────────────────────────────────
# MODULE 2 — DATA CLEANING
# ─────────────────────────────────────────────────────────────────

def clean_text(raw: str) -> str:
    """
    Normalise a single string:
      1. Collapse all whitespace runs to a single space
      2. Strip leading / trailing whitespace
      3. Convert to lowercase
    Returns an empty string if *raw* is not a string.
    """
    if not isinstance(raw, str):
        return ""
    return " ".join(raw.split()).lower()


def count_words(text: str) -> int:
    """Return the word count of *text*. Returns 0 for empty / non-string input."""
    if not isinstance(text, str) or not text.strip():
        return 0
    return len(text.split())


def remove_duplicates(items: List[str]) -> List[str]:
    """
    Return *items* with duplicates removed, preserving insertion order.
    Uses dict.fromkeys() — O(n) instead of the O(n²) seen-list approach.
    """
    return list(dict.fromkeys(items))


def run_data_cleaning() -> None:
    t_start = time.monotonic()
    header("MODULE 2 — DATA CLEANING")
    now_str = datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
    print()
    info(f"Input   : {len(SAMPLE_MESSY_DATA)} raw text entries")
    info(f"Source  : Copied from mixed client documents / emails")
    info(f"Started : {now_str}")

    # ── Raw input preview ─────────────────────────────────────
    section("RAW INPUT (before cleaning)")
    print()
    for i, line in enumerate(SAMPLE_MESSY_DATA, 1):
        print(f"  [{i:02}]  \"{line}\"")

    # ── Processing ────────────────────────────────────────────
    section("PROCESSING STEPS")
    print()
    step("Removing leading and trailing whitespace")
    step("Collapsing multiple spaces into single spaces")
    step("Normalising text to lowercase")
    step("Scanning for duplicate entries")

    cleaned_entries  = [clean_text(line) for line in SAMPLE_MESSY_DATA]
    unique_entries   = remove_duplicates(cleaned_entries)
    duplicates_found = len(cleaned_entries) - len(unique_entries)

    # Guard against empty source data causing ZeroDivisionError
    chars_before = sum(len(r) for r in SAMPLE_MESSY_DATA)
    chars_after  = sum(len(c) for c in unique_entries)
    chars_saved  = chars_before - chars_after
    reduction_pct = (
        round(chars_saved / chars_before * 100, 1) if chars_before else 0.0
    )
    total_words = sum(count_words(e) for e in unique_entries)

    # ── Cleaned output ────────────────────────────────────────
    section("CLEANED OUTPUT (after processing)")
    print()
    for i, line in enumerate(unique_entries, 1):
        print(f"  [{i:02}]  \"{line}\"")

    t_elapsed = time.monotonic() - t_start

    # ── Summary ───────────────────────────────────────────────
    section("DATA CLEANING SUMMARY")
    print()
    success(f"Entries before cleaning  : {len(SAMPLE_MESSY_DATA)}")
    success(f"Duplicates removed       : {duplicates_found}")
    success(f"Unique clean entries     : {len(unique_entries)}")
    info(   f"Total word count         : {total_words} words")
    info(   f"Characters before        : {chars_before}")
    info(   f"Characters after         : {chars_after}")
    info(   f"Characters saved         : {chars_saved}  ({reduction_pct}% reduction)")
    info(   f"Time elapsed             : {elapsed(t_elapsed)}")

    # ── Build export payload ──────────────────────────────────
    payload: dict = {
        "module"       : "Data Cleaning",
        "generated_at" : now_str,
        "sections": {
            "Statistics": {
                "Entries before cleaning" : len(SAMPLE_MESSY_DATA),
                "Duplicates removed"      : duplicates_found,
                "Unique clean entries"    : len(unique_entries),
                "Total word count"        : total_words,
                "Characters before"       : chars_before,
                "Characters after"        : chars_after,
                "Size reduction"          : f"{reduction_pct}%",
                "Time elapsed"            : elapsed(t_elapsed),
            },
            "Clean entries": unique_entries,
        },
    }

    prompt_export(payload, "data")
    print()
    input("  Press ENTER to return to menu...")


# ─────────────────────────────────────────────────────────────────
# MODULE 3 — FULL AUTOMATION PIPELINE
# ─────────────────────────────────────────────────────────────────

def run_full_automation() -> None:
    t_start = time.monotonic()
    header("FULL AUTOMATION PIPELINE")
    now_str = datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
    print()
    info("Running complete workspace automation workflow...")
    info("This combines File Organisation + Data Cleaning in one pass.")
    print()
    time.sleep(0.8)

    # ── Phase 1 — File organisation ───────────────────────────
    section("PHASE 1 OF 2  —  FILE ORGANISATION")
    t_phase1 = time.monotonic()
    organized = organize_files(SAMPLE_FILES)
    for f in SAMPLE_FILES:
        step(f"Processing  →  {f}")

    total_categorized = sum(
        len(v) for k, v in organized.items() if k != UNKNOWN_LABEL
    )
    unknown_count = len(organized.get(UNKNOWN_LABEL, []))
    t_phase1_done = time.monotonic() - t_phase1
    print()
    success(
        f"File organisation complete  ·  {len(SAMPLE_FILES)} files  "
        f"·  {elapsed(t_phase1_done)}"
    )

    # ── Phase 2 — Data cleaning ───────────────────────────────
    section("PHASE 2 OF 2  —  DATA CLEANING")
    t_phase2 = time.monotonic()
    cleaned_entries    = [clean_text(line) for line in SAMPLE_MESSY_DATA]
    unique_entries     = remove_duplicates(cleaned_entries)
    duplicates_removed = len(cleaned_entries) - len(unique_entries)

    chars_before  = sum(len(r) for r in SAMPLE_MESSY_DATA)
    chars_after   = sum(len(c) for c in unique_entries)
    reduction_pct = (
        round((chars_before - chars_after) / chars_before * 100, 1)
        if chars_before else 0.0
    )
    total_words = sum(count_words(e) for e in unique_entries)

    step("Whitespace normalisation complete")
    step("Text case normalisation complete")
    step(f"Duplicate detection complete  →  {duplicates_removed} removed")
    t_phase2_done = time.monotonic() - t_phase2
    print()
    success(
        f"Data cleaning complete  ·  {len(unique_entries)} clean entries  "
        f"·  {elapsed(t_phase2_done)}"
    )

    t_total = time.monotonic() - t_start

    # ── Final report ──────────────────────────────────────────
    print()
    divider("═")
    print(f"{'  FINAL AUTOMATION REPORT':^{WIDTH}}")
    print(f"{'  Generated: ' + now_str:^{WIDTH}}")
    divider("═")

    print()
    print("  FILE ORGANISATION RESULTS")
    divider()
    for category, files in organized.items():
        if files:
            print(f"    {category:<22}  →  {len(files):>2} file(s)")
    print()
    success(f"  Total files      : {len(SAMPLE_FILES)}")
    success(f"  Organised        : {total_categorized}")
    if unknown_count:
        warn(f"  Needs review     : {unknown_count}")
    info(   f"  Phase time       : {elapsed(t_phase1_done)}")

    print()
    print("  DATA CLEANING RESULTS")
    divider()
    success(f"  Input entries    : {len(SAMPLE_MESSY_DATA)}")
    success(f"  Clean entries    : {len(unique_entries)}")
    success(f"  Duplicates cut   : {duplicates_removed}")
    info(   f"  Words indexed    : {total_words}")
    info(   f"  Size reduction   : {reduction_pct}%")
    info(   f"  Phase time       : {elapsed(t_phase2_done)}")

    print()
    divider("═")
    success(f"  TOTAL PIPELINE TIME : {elapsed(t_total)}")
    divider("═")
    print()
    print("  ✅  WORKSPACE AUTOMATION COMPLETE")
    print("  Your files are organised. Your data is clean.")
    print("  Estimated time saved vs. manual work: ~45 minutes")
    print()
    divider("═")

    # ── Build export payload ──────────────────────────────────
    payload: dict = {
        "module"       : "Full Automation Pipeline",
        "generated_at" : now_str,
        "sections": {
            "File Organisation": {
                "Total files"           : len(SAMPLE_FILES),
                "Organised"             : total_categorized,
                "Flagged for review"    : unknown_count,
                "Phase time"            : elapsed(t_phase1_done),
                "Categories": {
                    cat: files
                    for cat, files in organized.items()
                    if files
                },
            },
            "Data Cleaning": {
                "Input entries"         : len(SAMPLE_MESSY_DATA),
                "Clean entries"         : len(unique_entries),
                "Duplicates removed"    : duplicates_removed,
                "Total words"           : total_words,
                "Size reduction"        : f"{reduction_pct}%",
                "Phase time"            : elapsed(t_phase2_done),
                "Clean entries list"    : unique_entries,
            },
            "Pipeline summary": {
                "Total pipeline time"   : elapsed(t_total),
                "Estimated time saved"  : "~45 minutes",
            },
        },
    }

    prompt_export(payload, "full")
    print()
    input("  Press ENTER to return to menu...")


# ─────────────────────────────────────────────────────────────────
# MAIN MENU
# ─────────────────────────────────────────────────────────────────

MENU_OPTIONS = {
    "1": ("📁  File Organisation",      "Scan and sort your files by type automatically"),
    "2": ("🧹  Data Cleaning",           "Normalise, deduplicate, and count your text data"),
    "3": ("🚀  Run Full Automation",     "Execute both modules in a single pass"),
    "4": ("📂  Open exports folder",    "View previously saved TXT / JSON reports"),
    "0": ("❌  Exit",                   ""),
}


def print_menu() -> None:
    clear()
    print()
    divider("═")
    print("  ██╗    ██╗ ██████╗ ██████╗ ██╗  ██╗███████╗██████╗  █████╗  ██████╗███████╗")
    print("  ██║    ██║██╔═══██╗██╔══██╗██║ ██╔╝██╔════╝██╔══██╗██╔══██╗██╔════╝██╔════╝")
    print("  ██║ █╗ ██║██║   ██║██████╔╝█████╔╝ ███████╗██████╔╝███████║██║     █████╗  ")
    print("  ██║███╗██║██║   ██║██╔══██╗██╔═██╗ ╚════██║██╔═══╝ ██╔══██║██║     ██╔══╝  ")
    print("  ╚███╔███╔╝╚██████╔╝██║  ██║██║  ██╗███████║██║     ██║  ██║╚██████╗███████╗")
    print("   ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝  ╚═╝ ╚═════╝╚══════╝")
    divider("═")
    print(f"  AutoClean Pro  ·  Freelance Automation Tool  ·  v{VERSION}")
    divider("═")
    print()
    print("  What would you like to automate today?\n")
    for key, (label, desc) in MENU_OPTIONS.items():
        if key == "0":
            print()
        print(f"    [{key}]  {label}")
        if desc:
            print(f"         {desc}")
        if key not in ("0",):
            print()
    divider("═")


def open_exports_folder() -> None:
    """Open (or print) the exports folder path so the user can inspect reports."""
    abs_path = os.path.abspath(EXPORT_DIR)
    if not os.path.isdir(abs_path):
        warn(f"No exports folder found yet. Run a module first.")
    else:
        reports = [f for f in os.listdir(abs_path)
                   if f.endswith((".txt", ".json"))]
        section("EXPORTS FOLDER")
        print()
        info(f"Location : {abs_path}")
        info(f"Reports  : {len(reports)} file(s) found")
        print()
        if reports:
            for r in sorted(reports):
                print(f"    📄  {r}")
        else:
            info("No reports yet.")
    print()
    input("  Press ENTER to return to menu...")


def main() -> None:
    """Main entry point — drives the menu loop."""
    dispatch = {
        "1": run_file_organization,
        "2": run_data_cleaning,
        "3": run_full_automation,
        "4": open_exports_folder,
    }

    while True:
        print_menu()
        choice = get_valid_choice(
            "  Enter your choice [0-4]: ",
            valid=list(MENU_OPTIONS.keys()),
        )
        print()

        if choice == "0":
            clear()
            divider("═")
            print()
            print("  Thank you for using WorkSpace AutoClean Pro.")
            print("  For custom automation solutions, contact us on Khamsat.")
            print()
            divider("═")
            print()
            break

        clear()
        try:
            dispatch[choice]()
        except Exception as exc:   # safety net — never crash in front of a client
            warn(f"Unexpected error: {exc}")
            info("Please try again or contact support.")
            print()
            input("  Press ENTER to return to menu...")


# ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    main()
