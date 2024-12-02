# person_and_licenceplate_detection

## Installation:

- Python 3.9 or later
- Pytorch: On Windows, run  
  `pip3 install torch torchvision torchaudio`
- OpenCV:  
  `pip install opencv-python`
- YOLOv5:  
  In the project's folder, run:  
  `pip install -U ultralytics`
- Clone YOLOv5 repository:  
  In the project's folder, run:  
  `git clone https://github.com/ultralytics/yolov5`

## Usage:

1. Create a directory at the same level as the `licenseplate_test.py` file.  
2. Add the images you want to blur to this directory.  
3. Run:  
   `python licenseplate.py`  
   This will create an `output_images` folder with the blurred images.
