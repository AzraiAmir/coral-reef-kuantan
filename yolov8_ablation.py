"""
YOLOv8 Ablation Studies
Conducts ablation studies to assess component contributions.
"""

import pandas as pd
from ultralytics import YOLO
from pathlib import Path


class AblationStudy:
    def __init__(self, data_yaml, output_dir='ablation_study'):
        self.data_yaml = data_yaml
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.results = []

    def run_configuration(self, config_name, **kwargs):
        """Run a single ablation configuration."""
        print(f"\n{'='*60}")
        print(f"Running configuration: {config_name}")
        print(f"{'='*60}")

        model = YOLO('yolov8m.pt')

        default_params = {
            'epochs': 100,
            'imgsz': 640,
            'batch': 16,
            'pretrained': True,
            'mosaic': 1.0,
            'mixup': 0.0,
            'copy_paste': 0.0,
            'hsv_h': 0.015,
            'hsv_s': 0.7,
            'hsv_v': 0.4,
        }

        default_params.update(kwargs)

        results = model.train(
            data=self.data_yaml,
            project=str(self.output_dir / config_name),
            name='train',
            verbose=False,
            plots=False,
            **default_params
        )

        metrics = {
            'config': config_name,
            'mAP50': results.results_dict.get('metrics/mAP50(B)', 0),
            'mAP50-95': results.results_dict.get('metrics/mAP50-95(B)', 0),
            'precision': results.results_dict.get('metrics/precision(B)', 0),
            'recall': results.results_dict.get('metrics/recall(B)', 0),
        }

        self.results.append(metrics)
        return metrics

    def run_all_ablations(self):
        """Run all ablation configurations."""
        configurations = [
            ('baseline', {'pretrained': False, 'mosaic': 0.0, 'mixup': 0.0,
                          'copy_paste': 0.0, 'hsv_h': 0.0, 'hsv_s': 0.0, 'hsv_v': 0.0}),
            ('pretrained', {'pretrained': True, 'mosaic': 0.0, 'mixup': 0.0,
                            'copy_paste': 0.0, 'hsv_h': 0.0, 'hsv_s': 0.0, 'hsv_v': 0.0}),
            ('+mosaic', {'pretrained': True, 'mosaic': 1.0, 'mixup': 0.0,
                         'copy_paste': 0.0, 'hsv_h': 0.0, 'hsv_s': 0.0, 'hsv_v': 0.0}),
            ('+mixup', {'pretrained': True, 'mosaic': 1.0, 'mixup': 0.2,
                        'copy_paste': 0.0, 'hsv_h': 0.0, 'hsv_s': 0.0, 'hsv_v': 0.0}),
            ('+copy_paste', {'pretrained': True, 'mosaic': 1.0, 'mixup': 0.2,
                             'copy_paste': 0.5, 'hsv_h': 0.0, 'hsv_s': 0.0, 'hsv_v': 0.0}),
            ('+hsv', {'pretrained': True, 'mosaic': 1.0, 'mixup': 0.2,
                      'copy_paste': 0.5, 'hsv_h': 0.015, 'hsv_s': 0.7, 'hsv_v': 0.4}),
            ('full', {'pretrained': True, 'mosaic': 1.0, 'mixup': 0.2,
                      'copy_paste': 0.5, 'hsv_h': 0.015, 'hsv_s': 0.7, 'hsv_v': 0.4}),
        ]

        for config_name, params in configurations:
            self.run_configuration(config_name, **params)

        # Save results
        df = pd.DataFrame(self.results)
        df.to_csv(self.output_dir / 'ablation_results.csv', index=False)

        # Calculate deltas
        baseline_map = df[df['config'] == 'baseline']['mAP50'].values[0]
        df['delta_mAP50'] = df['mAP50'] - baseline_map
        df.to_csv(self.output_dir / 'ablation_results_with_delta.csv', index=False)

        print("\n" + "=" * 60)
        print("Ablation Study Results")
        print("=" * 60)
        print(df.to_string(index=False))

        return df


if __name__ == "__main__":
    ablation = AblationStudy('coral_dataset.yaml')
    ablation.run_all_ablations()
