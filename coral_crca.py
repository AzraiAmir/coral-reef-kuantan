"""
Coral-CRCA: Colour-Reference Chart Automation Algorithm
Quantitative Bleaching Severity Assessment.
"""

import cv2
import numpy as np
from sklearn.cluster import KMeans
import easyocr
from PIL import Image
import torch


class CoralCRCA:
    def __init__(self, use_gpu=True):
        self.device = 'cuda' if (use_gpu and torch.cuda.is_available()) else 'cpu'
        self.ocr_reader = easyocr.Reader(['en'], gpu=use_gpu)

        self.reference_colors = {
            'C1': (255, 255, 255),
            'C2': (255, 245, 230),
            'C3': (255, 235, 210),
            'C4': (245, 220, 190),
            'C5': (230, 200, 170),
            'C6': (210, 180, 150),
        }

        self.kbi_thresholds = {
            'healthy': (0.0, 0.2),
            'mild_bleaching': (0.2, 0.4),
            'moderate_bleaching': (0.4, 0.6),
            'severe_bleaching': (0.6, 0.8),
            'critical_bleaching': (0.8, 1.0),
        }

    def detect_colour_chart(self, image):
        """Detect colour reference chart using OCR."""
        results = self.ocr_reader.readtext(image)

        chart_bbox = None
        detected_labels = []

        for (bbox, text, conf) in results:
            if text.upper() in self.reference_colors or \
               any(c in text.upper() for c in ['C1', 'C2', 'C3', 'C4', 'C5', 'C6']):
                detected_labels.append((bbox, text, conf))

        if detected_labels:
            all_x = [p[0] for bbox, _, _ in detected_labels for p in bbox]
            all_y = [p[1] for bbox, _, _ in detected_labels for p in bbox]
            chart_bbox = (min(all_x), min(all_y), max(all_x), max(all_y))

        return chart_bbox, detected_labels

    def extract_reference_colors(self, image, chart_bbox):
        """Extract reference colours from the colour chart."""
        if chart_bbox is None:
            return self.reference_colors

        x1, y1, x2, y2 = chart_bbox
        chart_region = image[y1:y2, x1:x2]

        h, w = chart_region.shape[:2]
        panel_h, panel_w = h // 2, w // 3

        extracted_colors = {}
        labels = list(self.reference_colors.keys())

        for i in range(2):
            for j in range(3):
                idx = i * 3 + j
                if idx < len(labels):
                    panel = chart_region[
                        i*panel_h:(i+1)*panel_h,
                        j*panel_w:(j+1)*panel_w
                    ]
                    median_color = np.median(panel.reshape(-1, 3), axis=0)
                    extracted_colors[labels[idx]] = tuple(median_color.astype(int))

        return extracted_colors

    def segment_coral(self, image, coral_mask=None):
        """Segment coral region from background."""
        if coral_mask is not None:
            return coral_mask

        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        lower_coral = np.array([0, 30, 50])
        upper_coral = np.array([180, 255, 255])

        mask = cv2.inRange(hsv, lower_coral, upper_coral)

        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        return mask

    def assign_colour_codes(self, image, coral_mask, reference_colors):
        """Assign colour codes to each pixel in the coral region."""
        coral_pixels = image[coral_mask > 0]

        if len(coral_pixels) == 0:
            return {}

        ref_codes = list(reference_colors.keys())
        ref_colors_array = np.array([reference_colors[code] for code in ref_codes])

        colour_assignments = {code: 0 for code in ref_codes}

        for pixel in coral_pixels:
            distances = np.sqrt(np.sum((ref_colors_array - pixel) ** 2, axis=1))
            closest_idx = np.argmin(distances)
            colour_assignments[ref_codes[closest_idx]] += 1

        total = sum(colour_assignments.values())
        colour_percentages = {
            code: (count / total) * 100
            for code, count in colour_assignments.items()
        }

        return colour_percentages

    def calculate_bleaching_severity(self, colour_percentages):
        """Calculate Kuantan Bleaching Index (KBI)."""
        weights = {
            'C1': 1.0,
            'C2': 0.8,
            'C3': 0.6,
            'C4': 0.4,
            'C5': 0.2,
            'C6': 0.0,
        }

        kbi = sum(
            weights.get(code, 0) * pct / 100
            for code, pct in colour_percentages.items()
        )

        return kbi

    def classify_health_status(self, kbi):
        """Classify health status based on KBI value."""
        for status, (low, high) in self.kbi_thresholds.items():
            if low <= kbi < high:
                return status
        return 'unknown'

    def analyze(self, image_path, coral_mask=None):
        """Full analysis pipeline for a single image."""
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not load image: {image_path}")

        chart_bbox, chart_labels = self.detect_colour_chart(image)
        reference_colors = self.extract_reference_colors(image, chart_bbox)
        mask = self.segment_coral(image, coral_mask)
        colour_percentages = self.assign_colour_codes(image, mask, reference_colors)
        kbi = self.calculate_bleaching_severity(colour_percentages)
        health_status = self.classify_health_status(kbi)

        return {
            'image_path': image_path,
            'chart_detected': chart_bbox is not None,
            'colour_percentages': colour_percentages,
            'bleaching_severity_index': kbi,
            'health_status': health_status,
        }
