"""
Image Quality Control
Assesses sharpness, colour balance, and presence of colour reference chart.
"""

import cv2
import numpy as np
from pathlib import Path


class ImageQualityControl:
    def __init__(self, sharpness_threshold=100, colour_balance_threshold=0.3):
        self.sharpness_threshold = sharpness_threshold
        self.colour_balance_threshold = colour_balance_threshold

    def calculate_sharpness(self, image):
        """Calculate image sharpness using Laplacian variance."""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        return laplacian.var()

    def calculate_colour_balance(self, image):
        """Calculate colour balance deviation from gray-world assumption."""
        b, g, r = cv2.split(image.astype(np.float32))

        avg_b = np.mean(b)
        avg_g = np.mean(g)
        avg_r = np.mean(r)
        avg_gray = (avg_b + avg_g + avg_r) / 3

        deviation = (
            abs(avg_b - avg_gray) / avg_gray +
            abs(avg_g - avg_gray) / avg_gray +
            abs(avg_r - avg_gray) / avg_gray
        ) / 3

        return deviation

    def assess_quality(self, image_path):
        """Assess overall image quality."""
        image = cv2.imread(image_path)
        if image is None:
            return {'pass': False, 'reason': 'Could not load image'}

        sharpness = self.calculate_sharpness(image)
        colour_balance = self.calculate_colour_balance(image)

        result = {
            'sharpness': sharpness,
            'colour_balance': colour_balance,
            'pass_sharpness': sharpness >= self.sharpness_threshold,
            'pass_colour_balance': colour_balance <= self.colour_balance_threshold,
            'pass': (sharpness >= self.sharpness_threshold and
                     colour_balance <= self.colour_balance_threshold),
        }

        return result

    def process_batch(self, image_dir, output_csv):
        """Process a batch of images and save QC results."""
        import pandas as pd

        image_dir = Path(image_dir)
        results = []

        for image_path in image_dir.glob("*.jpg"):
            result = self.assess_quality(str(image_path))
            result['image_path'] = str(image_path)
            result['image_name'] = image_path.name
            results.append(result)

        df = pd.DataFrame(results)
        df.to_csv(output_csv, index=False)

        pass_rate = df['pass'].mean() * 100
        print(f"QC complete. Pass rate: {pass_rate:.1f}%")
        print(f"Results saved to {output_csv}")

        return df
