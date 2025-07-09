#!/bin/bash

python licenseplate_test.py -i /mnt/s/cutbag/syncd/image_0 -o /mnt/s/cutbag/syncd/image_0_blur &
python licenseplate_test.py -i /mnt/s/cutbag/syncd/image_1 -o /mnt/s/cutbag/syncd/image_1_blur &
python licenseplate_test.py -i /mnt/s/cutbag/syncd/image_2 -o /mnt/s/cutbag/syncd/image_2_blur &
python licenseplate_test.py -i /mnt/s/cutbag/syncd/image_3 -o /mnt/s/cutbag/syncd/image_3_blur &
python licenseplate_test.py -i /mnt/s/cutbag/syncd/image_4 -o /mnt/s/cutbag/syncd/image_4_blur &
python licenseplate_test.py -i /mnt/s/cutbag/syncd/image_5 -o /mnt/s/cutbag/syncd/image_5_blur &
wait  # <-- wait for all background jobs to finish