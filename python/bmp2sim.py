# -*- coding: utf-8 -*-
"""
Created on Sun Apr 20 16:42:43 2025

@author: muizza
"""

#!/usr/bin/env python3
"""
bmp2sim.py

Convert a 24‑bit BMP file into a text file for simulation with a VHDL testbench.
"""

import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("Please install Pillow first: pip install pillow")

def bmp2sim(input_base: str) -> None:
    bmp_path = Path(f"{input_base}.bmp")
    if not bmp_path.is_file():
        sys.exit(f"ERROR: Input file '{bmp_path}' does not exist")

    # Open BMP and convert to RGB if needed
    img = Image.open(bmp_path)
    img = img.convert("RGB")
    width, height = img.size

    txt_path = Path(f"{input_base}.txt")
    try:
        with open(txt_path, "w") as f_out:
            f_out.write(f"# {txt_path.name} - RGB pixel in hex\n")
            pixels = img.load()
            for y in range(height):
                for x in range(width):
                    r, g, b = pixels[x, y]
                    f_out.write(f"{r:02X} {g:02X} {b:02X}\n")
    except IOError as e:
        sys.exit(f"ERROR: Could not write to '{txt_path}': {e}")

    print("OK")

def main():
    if len(sys.argv) != 2:
        print(f"USAGE: {sys.argv[0]} <input file base>")
        sys.exit(1)

    input_base = sys.argv[1]
    print("bmp2sim.py (convert bitmap-file to text-file)")
    print("============================================\n")
    bmp2sim(input_base)

if __name__ == "__main__":
    main()
