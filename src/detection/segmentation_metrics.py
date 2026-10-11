"""
Segmentation Metrics
Calculates IoU, Dice, and stability scores for segmentation.
"""

import numpy as np


class SegmentationMetrics:
    def __init__(self):
        pass

    def calculate_iou(self, pred_mask, true_mask):
        """Calculate Intersection over Union (IoU)."""
        intersection = np.logical_and(pred_mask, true_mask).sum()
        union = np.logical_or(pred_mask, true_mask).sum()

        if union == 0:
            return 0.0

        return intersection / union

    def calculate_dice(self, pred_mask, true_mask):
        """Calculate Dice coefficient."""
        intersection = np.logical_and(pred_mask, true_mask).sum()
        total = pred_mask.sum() + true_mask.sum()

        if total == 0:
            return 0.0

        return 2 * intersection / total

    def calculate_stability(self, pred_mask, true_mask):
        """Calculate stability score based on mask similarity."""
        iou = self.calculate_iou(pred_mask, true_mask)
        dice = self.calculate_dice(pred_mask, true_mask)

        return (iou + dice) / 2

    def evaluate_segmentation(self, pred_mask, true_mask):
        """Evaluate segmentation performance."""
        return {
            'iou': self.calculate_iou(pred_mask, true_mask),
            'dice': self.calculate_dice(pred_mask, true_mask),
            'stability': self.calculate_stability(pred_mask, true_mask),
        }
