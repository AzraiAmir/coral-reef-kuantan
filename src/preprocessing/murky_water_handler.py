"""
Murky Water Handler

Detects, classifies, and enhances murky water images for
coral reef monitoring in turbid nearshore environments.
"""

import cv2
import numpy as np


class MurkyWaterHandler:
    """Detects and enhances murky water imagery."""

    def __init__(self):
        self.thresholds = {
            "clear": (0.0, 0.3),
            "moderately_murky": (0.3, 0.5),
            "murky": (0.5, 0.7),
            "very_murky": (0.7, 1.0),
        }

    def detect_murky_water(self, image):
        """Compute murky water score (0 = clear, 1 = very murky)."""
        if image is None:
            return 0.0

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255.0

        # Metric 1: Low contrast indicates murky water
        contrast = gray.std()
        contrast_score = max(0.0, 1.0 - contrast / 0.3)

        # Metric 2: Blue-green dominance (murky water in Kuantan)
        b, g, r = cv2.split(image.astype(np.float32))
        bg_mean = (b.mean() + g.mean()) / 2
        r_mean = r.mean() + 1e-6
        bg_ratio = bg_mean / r_mean
        bg_score = min(1.0, max(0.0, (bg_ratio - 1.0) / 1.0))

        # Metric 3: Edge density (fewer edges = murkier)
        edges = cv2.Canny((gray * 255).astype(np.uint8), 50, 150)
        edge_density = edges.mean() / 255.0
        edge_score = max(0.0, 1.0 - edge_density / 0.05)

        # Weighted composite
        murky_score = 0.4 * contrast_score + 0.3 * bg_score + 0.3 * edge_score
        return float(np.clip(murky_score, 0.0, 1.0))

    def classify_murky_water(self, murky_score):
        """Classify murky score into categories."""
        for category, (low, high) in self.thresholds.items():
            if low <= murky_score < high:
                return category
        return "unknown"

    def enhance_murky_water(self, image, murky_score):
        """Apply dehazing enhancement based on murky score."""
        if image is None:
            return None

        # Dark Channel Prior dehazing
        dark = np.min(image, axis=2)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
        dark = cv2.erode(dark, kernel)

        # Atmospheric light estimate
        flat_dark = dark.flatten()
        top_indices = flat_dark.argsort()[-int(0.001 * len(flat_dark)):]
        atmospheric = image.reshape(-1, 3)[top_indices].mean(axis=0)

        # Transmission map
        transmission = 1.0 - 0.95 * (dark / (atmospheric.max() + 1e-6))
        transmission = cv2.GaussianBlur(transmission, (15, 15), 0)
        transmission = np.clip(transmission, 0.1, 0.9)

        # Recovery
        enhanced = np.zeros_like(image, dtype=np.float32)
        for c in range(3):
            enhanced[:, :, c] = (
                (image[:, :, c].astype(np.float32) - atmospheric[c])
                / transmission
                + atmospheric[c]
            )

        enhanced = np.clip(enhanced, 0, 255).astype(np.uint8)

        # Additional contrast enhancement for very murky
        if murky_score >= 0.7:
            lab = cv2.cvtColor(enhanced, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
            l = clahe.apply(l)
            enhanced = cv2.cvtColor(cv2.merge([l, a, b]), cv2.COLOR_LAB2BGR)

        return enhanced


if __name__ == "__main__":
    handler = MurkyWaterHandler()
    img = cv2.imread("data/raw/test_images/coral_1.jpg")
    if img is not None:
        score = handler.detect_murky_water(img)
        classification = handler.classify_murky_water(score)
        print(f"Murky score: {score:.3f}")
        print(f"Classification: {classification}")
        enhanced = handler.enhance_murky_water(img, score)
        cv2.imwrite("data/processed/murky_enhanced.jpg", enhanced)