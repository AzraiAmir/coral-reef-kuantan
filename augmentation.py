"""
Data Augmentation Pipeline
Applies geometric, photometric, and advanced augmentations.
"""

import cv2
import numpy as np
import random
from albumentations import (
    Compose, RandomScale, HorizontalFlip, Rotate,
    RandomBrightnessContrast, HueSaturationValue
)


class CoralAugmenter:
    def __init__(self):
        self.transform = Compose([
            RandomScale(scale_limit=0.2, p=0.5),
            HorizontalFlip(p=0.5),
            Rotate(limit=15, p=0.5),
            RandomBrightnessContrast(
                brightness_limit=0.2,
                contrast_limit=0.2,
                p=0.5
            ),
            HueSaturationValue(
                hue_shift_limit=15,
                sat_shift_limit=70,
                val_shift_limit=40,
                p=0.5
            ),
        ])

    def augment(self, image, bboxes=None, class_labels=None):
        """Apply augmentation to image and annotations."""
        if bboxes is not None:
            augmented = self.transform(
                image=image,
                bboxes=bboxes,
                class_labels=class_labels
            )
            return augmented['image'], augmented['bboxes'], augmented['class_labels']
        else:
            augmented = self.transform(image=image)
            return augmented['image']
