"""
Training Curves
Plots training and validation curves.
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


class TrainingCurves:
    def __init__(self, output_dir='training_curves'):
        self.output_dir = output_dir
        import os
        os.makedirs(output_dir, exist_ok=True)

    def plot_loss_curves(self, train_loss, val_loss, output_name='loss_curves'):
        """Plot training and validation loss curves."""
        fig, ax = plt.subplots(figsize=(10, 6))

        epochs = range(1, len(train_loss) + 1)

        ax.plot(epochs, train_loss, 'b-', label='Training Loss', linewidth=2)
        ax.plot(epochs, val_loss, 'r-', label='Validation Loss', linewidth=2)

        ax.set_xlabel('Epoch', fontsize=12)
        ax.set_ylabel('Loss', fontsize=12)
        ax.set_title('Training and Validation Loss', fontsize=14, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/{output_name}.png', dpi=300, bbox_inches='tight')
        plt.close()

        return f'{self.output_dir}/{output_name}.png'

    def plot_map_curves(self, train_map, val_map, output_name='map_curves'):
        """Plot training and validation mAP curves."""
        fig, ax = plt.subplots(figsize=(10, 6))

        epochs = range(1, len(train_map) + 1)

        ax.plot(epochs, train_map, 'b-', label='Training mAP@50', linewidth=2)
        ax.plot(epochs, val_map, 'r-', label='Validation mAP@50', linewidth=2)

        ax.set_xlabel('Epoch', fontsize=12)
        ax.set_ylabel('mAP@50', fontsize=12)
        ax.set_title('Training and Validation mAP@50', fontsize=14, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/{output_name}.png', dpi=300, bbox_inches='tight')
        plt.close()

        return f'{self.output_dir}/{output_name}.png'

    def plot_combined_curves(self, train_loss, val_loss, train_map, val_map,
                             output_name='combined_curves'):
        """Plot combined loss and mAP curves."""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

        epochs = range(1, len(train_loss) + 1)

        ax1.plot(epochs, train_loss, 'b-', label='Training Loss', linewidth=2)
        ax1.plot(epochs, val_loss, 'r-', label='Validation Loss', linewidth=2)
        ax1.set_xlabel('Epoch', fontsize=12)
        ax1.set_ylabel('Loss', fontsize=12)
        ax1.set_title('Loss Curves', fontsize=14, fontweight='bold')
        ax1.legend(fontsize=10)
        ax1.grid(True, alpha=0.3)

        ax2.plot(epochs, train_map, 'b-', label='Training mAP@50', linewidth=2)
        ax2.plot(epochs, val_map, 'r-', label='Validation mAP@50', linewidth=2)
        ax2.set_xlabel('Epoch', fontsize=12)
        ax2.set_ylabel('mAP@50', fontsize=12)
        ax2.set_title('mAP Curves', fontsize=14, fontweight='bold')
        ax2.legend(fontsize=10)
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/{output_name}.png', dpi=300, bbox_inches='tight')
        plt.close()

        return f'{self.output_dir}/{output_name}.png'
