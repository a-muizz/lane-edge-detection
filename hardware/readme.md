# VHDL Sobel Filter

This folder contains the VHDL implementation of a streaming 3×3 Sobel operator.

## Files

- **`sobel.vhd`**  
  Core Sobel filter:  
  - Three line-buffers maintain the 3×3 pixel window  
  - Multiply-accumulate with fixed coefficients  
  - Outputs gradient magnitude per pixel (optionally thresholded)

- **`top_level.vhd`**  
  Wraps the core for textio I/O in simulation:  
  - Reads `street_0_stimuli.txt` or other hex streams  
  - Feeds pixels into `sobel`  
  - Writes out result hex to `street_0_response.txt`

- **`tb_sobel.vhd`** (if present)  
  Testbench demonstrating how to hook up stimuli and capture responses.

## Simulating

1. **Generate stimuli** via the Python tools (in `../python`).  
2. **Run ModelSim/Questa**:  
   ```tcl
   vlog sobel.vhd top_level.vhd tb_sobel.vhd
   vsim tb_sobel
   run -all
3. Inspect street_0_response.txt for the hardware’s output hex.

