#!/usr/bin/env python3
"""
lane_fixed.py

2‑dimensional fixed‑point Sobel edge filter for lane detection.
"""

import sys
import math
from pathlib import Path
from PIL import Image

def load_image(path):
    img = Image.open(path).convert("RGB")
    return img, img.width, img.height

def get_pixel_safe(img, x, y):
    """Return (r,g,b), or (0,0,0) if out of bounds."""
    if x < 0 or x >= img.width or y < 0 or y >= img.height:
        return (0, 0, 0)
    return img.getpixel((x, y))

def lane_fixed(input_base: str):
    bmp_in = Path(f"{input_base}.bmp")
    if not bmp_in.is_file():
        sys.exit(f"ERROR: '{bmp_in}' not found")
    img_in, width, height = load_image(bmp_in)

    img_out = Image.new("RGB", (width, height))
    px_out = img_out.load()

    for y in range(height):
        for x in range(width):
            # fetch the 3×3 neighborhood
            lt = get_pixel_safe(img_in, x-1, y-1)
            ct = get_pixel_safe(img_in, x  , y-1)
            rt = get_pixel_safe(img_in, x+1, y-1)
            lc = get_pixel_safe(img_in, x-1, y  )
            rc = get_pixel_safe(img_in, x+1, y  )
            lb = get_pixel_safe(img_in, x-1, y+1)
            cb = get_pixel_safe(img_in, x  , y+1)
            rb = get_pixel_safe(img_in, x+1, y+1)

            # compute luminances with fixed weights
            def lum(p):
                r, g, b = p
                return 5*r + 9*g + 2*b

            lum_lt = lum(lt)
            lum_ct = lum(ct)
            lum_rt = lum(rt)
            lum_lc = lum(lc)
            lum_rc = lum(rc)
            lum_lb = lum(lb)
            lum_cb = lum(cb)
            lum_rb = lum(rb)

            # Sobel kernels (x and y)
            sum_x = ( lum_rt + 2*lum_rc + lum_rb ) - ( lum_lt + 2*lum_lc + lum_lb )
            sum_y = ( lum_lt + 2*lum_ct + lum_rt ) - ( lum_lb + 2*lum_cb + lum_rb )

            # gradient magnitude squared (scaled by 256)
            gsq256 = sum_x*sum_x + sum_y*sum_y

            # downscale by 256
            gsq = gsq256 // 256

            # clamp to 18‑bit maximum (262143)
            glim = min(gsq, 262143)

            # quantize to 13‑bit granularity
            g13 = 32 * (glim // 32)

            # integer gradient = floor(sqrt(g13) / 2)
            gint = int(math.sqrt(g13) / 2)

            # invert to make edges dark on light background
            lum_new = 255 - gint

            # write output pixel (greyscale)
            px_out[x, y] = (lum_new, lum_new, lum_new)

    out_path = Path(f"{input_base}_edge_fixed.bmp")
    img_out.save(out_path, format="BMP")
    print("OK")

def main():
    if len(sys.argv) != 2:
        print(f"USAGE: {sys.argv[0]} <input file base>")
        sys.exit(1)
    print("lane_fixed.py (fixed‑point Sobel edge filter)\n")
    lane_fixed(sys.argv[1])

if __name__ == "__main__":
    main()
