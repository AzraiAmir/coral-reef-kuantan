"""
Enhancement Metrics
Calculates UCIQE and UIQM metrics for image enhancement.
"""

import cv2
import numpy as np
from scipy import stats


class EnhancementMetrics:
    def __init__(self):
        pass

    def calculate_uciqe(self, image):
        """Calculate Underwater Colour Image Quality Evaluation (UCIQE)."""
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)

        # Chroma
        chroma = np.sqrt(a.astype(float)**2 + b.astype(float)**2)
        sigma_c = np.std(chroma)

        # Luminance contrast
        con_l = np.std(l)

        # Average saturation
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        s = hsv[:, :, 1]
        mu_s = np.mean(s)

        # UCIQE formula
        uciqe = 0.4680 * sigma_c + 0.2745 * con_l + 0.2576 * mu_s

        return uciqe

    def calculate_uiqm(self, image):
        """Calculate Underwater Image Quality Measure (UIQM)."""
        # UICM (Underwater Image Colourfulness Measure)
        r, g, b = cv2.split(image.astype(float))
        rg = r - g
        yb = 0.5 * (r + g) - b

        uicm = np.sqrt(np.std(rg)**2 + np.std(yb)**2) + \
               0.3 * np.sqrt(np.mean(rg)**2 + np.mean(yb)**2)

        # UISM (Underwater Image Sharpness Measure)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        uism = np.mean(np.sqrt(sobel_x**2 + sobel_y**2))

        # UIConM (Underwater Image Contrast Measure)
        uiconm = np.std(gray)

        # UIQM formula
        uiqm = 0.0282 * uicm + 0.2953 * uism + 3.5753 * uiconm

        return uiqm

    def compare_enhancement(self, original, enhanced):
        """Compare enhancement methods."""
        return {
            'original': {
                'uciqe': self.calculate_uciqe(original),
                'uiqm': self.calculate_uiqm(original),
            },
            'enhanced': {
                'uciqe': self.calculate_uciqe(enhanced),
                'uiqm': self.calculate_uiqm(enhanced),
            },
            'improvement': {
                'uciqe': self.calculate_uciqe(enhanced) - self.calculate_uciqe(original),
                'uiqm': self.calculate_uiqm(enhanced) - self.calculate_uiqm(original),
            }
        }
