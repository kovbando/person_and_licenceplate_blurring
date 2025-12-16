# -*- coding: utf-8 -*-
"""
# **Person & License Plate Blurring**
### **Embodied Intelligence — ELTE Budapest**
**Fall Semester 2025**

**Authors:**  
- **Hadj Sassi Emen**  
- **Noah van Potten**

---

This notebook demonstrates how to train a YOLOv5-based detection system for **automatically identifying and blurring people and license plates** in images or video streams.  
The project is developed as part of the **Embodied Intelligence** course at **ELTE Budapest**, Fall 2025.

## 🧠 **Project Overview**

We designed a detection pipeline capable of identifying:

- **Humans**
- **License plates**

Once detected, the regions can be **blurred**.

The system uses:

- **YOLOv5** for object detection  
- **A custom dataset** exported via Roboflow  
- **On-the-fly dataset refactoring** to conform to YOLOv5's structure  

This notebook contains:

1. Dataset download  
2. Automatic dataset cleanup (Roboflow → YOLOv5 fix)  
3. Training the YOLOv5 model  
4. Running inference on test images  
5. Producing anonymized output
"""

"""
Install the dependencies for this project.
"""

import contextlib
# Clone YOLOv5 package
!git clone https://github.com/ultralytics/yolov5.git --quiet
print("YOLOv5 installed succesfully!")

# Install YOLOv5 package dependencies
!pip install -r yolov5/requirements.txt --quiet
print("YOLOv5 package dependecies installed succesfully!")

# Install roboflow package
!pip install roboflow --quiet
print("Roboflow installed succesfully!")

"""
Download the custom dataset from Roboflow
"""

# Import roboflow
from roboflow import Roboflow

# Instantiate the Roboflow wrapper class with your API key
rf = Roboflow(api_key="DA1VlRYxFoKlQWOv8V2b")

# Load the correct workspace and project from your dataset URL
project = rf.workspace("t-ag3gh").project("yolo_model-x5ux3-zilgv")

# Specify project version
version = project.version(1)

# Download the dataset in YOLOv5 format
dataset = version.download("yolov5")

print("\nDataset downloaded successfully!")

import os, yaml, glob

dataset_path = dataset.location.rstrip("/")
yaml_path = f"{dataset_path}/data.yaml"

clean_yaml = {
    "path": dataset_path,
    "train": "train/images",
    "val": "valid/images",
    "test": "test/images",
    "nc": 2,
    "names": ["Human", "LicensePlate"],
}

with open(yaml_path, "w") as f:
    yaml.dump(clean_yaml, f)

# Fix label folders
splits = ["train", "valid", "test"]
for s in splits:
    old = f"{dataset_path}/{s}/labelTxt"
    new = f"{dataset_path}/{s}/labels"
    if os.path.exists(old):
        os.rename(old, new)

print("✔ Data.yaml cleaned and folder structure fixed")

import subprocess, sys, shutil

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["WANDB_DISABLED"] = "true"

def run_training(cfg, run_name):
    """Train YOLOv5 with clean single-line logging."""
    cmd = [
        "python", "/content/yolov5/train.py",
        "--data", yaml_path,
        "--weights", "yolov5s.pt",
        "--img", str(cfg["img"]),
        "--batch", str(cfg["batch"]),
        "--epochs", str(cfg["epochs"]),
        "--project", "/content/yolov5/runs/train",
        "--name", run_name,
        "--exist-ok",
    ]

    if cfg.get("optimizer") == "Adam":
        cmd += ["--optimizer", "Adam"]

    if cfg.get("iou"):
        cmd += ["--iou_t", str(cfg["iou"])]

    if cfg.get("strong_aug"):
        cmd += [
            "--hsv_h", "0.015",
            "--hsv_s", "0.7",
            "--hsv_v", "0.7",
            "--degrees", "10",
            "--translate", "0.2",
            "--scale", "0.7",
        ]

    print(f"\n🚀 Starting Experiment: {run_name}")
    print(f"Settings: {cfg}\n")

    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, bufsize=1
    )

    for raw in process.stdout:
        line = raw.strip()
        if "Epoch" in line or "%" in line:
            sys.stdout.write("\r" + line)
            sys.stdout.flush()

    process.wait()
    print("\n✔ Training complete:", run_name)

    # ZIP results for convenience
    run_dir = f"/content/yolov5/runs/train/{run_name}"
    zip_path = f"/content/{run_name}.zip"
    shutil.make_archive(f"/content/{run_name}", "zip", run_dir)

    print(f" Exported ZIP → {zip_path}")

cfg = {
    "img": 768,
    "batch": 16,
    "epochs": 100,
    "optimizer": "Adam",
    "iou": 0.5,
    "strong_aug": True,
}
run_training(cfg, "custom_training")