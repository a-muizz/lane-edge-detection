# Sample Input Images

This folder provides BMP images to test the pipeline:

- **`street_0.bmp`**  
- **`street_1.bmp`**  
- **`street_2.bmp`**  

Each is a 24-bit BMP (e.g., 640×480) of a road scene containing lane markings.  
Use these files with the Python converter:

```bash
python ../python/bitmap_to_hex.py street_0.bmp street_0_expected.txt
