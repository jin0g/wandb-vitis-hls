# WandB and Vitis HLS Integration

Use WandB to explore the synthesis parameters of VitisHLS and visualize timing and resources.

## Prerequisites

```bash
pip install wandb
wandb init
```

## Usage

Example command:

```bash
python main.py --source my_source.cc --kernel my_kernel --part xcvu9p-flgb2104-2-i --hls-period 4.5 --vivado-period 4.5 --synth-strategy AreaOptimized_high --impl-strategy Performance_high
```

- `--source`: Path to the C/C++ source file (default: `kernel.cc`)
- `--kernel`: Name of the top function (default: `kernel`)
- `--part`: Target device part (default: `xck26-sfvc784-2LV-c`)
- `--hls-period`: HLS clock cycle (default: 5.0)
- `--vivado-period`: Vivado clock cycle (default: 5.0)
- `--synth-strategy`: Synthesis strategy (default: `default`)
- `--impl-strategy`: Implementation strategy (default: `default`)


## Using Sweep with WandB

```bash
wandb sweep sweep-example.yaml
wandb agent <your_sweep_id>
```
- Multiple wandb agent processes can be launched to search in parallel
- Access wandb.ai to see the synthesis results visualized
