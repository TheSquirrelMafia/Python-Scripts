# Python Scripts
Will sort by Camera name, ISO, & optional D-Range.

There are 2 Python scripts. Both sort by Camera model & ISO. You need to have ExifTool installed in your C: drive or you'll need to provide your own path to where it's at in the line:

result = subprocess.run(
    ["C:\\exiftool.exe", "-ISO", "-Model", "-S", file_path],

You'll have to rename it from exiftool(-k).exe to exiftool.exe alone.

You'll also need to change the path to wherever you plan on placing your RAW files at.

if __name__ == "__main__":
    directory_path = 'C:\\change\\path\\to\\whatever'

So if you have a sorting folder in your D: drive, the path would look something like this:

if __name__ == "__main__":
    directory_path = 'D:\\sorting'

There are supposed to be 2 back slashes in the paths listed above. This README only shows one.

The other Python script provides an additional step by sorting files by D-Range when set to AUTO in the camera. You never know what you'll get when you have the D-Range in your camera set to AUTO. They'll either be ON or OFF. Once you know which files are ON & OFF, you can process them accordingly. If you have D-Range set to LOW, MEDIUM, or HIGH, it's going to place the RAW files within the regular ISO folders. This is only for the AUTO setting. When D-Range is set to AUTO in the camera, sometimes it will kick in & sometimes it won't. Not every singe RAW file is affected by it. It only happens when the camera detects a large amount of contrast in the scene & the ISO is set to at least 200. The D-Range Python script is looking for:

DynamicRangeExpansion: OFF;AUTO;0,0
DynamicRangeExpansion: ON;AUTO;0,0

Inside the EXIF.

Obviously you'll need to have Python installed in your machine. I use Microsoft Visio Studio Code to run my Python scripts. You can use that or whatever you want.

The other 2 scripts do the same thing, but they will append what image tone was used in the RAW file.

D-Range will affect the ability of a RAW converter to get the right contrast, brightness, & exposure. Outside of Digital Camera Utility 5 from Ricoh, all other RAW converters will guesstimate the exposure on D-Range embedded RAW files.
