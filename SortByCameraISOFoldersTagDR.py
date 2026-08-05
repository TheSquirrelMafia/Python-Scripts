import os
import subprocess
import re

# Map ISO value into your defined buckets
def iso_bucket(iso):
    if 1 <= iso <= 100:
        return 100
    elif 101 <= iso <= 200:
        return 200
    elif 201 <= iso <= 400:
        return 400
    elif 401 <= iso <= 800:
        return 800
    elif 801 <= iso <= 1600:
        return 1600
    elif 1601 <= iso <= 3200:
        return 3200
    elif 3201 <= iso <= 6400:
        return 6400
    elif 6401 <= iso <= 12800:
        return 12800
    elif 12801 <= iso <= 25600:
        return 25600
    elif 25601 <= iso <= 51200:
        return 51200
    else:
        return iso


def extract_metadata(file_path):
    try:
        # Extract ISO, Model, and DRE
        result = subprocess.run(
            [
                "C:\\exiftool.exe",
                "-ISO",
                "-Model",
                "-DynamicRangeExpansion",
                "-S",
                file_path
            ],
            capture_output=True,
            text=True
        )

        lines = result.stdout.strip().splitlines()
        iso, model, dre = None, None, None

        for line in lines:
            if line.startswith("ISO:"):
                iso = int(line.split(":", 1)[1].strip())

            elif line.startswith("Model:"):
                model = line.split(":", 1)[1].strip().replace(" ", "_")

            elif line.startswith("DynamicRangeExpansion:"):
                dre_raw = line.split(":", 1)[1].strip().upper()

                # Normalize separators for easier matching
                dre_clean = (
                    dre_raw
                    .replace(";", "_")
                    .replace(",", "_")
                    .replace(" ", "_")
                )

                # Treat all known ON variants as ON
                # Examples:
                # ON;AUTO;0,0
                # ON;ENABLED;0;0
                # On; Enabled; 0; 0
                # ON
                if (
                    "ON" in dre_clean
                    or "ENABLED" in dre_clean
                ):
                    dre = "ON"
                else:
                    dre = "OFF"

        return iso, model, dre

    except Exception as e:
        print(f"Error extracting metadata from {file_path}: {e}")
        return None, None, None


def sort_raw_files_by_iso_model(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.pef', '.dng')):
                file_path = os.path.join(root, file)

                iso, model, dre = extract_metadata(file_path)

                if iso is not None and model is not None:
                    bucket = iso_bucket(iso)

                    # Folder name
                    dir_name = f"{model}_ISO_{bucket}"
                    target_dir = os.path.join(root, dir_name)
                    os.makedirs(target_dir, exist_ok=True)

                    # Append _DR when DRE is ON
                    base, ext = os.path.splitext(file)

                    if dre == "ON":
                        new_file_name = f"{base}_DR{ext}"
                    else:
                        new_file_name = file

                    source_path = file_path
                    destination_path = os.path.join(
                        target_dir,
                        new_file_name
                    )

                    os.rename(source_path, destination_path)

                    print(f"Moved {file} -> {destination_path}")

                else:
                    print(f"Skipped {file} (missing ISO or Model)")


if __name__ == "__main__":
    directory_path = 'C:\\change\\path\\to\\whatever'
    sort_raw_files_by_iso_model(directory_path)
    print(
        "Raw files sorted into Model/ISO folders "
        "with _DR tagging for all ON/Enabled DRE modes."
    )