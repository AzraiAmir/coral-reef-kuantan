"""
Image vs Video Detection Comparison

Compares YOLOv8 detection performance between image and video frame inputs
for coral detection (proof-of-concept analysis).
"""

from pathlib import Path
import cv2
import pandas as pd
from ultralytics import YOLO


class ImageVideoDetectionComparison:
    """Compares detection between image and video frame inputs."""

    def __init__(self, model_path, output_dir="image_video_detection"):
        self.model = YOLO(model_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def compare_detection(self, image_path, video_path, frame_index=0, conf=0.5):
        """Compare detection between image and matching video frame."""
        image = cv2.imread(str(image_path))
        if image is None:
            raise ValueError(f"Cannot read image: {image_path}")

        cap = cv2.VideoCapture(str(video_path))
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        ret, frame = cap.read()
        cap.release()
        if not ret:
            raise ValueError(f"Cannot read frame {frame_index}")

        image_result = self.model.predict(str(image_path), conf=conf, verbose=False)
        frame_result = self.model.predict(frame, conf=conf, verbose=False)

        def count_detections(results):
            total = 0
            confs = []
            for r in results:
                if r.boxes is not None:
                    total += len(r.boxes)
                    confs.extend([float(b.conf[0]) for b in r.boxes])
            return total, (sum(confs) / len(confs) if confs else 0.0)

        img_count, img_conf = count_detections(image_result)
        vid_count, vid_conf = count_detections(frame_result)

        return {
            "image": {
                "path": str(image_path),
                "resolution": f"{image.shape[1]}x{image.shape[0]}",
                "detections": img_count,
                "mean_confidence": round(img_conf, 3),
            },
            "video_frame": {
                "path": str(video_path),
                "frame_index": frame_index,
                "resolution": f"{frame.shape[1]}x{frame.shape[0]}",
                "detections": vid_count,
                "mean_confidence": round(vid_conf, 3),
            },
            "difference": {
                "detections": img_count - vid_count,
                "confidence": round(img_conf - vid_conf, 3),
            },
        }

    def generate_report(self, image_paths, video_paths, output_csv):
        """Generate comparison report for multiple image-video pairs."""
        rows = []
        for img, vid in zip(image_paths, video_paths):
            try:
                r = self.compare_detection(img, vid)
                rows.append({
                    "image_path": img,
                    "video_path": vid,
                    "image_detections": r["image"]["detections"],
                    "video_detections": r["video_frame"]["detections"],
                    "image_confidence": r["image"]["mean_confidence"],
                    "video_confidence": r["video_frame"]["mean_confidence"],
                    "detection_diff": r["difference"]["detections"],
                })
            except Exception as e:
                print(f"Skip {img}: {e}")

        df = pd.DataFrame(rows)
        df.to_csv(output_csv, index=False)
        print(f"Report saved to {output_csv}")
        return df


if __name__ == "__main__":
    print("Image vs Video Detection Comparison ready.")