import torch
import cv2
import os
import argparse
import warnings
import sys

# Suppress all FutureWarnings globally
warnings.simplefilter(action='ignore', category=FutureWarning)

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Blur persons and license plates in images.")
parser.add_argument('-i', '--image_folder', type=str, required=True, help='Path to the folder with input images')
parser.add_argument('-o', '--output_dir', type=str, required=True, help='Path to the folder to save blurred images')

# If no arguments are provided, print help and exit
if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    sys.exit(1)

args = parser.parse_args()

image_folder = args.image_folder
output_dir = args.output_dir

# Allowlist YOLOv5 model class for torch.load (PyTorch 2.6+)
torch.serialization.add_safe_globals(['models.yolo.Model'])

# Load models
person_model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
plate_model = torch.hub.load('yolov5', 'custom', path="best_fixed.pt", source='local')

# Ensure output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Get list of image files
image_files = [f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.png', '.bmp'))]
print(f"Found {len(image_files)} image(s) to process.")

person_class_id = 0

try:
    # Process each image
    for image_name in image_files:
        img_path = os.path.join(image_folder, image_name)
        img = cv2.imread(img_path)
    
        person_results = person_model(img)
        person_detections = person_results.xyxy[0].cpu().numpy()
        for *box, conf, class_id in person_detections:
            if int(class_id) == person_class_id:
                x1, y1, x2, y2 = map(int, box)
                x1, y1 = max(0, x1), max(0, y1)
                x2, y2 = min(img.shape[1], x2), min(img.shape[0], y2)
                img[y1:y2, x1:x2] = cv2.GaussianBlur(img[y1:y2, x1:x2], (51, 51), 30)
    
        plate_results = plate_model(img)
        plate_detections = plate_results.xyxy[0].cpu().numpy()
        for *box, conf, class_id in plate_detections:
            x1, y1, x2, y2 = map(int, box)
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(img.shape[1], x2), min(img.shape[0], y2)
            img[y1:y2, x1:x2] = cv2.GaussianBlur(img[y1:y2, x1:x2], (51, 51), 30)
    
#        output_image_path = os.path.join(output_dir, image_name)
#        cv2.imwrite(output_image_path, img)
#        print(f"{output_image_path} saved")
        base_name = os.path.splitext(image_name)[0]
        output_image_path = os.path.join(output_dir, base_name + '.jpg')
#        cv2.imwrite(output_image_path, img)
        cv2.imwrite(output_image_path, img, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
        print(f"{output_image_path} saved")
except KeyboardInterrupt:
    print("\nProcessing interrupted by user. Exiting gracefully.")
    sys.exit(0)

