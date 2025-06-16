import shutil
from pathlib import Path

# Define paths
BASE_DIR = Path(__file__).resolve().parents[1]
TEXT_JSON_DIR = BASE_DIR / "data" / "structured_json_from_text"
SCANNED_JSON_DIR = BASE_DIR / "data" / "structured_json_scanned"
FINAL_JSON_DIR = BASE_DIR / "data" / "final_json"

# Create final_json directory if not exists
FINAL_JSON_DIR.mkdir(parents=True, exist_ok=True)

# Merge files from both folders
def copy_json_files(source_dir):
    for json_file in source_dir.glob("*.json"):
        destination = FINAL_JSON_DIR / json_file.name

        # Rename if conflict
        if destination.exists():
            stem = json_file.stem
            suffix = json_file.suffix
            counter = 1
            while (FINAL_JSON_DIR / f"{stem}_{counter}{suffix}").exists():
                counter += 1
            destination = FINAL_JSON_DIR / f"{stem}_{counter}{suffix}"

        shutil.copy(json_file, destination)
        print(f"[+] Copied: {json_file.name} -> {destination.name}")

def main():
    copy_json_files(TEXT_JSON_DIR)
    copy_json_files(SCANNED_JSON_DIR)
    print("\n✅ All JSON files have been merged into 'final_json'.")

if __name__ == "__main__":
    main()
