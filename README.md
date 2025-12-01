# person_and_licenceplate_blurring
Useful tool to load pictures from a folder and blur all detected persons and licenseplates, for privacy reasons.

## Installation:
- You will need Python 3.9 or later, 3.10 recommended
- Clone this repository **with submodules**  
  run the following to clone everything: `git clone --recurse-submodules https://github.com/kovbando/person_and_licenceplate_blurring.git`
- Preferably use a python virtual environment. `python -m venv venv` then activate your venv!
- If you install all requirements the default version of pytorch will **NOT** use CUDA.\
 If you have a CUDA capable system run `pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121` before instaalling everything else in the next step! 
-  and install dependencies via pip\
  `pip install -r requirements.txt`
- *The steps below are probably redundant, because everything shouldd be handled by the submodule inclusion and requirements.txt*
- YOLOv5:  
  In the project's folder `person_and_licenceplate_blurring`, run:  
  `pip install -U ultralytics`\
- Clone YOLOv5 repository:  
  In the project's folder `person_and_licenceplate_blurring`, run:  
  `git clone https://github.com/ultralytics/yolov5`
- YOLOv5 was added as a submodule, so no need to clone it separately

## Usage:

After successfully installing all dependencies, you can run `python licenseplate_test.py -i <input_folder> -o <output_folder> (-f)`\
This will load all images, regardless of their name or format from the **input_folder**, apply the blurring on all detected licenseplates and persons, and save the resulting image in the **output_folder** as *.jpg*.\
If you enecounter some error regarding the loading of the models, first thing to try is to add the `-f` option to your commmand. It will force a reload of the models, and probably fix any issues.

## Notes:

You should be able to run this the same way on Linux or on Windows. The only difference would be the batch.sh or batch.cmd for batching operations.\
The `convert_serialization.py` can be used to convert explicitly windows formatted *.pt* checkpoints to universally usable checkpoints.

## Sample Images:

Below are some example images included in the `img` folder:

### Dev0_Image_w1920_h1200_fn92.jpg
![Dev0 Image](img/Dev0_Image_w1920_h1200_fn92.jpg)

### Dev1_Image_w1920_h1200_fn262.jpg
![Dev1 Image](img/Dev1_Image_w1920_h1200_fn262.jpg)

### Dev3_Image_w1920_h1200_fn155.jpg
![Dev3 Image](img/Dev3_Image_w1920_h1200_fn155.jpg)

### Dev3_Image_w1920_h1200_fn350.jpg
![Dev3 Image](img/Dev3_Image_w1920_h1200_fn350.jpg)
