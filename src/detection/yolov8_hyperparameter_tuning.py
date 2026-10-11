"""
YOLOv8 Hyperparameter Tuning
Hyperparameter tuning using grid search and Bayesian optimisation.
"""

import optuna
from ultralytics import YOLO
import json
from pathlib import Path


class HyperparameterTuner:
    def __init__(self, data_yaml, output_dir='hyperparameter_tuning'):
        self.data_yaml = data_yaml
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.best_params = None
        self.best_value = None

    def objective(self, trial):
        """Objective function for Optuna optimisation."""
        # Suggest hyperparameters
        lr0 = trial.suggest_float('lr0', 1e-4, 1e-2, log=True)
        lrf = trial.suggest_float('lrf', 0.001, 0.1, log=True)
        momentum = trial.suggest_float('momentum', 0.8, 0.98)
        weight_decay = trial.suggest_float('weight_decay', 1e-5, 1e-3, log=True)
        warmup_epochs = trial.suggest_int('warmup_epochs', 1, 5)
        box = trial.suggest_float('box', 5.0, 10.0)
        cls = trial.suggest_float('cls', 0.3, 0.8)
        batch = trial.suggest_categorical('batch', [8, 16, 32])

        model = YOLO('yolov8m.pt')

        results = model.train(
            data=self.data_yaml,
            epochs=50,
            imgsz=640,
            batch=batch,
            lr0=lr0,
            lrf=lrf,
            momentum=momentum,
            weight_decay=weight_decay,
            warmup_epochs=warmup_epochs,
            box=box,
            cls=cls,
            project=str(self.output_dir / 'trials'),
            name=f'trial_{trial.number}',
            verbose=False,
            plots=False,
        )

        return results.results_dict.get('metrics/mAP50(B)', 0)

    def tune(self, n_trials=20, timeout_hours=24):
        """Run hyperparameter tuning."""
        study = optuna.create_study(direction='maximize')

        study.optimize(
            self.objective,
            n_trials=n_trials,
            timeout=timeout_hours * 3600,
        )

        self.best_params = study.best_params
        self.best_value = study.best_value

        # Save results
        results = {
            'best_params': self.best_params,
            'best_value': self.best_value,
            'n_trials': len(study.trials),
        }

        with open(self.output_dir / 'best_params.json', 'w') as f:
            json.dump(results, f, indent=2)

        print(f"Best mAP@50: {self.best_value:.4f}")
        print(f"Best params: {self.best_params}")

        return results


if __name__ == "__main__":
    tuner = HyperparameterTuner('coral_dataset.yaml')
    tuner.tune(n_trials=20)
