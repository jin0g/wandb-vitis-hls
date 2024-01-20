import argparse
import subprocess
import os
import re
import wandb

parser = argparse.ArgumentParser(description="Vitis HLS and WandB integration tool")

parser.add_argument('--source', type=str, default='kernel.cc', help='Path to the C/C++ source file')
parser.add_argument('--kernel', type=str, default='kernel', help='Name of the top function')
parser.add_argument('--part', type=str, default='xck26-sfvc784-2LV-c', help='Target device part')
parser.add_argument('--hls-period', type=float, default=5.0, help='HLS clock cycle')
parser.add_argument('--vivado-period', type=float, default=5.0, help='Vivado clock cycle')
parser.add_argument('--synth-strategy', type=str, default='default', help='Synthesis strategy')
parser.add_argument('--impl-strategy', type=str, default='default', help='Implementation strategy')

args = parser.parse_args()

# Set environment variables
os.environ['SOURCE'] = args.source
os.environ['KERNEL'] = args.kernel
os.environ['PART'] = args.part
os.environ['HLS_PERIOD'] = str(args.hls_period)
os.environ['VIVADO_PERIOD'] = str(args.vivado_period)
os.environ['SYNTH_STRATEGY'] = args.synth_strategy
os.environ['IMPL_STRATEGY'] = args.impl_strategy

# Initialize WandB
wandb.init(project="wandb-vitis-hls", config=args.__dict__)

# Run the Vitis HLS command
dir = f"build/{args.source}-{args.kernel}-{args.part}-{args.hls_period}-{args.vivado_period}-{args.synth_strategy}-{args.impl_strategy}"
cmd = f"mkdir -p {dir} && cd {dir} && vitis_hls -f ../../script.tcl"
try:
    result = subprocess.run(cmd, check=True, shell=True, text=True, capture_output=True)
except subprocess.CalledProcessError as e:
    print(e.stdout)
    print(e.stderr)
    exit(1)
log = result.stdout

# Parse the log file
resource = {
    "SLICE": int(re.search(r"SLICE:\s*(\d+)(?!.*SLICE:)", log, re.DOTALL).group(1)),
    "LUT": int(re.search(r"LUT:\s*(\d+)(?!.*LUT:)", log, re.DOTALL).group(1)),
    "FF": int(re.search(r"FF:\s*(\d+)(?!.*FF:)", log, re.DOTALL).group(1)),
    "DSP": int(re.search(r"DSP:\s*(\d+)(?!.*DSP:)", log, re.DOTALL).group(1)),
    "BRAM": int(re.search(r"BRAM:\s*(\d+)(?!.*BRAM:)", log, re.DOTALL).group(1)),
    "URAM": int(re.search(r"URAM:\s*(\d+)(?!.*URAM:)", log, re.DOTALL).group(1)),
    "LATCH": int(re.search(r"LATCH:\s*(\d+)(?!.*LATCH:)", log, re.DOTALL).group(1)),
    "SRL": int(re.search(r"SRL:\s*(\d+)(?!.*SRL:)", log, re.DOTALL).group(1)),
    "CLB": int(re.search(r"CLB:\s*(\d+)(?!.*CLB:)", log, re.DOTALL).group(1)),
    "CP": float(re.search(r"CP achieved post-implementation:\s*([\d.]+)", log, re.DOTALL).group(1)),
}

# Log
wandb.log(resource)
