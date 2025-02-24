# CUDATop

A terminal-based, real-time NVIDIA GPU monitoring tool that provides a visual representation of GPU core utilization using CUDA cores visualization. The program displays detailed information about each GPU in the system, including memory usage, utilization rates, and an interactive visualization of CUDA core activity.

## Features

- Real-time monitoring of multiple NVIDIA GPUs
- Visual representation of CUDA cores with color-coded utilization levels
- Detailed GPU information including:
  - Device name
  - GPU utilization percentage
  - Memory usage (used/total)
  - CUDA core count
- Color-coded core status indicators:
  - Red: High utilization (>75%)
  - Yellow: Medium utilization (25-75%)
  - Green: Low utilization (<25%)
- Auto-refreshing display (1-second intervals)
- Terminal-based user interface using curses library

## Requirements

- Python 3.6 or higher
- NVIDIA GPU with updated drivers
- Required Python packages:
  ```
  pynvml>=11.0.0
  windows-curses>=2.3.0  # For Windows systems only
  ```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/cudatop.git
   cd cudatop
   ```

2. Install required packages:
   ```bash
   pip install pynvml
   pip install windows-curses  # Windows only
   ```

## Usage

Run the program from the command line:
```bash
python cudatop.py
```

### Controls
- Press 'q' to quit the program
- Ctrl+C to force exit

## Technical Details

### Core Components

1. **GPU Initialization (`init_gpus`)**:
   - Initializes NVML (NVIDIA Management Library)
   - Detects and creates handles for all available GPUs

2. **GPU Information Retrieval (`get_gpu_info`)**:
   - Collects device name, utilization rates, memory info, and core count
   - Handles UTF-8 decoding for device names

3. **CUDA Core Visualization (`draw_cuda_cores`)**:
   - Creates a visual grid representation of CUDA cores
   - Implements dynamic sizing based on terminal dimensions
   - Adds randomization to simulate real core activity

4. **Main Loop (`main`)**:
   - Handles terminal display using curses
   - Manages color initialization
   - Implements non-blocking input handling
   - Updates display at 1-second intervals

## Error Handling

The program includes several error handling mechanisms:
- Graceful shutdown of NVML
- Terminal restoration on exit
- Boundary checking for display dimensions
- UTF-8 decoding error handling

## Limitations

- Requires NVIDIA GPU(s)
- Terminal must support color output
- Display quality depends on terminal size
- Randomization in core visualization is for demonstration purposes

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- NVIDIA for NVML library
- Python curses library maintainers
- Contributors to the pynvml package
