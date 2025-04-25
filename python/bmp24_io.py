# -*- coding: utf-8 -*-
"""
Created on Sun Apr 20 16:44:49 2025

@author: muizza
"""

#!/usr/bin/env python3
"""
bmp24_io.py

Simple and easy‑to‑use functions for handling 24‑bit BMP files:
  - only for BMP files in 24bit format
  - y-index runs top → bottom
  - border protection: get outside image → black (0)
"""

from PIL import Image

def bmp24_open(filename):
    """
    Reads a 24‑bit BMP file.
    Returns: (image, x_size, y_size)
      image   : a list-of-lists of longs (pixel = 0xRRGGBB)
      x_size  : width
      y_size  : height
    """
    img = Image.open(filename)
    img = img.convert("RGB")
    x_size, y_size = img.size

    # allocate 2D array
    image = [[0]*x_size for _ in range(y_size)]

    # fill in row‑major, top→bottom (Pillow’s (0,0) is top‑left)
    for y in range(y_size):
        for x in range(x_size):
            r, g, b = img.getpixel((x, y))
            image[y][x] = (r & 0xFF) << 16 | (g & 0xFF) << 8 | (b & 0xFF)

    return image, x_size, y_size


def bmp24_get(image, x, y, x_size, y_size):
    """
    Border‑protected read:
      if (x,y) out of bounds → returns 0 (black)
      else → returns pixel long 0xRRGGBB
    """
    if x < 0 or x >= x_size or y < 0 or y >= y_size:
        return 0
    return image[y][x]


def bmp24_r(pix):
    """Extract red component (0–255) from long pixel."""
    return (pix >> 16) & 0xFF


def bmp24_g(pix):
    """Extract green component (0–255) from long pixel."""
    return (pix >> 8) & 0xFF


def bmp24_b(pix):
    """Extract blue component (0–255) from long pixel."""
    return pix & 0xFF


def bmp24_put(image, r, g, b, x, y, x_size, y_size):
    """
    Writes a pixel at (x,y). Raises if out of range.
    Packs as 0xRRGGBB.
    """
    if x < 0 or x >= x_size or y < 0 or y >= y_size:
        raise IndexError(f"bmp24_put: coords out of range {x},{y} (max={x_size-1},{y_size-1})")
    image[y][x] = ((r & 0xFF) << 16) | ((g & 0xFF) << 8) | (b & 0xFF)


def bmp24_close(filename, image, x_size, y_size):
    """
    Writes out a 24‑bit BMP file from the in‑memory image array.
    """
    out = Image.new("RGB", (x_size, y_size))
    for y in range(y_size):
        for x in range(x_size):
            pix = bmp24_get(image, x, y, x_size, y_size)
            out.putpixel((x, y), (bmp24_r(pix), bmp24_g(pix), bmp24_b(pix)))
    out.save(filename, format="BMP")
