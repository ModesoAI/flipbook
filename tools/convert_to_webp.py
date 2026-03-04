# /// script
# dependencies = [
#   "Pillow",
# ]
# ///

import os
import argparse
from PIL import Image
from pathlib import Path

def convert_to_webp(input_dir, output_dir, quality=80):
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    png_files = sorted(list(input_path.glob("*.png")))
    if not png_files:
        print(f"No PNG files found in {input_path}")
        return

    print(f"Converting {len(png_files)} frames to WebP in {output_path}...")
    for png_file in png_files:
        img = Image.open(png_file)
        webp_filename = png_file.stem + ".webp"
        img.save(output_path / webp_filename, "WEBP", quality=quality)
    print("Conversion complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert PNG frames to WebP")
    parser.add_argument("--input", required=True, help="Directory containing PNG frames")
    parser.add_argument("--output", required=True, help="Directory to save WebP frames")
    parser.add_argument("--quality", type=int, default=80, help="WebP quality (0-100)")
    
    args = parser.parse_args()
    convert_to_webp(args.input, args.output, args.quality)
