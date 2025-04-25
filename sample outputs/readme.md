# Sample Outputs

After running the pipeline, you’ll find:

- **`street_0_expected.txt`**  
  Hex stream produced by `bmp2sim.py` (software reference).

- **`street_0_stimuli.txt`**  
  Same as above, renamed for hardware input.

- **`street_0_response.txt`**  
  Hex stream output from the VHDL Sobel filter.

- **`street_A_hardware.bmp`**  
  Reconstructed BMP from `street_0_response.txt` via `sim2bmp.py`.

- **`street_A_python.bmp`**  
  Output BMP from the Python Sobel (`lane_fixed.py`).  
  *(Note: “street_0” and “street_A” refer to the same scene.)*

## Quick Comparison

Use any image viewer to compare:

```bash
# Python result
display street_A_python.bmp

# Hardware result
display street_A_hardware.bmp
This lets you visually verify that the hardware matches the software reference.
---

Feel free to tweak descriptions or usage examples to match any local paths or specific file names.
