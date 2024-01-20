# WandB and Vitis HLS Integration

## Overview

This tool integrates Vitis High-Level Synthesis (HLS) with Weights & Biases (WandB) for performing parameter exploration and logging. It allows users to run Vitis HLS with various parameters, capture the resource usage and performance metrics, and log them to WandB for analysis.

## Basic Usage

### Prerequisites

- Vitis HLS installed and configured on your system.
- Python environment with necessary packages (`wandb`, etc.) installed.

### Command Line Arguments

Run the script with the following command-line arguments:

- `--source`: Path to the C/C++ source file (default: `kernel.cc`)
- `--kernel`: Name of the top function (default: `kernel`)
- `--part`: Target device part (default: `xck26-sfvc784-2LV-c`)
- `--hls-period`: HLS clock cycle (default: 5.0)
- `--vivado-period`: Vivado clock cycle (default: 5.0)
- `--synth-strategy`: Synthesis strategy (default: `default`)
- `--impl-strategy`: Implementation strategy (default: `default`)

Example command:

```bash
python your_script.py --source my_source.cc --kernel my_kernel --part xcvu9p-flgb2104-2-i --hls-period 4.5 --vivado-period 4.5 --synth-strategy AreaOptimized_high --impl-strategy Performance_high
```

This will execute the Vitis HLS tool with the specified parameters and log the results to WandB.

## Using Sweep with WandB

### Setting Up a Sweep

1. Define your sweep configuration in a YAML file (e.g., `sweep-config.yaml`). This file should specify the parameters to sweep over and the method (grid search in this case).

Example `sweep-config.yaml`:

```yaml
program: your_script.py
method: grid
parameters:
  hls-period:
    values: [1.0, 1.1, ..., 2.0]
  vivado-period:
    values: [1.0, 1.1, ..., 2.0]
  synth-strategy:
    values: ["Strategy1", "Strategy2", ..., "Strategy5"]
  impl-strategy:
    values: ["Strategy1", "Strategy2", ..., "Strategy5"]
```

2. Initialize the sweep in WandB:

```bash
wandb sweep sweep-config.yaml
```

This will generate a Sweep ID.

3. Start the sweep agent using the generated Sweep ID:

```bash
wandb agent <your_sweep_id>
```

The script will automatically run with all combinations of the specified parameters, and the results will be logged to your WandB project.
