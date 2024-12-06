import torch
import cv2
import os
import warnings

person_model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
plate_model = torch.hub.load('yolov5', 'custom', path="best_fixed.pt", source='local')

#this is to supress "FutureWarning: `torch.cuda.amp.autocast(args...)` is deprecated. Please use `torch.amp.autocast('cuda', args...)` instead."
warnings.filterwarnings(
    "ignore", 
    category=FutureWarning, 
    message=r"`torch\.cuda\.amp\.autocast\(.*\)` is deprecated"
)


image_folder = "images"
output_dir = 'output_images'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

image_files = [f for f in os.listdir(image_folder) if f.endswith('.jpg')]

person_class_id = 0

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

            roi = img[y1:y2, x1:x2]

            blurred_roi = cv2.GaussianBlur(roi, (51, 51), 30)

            img[y1:y2, x1:x2] = blurred_roi

    plate_results = plate_model(img)
    plate_detections = plate_results.xyxy[0].cpu().numpy()
    for *box, conf, class_id in plate_detections:
        x1, y1, x2, y2 = map(int, box)
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(img.shape[1], x2), min(img.shape[0], y2)

        roi = img[y1:y2, x1:x2]

        blurred_roi = cv2.GaussianBlur(roi, (51, 51), 30)

        img[y1:y2, x1:x2] = blurred_roi


    output_image_path = os.path.join(output_dir, image_name)
    cv2.imwrite(output_image_path, img)

    print(f"{output_image_path} saved")
