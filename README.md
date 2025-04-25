# lane-edge-detection# Lane Edge Detection

This repository implements a 3×3 Sobel‐based edge detector for road-lane images, combining a Python preprocessing/postprocessing pipeline with a VHDL hardware filter. It’s based on the FPGA Vision Lab developed by Professor Marco Winzker.

---

## Repository Structure

├── python/ # Python scripts for BMP↔hex conversion and software Sobel ├── hardware/ # VHDL design for 3×3 Sobel filter ├── sample-inputs/ # BMP images of road lanes └── sample-outputs/ # ├── street_0_expected.txt # expected hex from python ├── street_0_stimuli.txt # stimuli hex for hardware ├── street_0_response.txt # hardware output hex ├── street_A_hardware.bmp # reconstructed BMP from hardware └── street_A_python.bmp # reconstructed BMP from Python


---

## How It Works

1. **Pre-Processing (Python)**  
   - **`bitmap_to_hex.py`**: Reads a BMP image, extracts pixel bytes, writes a text file of hex values.  
   - **`lane_fixed.py`**: Applies a 3×3 Sobel filter directly in Python (software reference).  
   - **`hex_to_bitmap.py`**: Reconstructs a BMP from a hex bitstream.

2. **Hardware Filtering (VHDL)**  
   - **`hardware/sobel.vhd`**: Implements the 3×3 Sobel operator in a streaming pipeline.  
   - **`hardware/top_level.vhd`**: Instantiates the Sobel core, interfaces to hex stimuli and response files.

3. **Post-Processing (Python)**  
   - Convert the hardware’s output hex stream back into a BMP to visualize the edge map.

---

## What Is Sobel Filtering?

The **Sobel operator** approximates the image gradient using two 3×3 convolution kernels:

Gx = [ –1, 0, +1 –2, 0, +2 –1, 0, +1 ]

Gy = [ +1, +2, +1 0, 0, 0 –1, –2, –1 ]


- Convolve the image with **Gx** and **Gy**, compute the gradient magnitude per pixel:  
  $$ \|G\| = \sqrt{Gx^2 + Gy^2} $$  
- High gradient magnitudes correspond to edges.  
- In hardware, the square-root can be approximated or omitted for thresholding.

---

## Important Code Highlights

- **`python/bitmap_to_hex.py`**  
  Streamlines BMP reading and hex export (handles header vs. pixel data).

- **`python/lane_fixed.py`**  
  Demonstrates the 3×3 Sobel in pure Python—useful for verification against hardware.

- **`hardware/sobel.vhd`**  
  - **Line buffering**: three row buffers to supply a 3×3 window each cycle.  
  - **Convolution**: multiplies and accumulates with constant coefficients.  
  - **Pipeline registers**: achieve one‐pixel‐per‐clock throughput.

- **`hardware/top_level.vhd`**  
  Hooks the Sobel core to file-I/O on ModelSim or other simulators via textio.

---

## Next Steps

While Sobel filtering highlights all edges, isolating lane markings typically requires a **Hough Transform** to detect straight lines in the edge map. Integrating a Hough module (e.g., in hardware or software) will allow robust lane identification under varying conditions.

---

## References

- **FPGA Vision Lab** by Prof. Marco Winzker  
  https://www.h-brs.de/de/fpga-vision-lab

- **YouTube Playlist** (Marco Winzker’s lab):  
  https://www.youtube.com/watch?v=-H7moO09tCg&list=PLGzeDuLmmxDq5ErLABOdJkdFO3imtwUqJ&ab_channel=MarcoWinzker%28Professor%29

- **Sobel operator** (Wikipedia):  
  https://en.wikipedia.org/wiki/Sobel_operator

- **Hough transform** (Wikipedia):  
  https://en.wikipedia.org/wiki/Hough_transform
