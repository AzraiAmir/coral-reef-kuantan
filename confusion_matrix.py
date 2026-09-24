"""
Confusion Matrix
Generates confusion matrices for detection model.
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report


class ConfusionMatrixGenerator:
    def __init__(self, class_names, output_dir='confusion_matrices'):
        self.class_names = class_names
        self.output_dir = output_dir
        import os
        os.makedirs(output_dir, exist_ok=True)

    def generate_confusion_matrix(self, y_true, y_pred, output_name='confusion_matrix'):
        """Generate confusion matrix."""
        cm = confusion_matrix(y_true, y_pred)

        fig, ax = plt.subplots(figsize=(12, 10))

        sns.heatmap(
            cm,
            annot=True,
            fmt='d',
            cmap='Blues',
            xticklabels=self.class_names,
            yticklabels=self.class_names,
            ax=ax
        )

        ax.set_xlabel('Predicted', fontsize=12, fontweight='bold')
        ax.set_ylabel('Actual', fontsize=12, fontweight='bold')
        ax.set_title('Confusion Matrix', fontsize=14, fontweight='bold')

        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/{output_name}.png', dpi=300, bbox_inches='tight')
        plt.close()

        return cm

    def generate_normalized_confusion_matrix(self, y_true, y_pred,
                                             output_name='normalized_confusion_matrix'):
        """Generate normalized confusion matrix."""
        cm = confusion_matrix(y_true, y_pred, normalize='true')

        fig, ax = plt.subplots(figsize=(12, 10))

        sns.heatmap(
            cm,
            annot=True,
            fmt='.2f',
            cmap='Blues',
            xticklabels=self.class_names,
            yticklabels=self.class_names,
            ax=ax
        )

        ax.set_xlabel('Predicted', fontsize=12, fontweight='bold')
        ax.set_ylabel('Actual', fontsize=12, fontweight='bold')
        ax.set_title('Normalized Confusion Matrix', fontsize=14, fontweight='bold')

        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/{output_name}.png', dpi=300, bbox_inches='tight')
        plt.close()

        return cm

    def generate_classification_report(self, y_true, y_pred):
        """Generate classification report."""
        report = classification_report(
            y_true,
            y_pred,
            target_names=self.class_names,
            output_dict=True
        )

        return report
