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
        return iso  # fallback for unexpected values

def extract_metadata(file_path):
    try:
        # Extract ISO, DRE, and Model
        result = subprocess.run(
            ["C:\\exiftool.exe", "-ISO", "-DynamicRangeExpansion", "-Model", "-S", file_path],
            capture_output=True,
            text=True
        )
        lines = result.stdout.strip().splitlines()
        iso, dre, model = None, None, None
        for line in lines:
            if line.startswith("ISO:"):
                iso_str = line.split(":", 1)[1].strip()
                iso = int(iso_str)
            elif line.startswith("DynamicRangeExpansion:"):
                dre_raw = line.split(":", 1)[1].strip()
                if dre_raw.upper() in ["ON", "OFF", "AUTO"]:
                    dre = dre_raw.upper()
                else:
                    dre = dre_raw.replace(";", "_").replace(" ", "_")
            elif line.startswith("Model:"):
                model = line.split(":", 1)[1].strip().replace(" ", "_")
        # Default DRE if missing
        if dre is None:
            dre = "NONE"
        return iso, dre, model
    except Exception as e:
        print(f"Error extracting metadata from {file_path}: {e}")
        return None, None, None

def sort_raw_files_by_iso_dre_model(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.nef', '.cr2', '.arw', '.pef', '.dng')):
                file_path = os.path.join(root, file)
                iso, dre, model = extract_metadata(file_path)
                if iso is not None and model is not None:
                    bucket = iso_bucket(iso)  # group into range
                    # Add camera model in front of the folder
                    dir_name = f"{model}_ISO_{bucket}_DRE_{dre}"
                    iso_dre_dir = os.path.join(root, dir_name)
                    os.makedirs(iso_dre_dir, exist_ok=True)

                    source_path = file_path
                    destination_path = os.path.join(iso_dre_dir, file)
                    os.rename(source_path, destination_path)

                    print(f"Moved {file} -> {iso_dre_dir}")
                else:
                    print(f"Skipped {file} (missing ISO or Model)")

if __name__ == "__main__":
    directory_path = 'C:\\change\\path\\to\\whatever'
    sort_raw_files_by_iso_dre_model(directory_path)
    print("Raw files sorted and moved into grouped Model/ISO/DRE directories.")
