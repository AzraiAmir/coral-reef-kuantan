"""
Enhancement Comparison
Compares traditional vs. deep learning enhancement methods.
"""

import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from enhancement_metrics import EnhancementMetrics


class EnhancementComparison:
    def __init__(self, output_dir='enhancement_comparison'):
        self.output_dir = output_dir
        self.metrics = EnhancementMetrics()
        import os
        os.makedirs(output_dir, exist_ok=True)

    def compare_methods(self, original, traditional, deep_learning):
        """Compare traditional and deep learning enhancement."""
        results = {
            'original': {
                'uciqe': self.metrics.calculate_uciqe(original),
                'uiqm': self.metrics.calculate_uiqm(original),
            },
            'traditional': {
                'uciqe': self.metrics.calculate_uciqe(traditional),
                'uiqm': self.metrics.calculate_uiqm(traditional),
            },
            'deep_learning': {
                'uciqe': self.metrics.calculate_uciqe(deep_learning),
                'uiqm': self.metrics.calculate_uiqm(deep_learning),
            },
        }

        return results

    def visualize_comparison(self, original, traditional, deep_learning,
                             output_name='comparison'):
        """Visualize enhancement comparison."""
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))

        axes[0].imshow(cv2.cvtColor(original, cv2.COLOR_BGR2RGB))
        axes[0].set_title('Original', fontsize=12, fontweight='bold')
        axes[0].axis('off')

        axes[1].imshow(cv2.cvtColor(traditional, cv2.COLOR_BGR2RGB))
        axes[1].set_title('Traditional Enhancement', fontsize=12, fontweight='bold')
        axes[1].axis('off')

        axes[2].imshow(cv2.cvtColor(deep_learning, cv2.COLOR_BGR2RGB))
        axes[2].set_title('Deep Learning Enhancement', fontsize=12, fontweight='bold')
        axes[2].axis('off')

        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/{output_name}.png', dpi=300, bbox_inches='tight')
        plt.close()

        return f'{self.output_dir}/{output_name}.png'
