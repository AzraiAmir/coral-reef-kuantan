"""
Mask Quality Control
Retains high-confidence masks based on IoU and stability thresholds.
"""

import numpy as np
import pandas as pd


class MaskQualityControl:
    def __init__(self, iou_threshold=0.8, stability_threshold=0.8):
        self.iou_threshold = iou_threshold
        self.stability_threshold = stability_threshold

    def filter_masks(self, masks):
        """Filter masks based on quality thresholds."""
        filtered = []

        for mask in masks:
            if (mask['iou'] >= self.iou_threshold and
                mask['stability'] >= self.stability_threshold):
                filtered.append(mask)

        return filtered

    def calculate_pass_rate(self, masks):
        """Calculate pass rate of mask quality control."""
        passed = self.filter_masks(masks)
        pass_rate = len(passed) / len(masks) * 100 if masks else 0

        return {
            'total_masks': len(masks),
            'passed_masks': len(passed),
            'pass_rate': pass_rate,
        }

    def generate_qc_report(self, masks, output_csv):
        """Generate quality control report."""
        results = []
        for mask in masks:
            results.append({
                'mask_id': mask.get('id', 'unknown'),
                'iou': mask['iou'],
                'stability': mask['stability'],
                'passed_iou': mask['iou'] >= self.iou_threshold,
                'passed_stability': mask['stability'] >= self.stability_threshold,
                'passed_both': (mask['iou'] >= self.iou_threshold and
                               mask['stability'] >= self.stability_threshold),
            })

        df = pd.DataFrame(results)
        df.to_csv(output_csv, index=False)

        return df
