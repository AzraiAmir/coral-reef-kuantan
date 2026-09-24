"""
Traditional Enhancement Pipeline
Implements Red Channel Compensation, Gray-World White Balance, and CLAHE.
"""

import cv2
import numpy as np


class TraditionalEnhancer:
    def __init__(self, clip_limit=2.5, tile_grid_size=(8, 8)):
        self.clip_limit = clip_limit
        self.tile_grid_size = tile_grid_size

    def red_channel_compensation(self, image):
        """Red Channel Compensation (RCC)."""
        b, g, r = cv2.split(image.astype(np.float32))

        avg_r = np.mean(r)
        avg_g = np.mean(g)
        avg_b = np.mean(b)

        r_compensated = r + (avg_g - avg_r) * (1 - r / 255.0) + \
                        (avg_b - avg_r) * (1 - r / 255.0)
        r_compensated = np.clip(r_compensated, 0, 255).astype(np.uint8)

        return cv2.merge([
            b.astype(np.uint8),
            g.astype(np.uint8),
            r_compensated
        ])

    def gray_world_white_balance(self, image):
        """Gray-World White Balance."""
        result = image.astype(np.float32)
        avg_b = np.mean(result[:, :, 0])
        avg_g = np.mean(result[:, :, 1])
        avg_r = np.mean(result[:, :, 2])
        avg_gray = (avg_b + avg_g + avg_r) / 3

        result[:, :, 0] = result[:, :, 0] * (avg_gray / avg_b)
        result[:, :, 1] = result[:, :, 1] * (avg_gray / avg_g)
        result[:, :, 2] = result[:, :, 2] * (avg_gray / avg_r)

        return np.clip(result, 0, 255).astype(np.uint8)

    def clahe_enhancement(self, image):
        """CLAHE (Contrast Limited Adaptive Histogram Equalization)."""
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)

        clahe = cv2.createCLAHE(
            clipLimit=self.clip_limit,
            tileGridSize=self.tile_grid_size
        )
        l_enhanced = clahe.apply(l)

        lab_enhanced = cv2.merge([l_enhanced, a, b])
        return cv2.cvtColor(lab_enhanced, cv2.COLOR_LAB2BGR)

    def enhance(self, image):
        """Apply full enhancement pipeline."""
        img = self.red_channel_compensation(image)
        img = self.gray_world_white_balance(img)
        img = self.clahe_enhancement(img)
        return img

    def enhance_batch(self, image_paths, output_dir):
        """Enhance a batch of images."""
        import os
        os.makedirs(output_dir, exist_ok=True)

        for path in image_paths:
            img = cv2.imread(path)
            enhanced = self.enhance(img)
            output_path = os.path.join(output_dir, os.path.basename(path))
            cv2.imwrite(output_path, enhanced)

        print(f"Enhanced {len(image_paths)} images saved to {output_dir}")
