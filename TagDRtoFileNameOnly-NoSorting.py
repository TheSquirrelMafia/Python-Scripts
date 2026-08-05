import os
import subprocess

def extract_dre(file_path):
    """Extract and normalize Dynamic Range Expansion (DRE)."""
    try:
        result = subprocess.run(
            ["C:\\exiftool.exe", "-DynamicRangeExpansion", "-S", file_path],
            capture_output=True,
            text=True
        )

        lines = result.stdout.strip().splitlines()
        dre = None

        for line in lines:
            if line.startswith("DynamicRangeExpansion:"):
                dre_raw = line.split(":", 1)[1].strip().upper()

                # Normalize separators
                dre_clean = (
                    dre_raw
                    .replace(";", "_")
                    .replace(",", "_")
                    .replace(" ", "_")
                )

                # Treat all ON/Enabled variants as ON
                if "ON" in dre_clean or "ENABLED" in dre_clean:
                    dre = "ON"

                # Treat explicit OFF variants as OFF
                elif "OFF" in dre_clean:
                    dre = "OFF"

                else:
                    dre = None

        return dre

    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None


def rename_with_dr(directory):
    """Only rename files in place, no folder sorting."""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.pef', '.dng')):
                file_path = os.path.join(root, file)
                dre = extract_dre(file_path)

                base, ext = os.path.splitext(file)

                # Skip files already ending with _DR
                if base.upper().endswith("_DR"):
                    print(f"Skipped (already tagged): {file}")
                    continue

                # Append _DR only if DRE is ON
                if dre == "ON":
                    new_name = f"{base}_DR{ext}"
                else:
                    new_name = file

                if new_name != file:
                    new_path = os.path.join(root, new_name)
                    os.rename(file_path, new_path)
                    print(f"Renamed: {file} → {new_name}")
                else:
                    print(f"Unchanged: {file}")


if __name__ == "__main__":
    directory_path = 'C:\\change\\path\\to\\whatever'
    rename_with_dr(directory_path)
    print("Finished renaming files with _DR for all ON/Enabled DRE modes.")