import os
import subprocess
import re


def extract_metadata(file_path):
    """Extract ImageTone + DRE from EXIF."""
    try:
        result = subprocess.run(
            ["C:\\exiftool.exe", "-DynamicRangeExpansion", "-ImageTone", "-S", file_path],
            capture_output=True,
            text=True
        )

        lines = result.stdout.strip().splitlines()
        dre = None
        tone = None

        for line in lines:
            # Image Tone
            if line.startswith("ImageTone:"):
                tone = line.split(":", 1)[1].strip().replace(" ", "_")

            # DRE
            elif line.startswith("DynamicRangeExpansion:"):
                dre_raw = line.split(":", 1)[1].strip().upper().replace(";", "_").replace(",", "_").replace(" ", "_")

                if re.search(r"\bON\b", dre_raw) or re.search(r"ON.*AUTO.*0.*0", dre_raw):
                    dre = "ON"
                elif re.search(r"\bOFF\b", dre_raw):
                    dre = "OFF"
                else:
                    dre = None

        return tone, dre

    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None, None


def rename_with_tone_and_dr(directory):
    """Rename files: ImageTone first, then _DR if ON."""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.pef', '.dng')):
                file_path = os.path.join(root, file)

                tone, dre = extract_metadata(file_path)

                base, ext = os.path.splitext(file)

                new_name_parts = [base]

                # 1. Append ImageTone first
                if tone:
                    new_name_parts.append(tone)

                # 2. Append DR after tone
                if dre == "ON":
                    new_name_parts.append("DR")

                new_name = "_".join(new_name_parts) + ext

                if new_name != file:
                    new_path = os.path.join(root, new_name)
                    os.rename(file_path, new_path)
                    print(f"Renamed: {file} → {new_name}")
                else:
                    print(f"Unchanged: {file}")


if __name__ == "__main__":
    directory_path = 'C:\\change\\path\\to\\whatever'
    rename_with_tone_and_dr(directory_path)
    print("Finished renaming files with ImageTone + _DR (if ON).")
    