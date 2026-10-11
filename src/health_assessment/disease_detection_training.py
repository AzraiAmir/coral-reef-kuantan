"""
Disease Detection Training
Train disease detection model using YOLOv8.
"""

from ultralytics import YOLO
from pathlib import Path


class DiseaseDetectionTrainer:
    def __init__(self, data_yaml, output_dir='disease_detection'):
        self.data_yaml = data_yaml
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def train(self, epochs=200, imgsz=640, batch=16):
        """Train disease detection model."""
        model = YOLO('yolov8m.pt')

        results = model.train(
            data=self.data_yaml,
            epochs=epochs,
            imgsz=imgsz,
            batch=batch,
            project=str(self.output_dir),
            name='train',
            optimizer='Adam',
            lr0=0.001,
            patience=50,
            save=True,
            plots=True,
        )

        return results

    def validate(self, model_path, data_yaml):
        """Validate disease detection model."""
        model = YOLO(model_path)
        metrics = model.val(data=data_yaml)

        print(f"mAP@50: {metrics.box.map50:.4f}")
        print(f"mAP@50-95: {metrics.box.map:.4f}")
        print(f"Precision: {metrics.box.mp:.4f}")
        print(f"Recall: {metrics.box.mr:.4f}")

        return metrics


if __name__ == "__main__":
    trainer = DiseaseDetectionTrainer('disease_dataset.yaml')
    trainer.train(epochs=200)
