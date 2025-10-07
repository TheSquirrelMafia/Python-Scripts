import os
import subprocess
import re

def extract_metadata(file_path):
    """Extract Model, DRE (DynamicRangeExpansion), and ImageTone values."""
    try:
        result = subprocess.run(
            ["C:\\exiftool.exe", "-Model", "-DynamicRangeExpansion", "-ImageTone", "-S", file_path],
            capture_output=True,
            text=True
        )

        lines = result.stdout.strip().splitlines()
        model, dre, tone = None, None, None

        for line in lines:
            if line.startswith("Model:"):
                model_raw = line.split(":", 1)[1].strip()
                model = model_raw.replace(" ", "_")

            elif line.startswith("DynamicRangeExpansion:"):
                dre_raw = line.split(":", 1)[1].strip()
                dre_upper = dre_raw.upper().replace(";", "_").replace(",", "_").replace(" ", "_")
                if re.search(r"OFF.*AUTO.*0.*0", dre_upper):
                    dre = "DRE_OFF_AUTO_0_0"
                elif re.search(r"ON.*AUTO.*0.*0", dre_upper):
                    dre = "DRE_ON_AUTO_0_0"
                elif "OFF" in dre_upper:
                    dre = "DRE_OFF_AUTO_0_0"
                elif "ON" in dre_upper:
                    dre = "DRE_ON_AUTO_0_0"
                else:
                    dre = "DRE_UNKNOWN"

            elif line.startswith("ImageTone:"):
                tone_raw = line.split(":", 1)[1].strip()
                tone = tone_raw.replace(" ", "_")

        return model, dre, tone

    except Exception as e:
        print(f"Error reading metadata from {file_path}: {e}")
        return None, None, None

def sort_by_model_dre_and_tone(directory):
    """Sort RAW files into folders by model + DRE and append ImageTone (+_DR if ON)."""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.nef', '.cr2', '.arw', '.pef', '.dng')):
                file_path = os.path.join(root, file)
                model, dre, tone = extract_metadata(file_path)

                if model and dre and ("DRE_ON" in dre or "DRE_OFF" in dre):
                    # Create folder named with Model + DRE
                    folder_name = f"{model}_{dre}"
                    target_dir = os.path.join(root, folder_name)
                    os.makedirs(target_dir, exist_ok=True)

                    # Append ImageTone (and _DR if DRE_ON)
                    base, ext = os.path.splitext(file)
                    if tone:
                        if "DRE_ON" in dre:
                            new_file_name = f"{base}_{tone}_DR{ext}"
                        else:
                            new_file_name = f"{base}_{tone}{ext}"
                    else:
                        new_file_name = file

                    destination = os.path.join(target_dir, new_file_name)

                    # Move file
                    os.rename(file_path, destination)
                    print(f"Moved {file} → {destination}")
                else:
                    print(f"Skipped {file} (missing or invalid DRE/Model)")

if __name__ == "__main__":
    directory_path = r"C:\\change\\path\\to\\whatever"
    sort_by_model_dre_and_tone(directory_path)
    print("RAW files sorted by Model + DRE, and renamed with ImageTone (+_DR for DRE ON).")
