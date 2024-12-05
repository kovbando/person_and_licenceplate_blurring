#this script converts the windows serialization in the trained model into posix based serialization. This allows to run on linux based systems.
# Add YOLOv5 to the Python path
import sys
sys.path.append("D:/Projects/person_and_licenceplate_blurring/yolov5")

import torch
from pathlib import WindowsPath, PosixPath

# Recursive function to replace WindowsPath with strings
def replace_windows_paths(obj):
    if isinstance(obj, WindowsPath):
        return str(obj)  # Convert WindowsPath to string
    elif isinstance(obj, list):
        return [replace_windows_paths(i) for i in obj]  # Handle lists
    elif isinstance(obj, dict):
        return {k: replace_windows_paths(v) for k, v in obj.items()}  # Handle dicts
    else:
        return obj  # Return other types unchanged

# Path to the original and converted checkpoints
original_checkpoint_path = "runs/train/exp12/weights/best.pt"
converted_checkpoint_path = "best_fixed.pt"

# Load, fix, and save the checkpoint
checkpoint = torch.load(original_checkpoint_path, map_location="cpu")
fixed_checkpoint = replace_windows_paths(checkpoint)
torch.save(fixed_checkpoint, converted_checkpoint_path)

print(f"Checkpoint converted and saved as {converted_checkpoint_path}")
