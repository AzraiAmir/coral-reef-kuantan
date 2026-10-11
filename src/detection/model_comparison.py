"""
YOLO Model Comparison Framework
Compare YOLOv8, v9, v10, v11, v12 for coral detection.
"""

import torch
from ultralytics import YOLO
import pandas as pd
import time
import os
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np


class YOLOModelComparison:
    def __init__(self, data_yaml, device='cuda'):
        self.data_yaml = data_yaml
        self.device = device
        self.results = {}

    def evaluate_model(self, model_name, epochs=100):
        """Evaluate a single YOLO model."""
        print(f"\n{'='*60}")
        print(f"Evaluating {model_name}")
        print(f"{'='*60}")

        model = YOLO(f'{model_name}.pt')

        start_time = time.time()
        model.train(
            data=self.data_yaml,
            epochs=epochs,
            imgsz=640,
            batch=16,
            device=self.device,
            project='model_comparison',
            name=model_name,
            verbose=False
        )
        training_time = time.time() - start_time

        val_results = model.val(data=self.data_yaml)

        inference_times = []
        for _ in range(10):
            start = time.time()
            model.predict('test_images/sample.jpg', verbose=False)
            inference_times.append(time.time() - start)

        self.results[model_name] = {
            'mAP50': val_results.box.map50,
            'mAP50-95': val_results.box.map,
            'precision': val_results.box.mp,
            'recall': val_results.box.mr,
            'training_time_s': training_time,
            'inference_time_ms': np.mean(inference_times) * 1000,
        }

        return self.results[model_name]

    def compare_all(self, model_versions=None, epochs=100):
        """Compare all YOLO versions."""
        if model_versions is None:
            model_versions = ['yolov8m', 'yolov9m', 'yolov10m', 'yolov11m', 'yolov12m']

        for version in model_versions:
            try:
                self.evaluate_model(version, epochs=epochs)
            except Exception as e:
                print(f"Error evaluating {version}: {e}")

        return pd.DataFrame(self.results).T
