# Python Utilities

This directory contains the Python scripts that drive the software side of the lane-edge detection pipeline:

## Files

- **`bitmap_to_hex.py`**  
  Converts a 24-bit BMP image into a text file of hexadecimal pixel values.  
  **Usage**  
  ```bash
  python bitmap_to_hex.py input.bmp output.txt
lane_fixed.py
Applies a 3×3 Sobel filter directly in Python to an input BMP, producing an edge-map BMP.
Usage

bash
Copy
Edit
python lane_fixed.py input.bmp output_edges.bmp
hex_to_bitmap.py
Reconstructs a BMP image from a text file of hex pixel values.
Usage

bash
Copy
Edit
python hex_to_bitmap.py input.txt output.bmp
How to Verify
Convert a sample image:

bash
Copy
Edit
python bitmap_to_hex.py ../sample-inputs/street_0.bmp street_0_expected.txt
Run the software Sobel:

bash
Copy
Edit
python lane_fixed.py ../sample-inputs/street_0.bmp street_0_python.bmp
Reconstruct from your hex:

bash
Copy
Edit
python hex_to_bitmap.py street_0_expected.txt street_0_reconstructed.bmp
