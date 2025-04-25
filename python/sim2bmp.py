#!/usr/bin/env python3
"""
sim2bmp.py

Convert a text-file from VHDL-testbench simulation into a 1280×720 BMP image.
Accepts any whitespace layout (one or three hex values per line, etc).
If the input is shorter than expected (e.g. border pixels omitted), pads missing values with 0x00.
"""

import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("Please install Pillow first: pip install pillow")

WIDTH, HEIGHT = 1280, 720
PIXELS = WIDTH * HEIGHT

def sim2bmp(input_base: str):
    txt_path = Path(f"{input_base}.txt")
    if not txt_path.is_file():
        sys.exit(f"ERROR: File '{txt_path}' does not exist")

    # Read header then all remaining tokens (whitespace‑split)
    with txt_path.open() as f:
        _header = f.readline()
        tokens = f.read().split()

    expected = PIXELS * 3
    actual = len(tokens)
    if actual < expected:
        missing = expected - actual
        print(f"WARNING: Found only {actual} hex values, expected {expected}; padding {missing} zeros")
        tokens += ['00'] * missing
    elif actual > expected:
        # extra tokens get ignored
        tokens = tokens[:expected]

    img = Image.new("RGB", (WIDTH, HEIGHT))
    px  = img.load()

    for i in range(PIXELS):
        idx = 3 * i
        chunk = tokens[idx:idx+3]
        try:
            r, g, b = (int(chunk[j], 16) for j in range(3))
        except ValueError:
            sys.exit(f"ERROR: Invalid hex value in tokens[{idx}:{idx+3}]: {chunk}")

        x = i % WIDTH
        y = i // WIDTH
        px[x, y] = (r, g, b)

    bmp_path = Path(f"{input_base}.bmp")
    img.save(bmp_path, format="BMP")
    print("OK")


def main():
    if len(sys.argv) != 2:
        print(f"USAGE: {sys.argv[0]} <input file base>")
        sys.exit(1)
    print("sim2bmp.py (convert text-file to bitmap-file)\n")
    sim2bmp(sys.argv[1])


if __name__ == "__main__":
    main()
