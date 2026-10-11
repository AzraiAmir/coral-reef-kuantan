"""
Precision-Recall Curves
Generates precision-recall curves for detection model.
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_curve, average_precision_score


class PrecisionRecallCurves:
    def __init__(self, class_names, output_dir='pr_curves'):
        self.class_names = class_names
        self.output_dir = output_dir
        import os
        os.makedirs(output_dir, exist_ok=True)

    def plot_pr_curves(self, y_true, y_scores, output_name='pr_curves'):
        """Plot precision-recall curves for all classes."""
        fig, ax = plt.subplots(figsize=(10, 8))

        for i, class_name in enumerate(self.class_names):
            precision, recall, _ = precision_recall_curve(
                y_true[:, i],
                y_scores[:, i]
            )
            ap = average_precision_score(y_true[:, i], y_scores[:, i])

            ax.plot(recall, precision, label=f'{class_name} (AP={ap:.3f})', linewidth=2)

        ax.set_xlabel('Recall', fontsize=12)
        ax.set_ylabel('Precision', fontsize=12)
        ax.set_title('Precision-Recall Curves', fontsize=14, fontweight='bold')
        ax.legend(loc='best', fontsize=8)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/{output_name}.png', dpi=300, bbox_inches='tight')
        plt.close()

        return f'{self.output_dir}/{output_name}.png'

    def calculate_map(self, y_true, y_scores):
        """Calculate mean average precision."""
        aps = []
        for i in range(len(self.class_names)):
            ap = average_precision_score(y_true[:, i], y_scores[:, i])
            aps.append(ap)

        return {
            'mAP': np.mean(aps),
            'per_class_ap': dict(zip(self.class_names, aps))
        }
