"""
D_toWhite Metric
Calculates D_toWhite metric for bleaching severity.
"""

import cv2
import numpy as np


class DToWhiteCalculator:
    def __init__(self):
        self.white_reference = None

    def set_white_reference(self, image, white_patch_bbox):
        """Set white reference patch from colour chart."""
        x1, y1, x2, y2 = white_patch_bbox
        white_patch = image[y1:y2, x1:x2]
        self.white_reference = np.median(white_patch.reshape(-1, 3), axis=0)

    def calculate_d_to_white(self, image, coral_mask):
        """Calculate D_toWhite metric for coral pixels."""
        if self.white_reference is None:
            raise ValueError("White reference not set.")

        lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        lab_white = cv2.cvtColor(
            np.uint8([[self.white_reference]]),
            cv2.COLOR_BGR2LAB
        )[0][0]

        coral_pixels = lab_image[coral_mask > 0]

        if len(coral_pixels) == 0:
            return None

        distances = np.sqrt(np.sum((coral_pixels - lab_white) ** 2, axis=1))
        d_to_white = np.mean(distances)

        return d_to_white
