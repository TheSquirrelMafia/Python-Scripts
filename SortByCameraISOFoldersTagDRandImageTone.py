import os
import subprocess

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
        result = subprocess.run(
            [
                "C:\\exiftool.exe",
                "-ISO",
                "-Model",
                "-DynamicRangeExpansion",
                "-ImageTone",
                "-S",
                file_path
            ],
            capture_output=True,
            text=True
        )

        lines = result.stdout.strip().splitlines()
        iso, model, dre, tone = None, None, None, None

        for line in lines:
            if line.startswith("ISO:"):
                iso = int(line.split(":", 1)[1].strip())

            elif line.startswith("Model:"):
                model = line.split(":", 1)[1].strip().replace(" ", "_")

            elif line.startswith("ImageTone:"):
                tone = line.split(":", 1)[1].strip().replace(" ", "_")

            elif line.startswith("DynamicRangeExpansion:"):
                dre_raw = line.split(":", 1)[1].strip().upper()

                # Normalize separators
                dre_clean = (
                    dre_raw
                    .replace(";", "_")
                    .replace(",", "_")
                    .replace(" ", "_")
                )

                # Treat all ON/Enabled variants as ON
                if (
                    "ON" in dre_clean
                    or "ENABLED" in dre_clean
                ):
                    dre = "ON"
                else:
                    dre = "OFF"

        return iso, model, dre, tone

    except Exception as e:
        print(f"Error extracting metadata from {file_path}: {e}")
        return None, None, None, None


def sort_raw_files_by_iso_model(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.pef', '.dng')):
                file_path = os.path.join(root, file)

                iso, model, dre, tone = extract_metadata(file_path)

                if iso is not None and model is not None:
                    bucket = iso_bucket(iso)

                    # Folder name
                    dir_name = f"{model}_ISO_{bucket}"
                    target_dir = os.path.join(root, dir_name)
                    os.makedirs(target_dir, exist_ok=True)

                    base, ext = os.path.splitext(file)

                    # Build new filename:
                    # OriginalName_ImageTone_DR.ext
                    new_name_parts = [base]

                    # Append ImageTone first
                    if tone:
                        new_name_parts.append(tone)

                    # Append DR second if DRE is ON
                    if dre == "ON":
                        new_name_parts.append("DR")

                    new_file_name = "_".join(new_name_parts) + ext

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
        "Sorting complete: ImageTone appended first, "
        "then _DR for all ON/Enabled DRE modes."
    )