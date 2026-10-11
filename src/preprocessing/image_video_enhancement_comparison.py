"""
Image vs Video Enhancement Comparison

Compares enhancement results between image and video frame inputs
to assess input-modality trade-offs (resolution, temporal context).
"""

import os
from pathlib import Path
import cv2
import numpy as np
import pandas as pd

from src.preprocessing.traditional_enhancement import TraditionalEnhancer
from src.preprocessing.enhancement_metrics import EnhancementMetrics


class ImageVideoEnhancementComparison:
    """Compares enhancement quality between image and video frames."""

    def __init__(self, output_dir="image_video_comparison"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.enhancer = TraditionalEnhancer()
        self.metrics = EnhancementMetrics()

    def compare_image_video(self, image_path, video_path, frame_index=0):
        """Compare enhancement on a single image vs a video frame."""
        image = cv2.imread(str(image_path))
        if image is None:
            raise ValueError(f"Cannot read image: {image_path}")

        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            raise ValueError(f"Cannot open video: {video_path}")
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        ret, video_frame = cap.read()
        cap.release()
        if not ret:
            raise ValueError(f"Cannot read frame {frame_index}")

        # Enhance both
        image_enhanced = self.enhancer.enhance(image)
        video_enhanced = self.enhancer.enhance(video_frame)

        # Compute metrics
        result = {
            "image": {
                "resolution": f"{image.shape[1]}x{image.shape[0]}",
                "megapixels": round(image.shape[0] * image.shape[1] / 1e6, 2),
                "uciqe_original": self.metrics.calculate_uciqe(image),
                "uciqe_enhanced": self.metrics.calculate_uciqe(image_enhanced),
                "uiqm_original": self.metrics.calculate_uiqm(image),
                "uiqm_enhanced": self.metrics.calculate_uiqm(image_enhanced),
            },
            "video_frame": {
                "resolution": f"{video_frame.shape[1]}x{video_frame.shape[0]}",
                "megapixels": round(video_frame.shape[0] * video_frame.shape[1] / 1e6, 2),
                "uciqe_original": self.metrics.calculate_uciqe(video_frame),
                "uciqe_enhanced": self.metrics.calculate_uciqe(video_enhanced),
                "uiqm_original": self.metrics.calculate_uiqm(video_frame),
                "uiqm_enhanced": self.metrics.calculate_uiqm(video_enhanced),
            },
        }
        return result

    def generate_comparison_report(self, image_paths, video_paths, output_csv):
        """Generate comparison report for multiple image-video pairs."""
        rows = []
        for img, vid in zip(image_paths, video_paths):
            try:
                r = self.compare_image_video(img, vid)
                rows.append({
                    "image_path": img,
                    "video_path": vid,
                    "image_mp": r["image"]["megapixels"],
                    "video_mp": r["video_frame"]["megapixels"],
                    "image_uciqe": r["image"]["uciqe_enhanced"],
                    "video_uciqe": r["video_frame"]["uciqe_enhanced"],
                    "image_uiqm": r["image"]["uiqm_enhanced"],
                    "video_uiqm": r["video_frame"]["uiqm_enhanced"],
                })
            except Exception as e:
                print(f"Skip {img}: {e}")

        df = pd.DataFrame(rows)
        df.to_csv(output_csv, index=False)
        print(f"Comparison report saved to {output_csv}")
        return df


if __name__ == "__main__":
    comparison = ImageVideoEnhancementComparison()
    # result = comparison.compare_image_video(
    #     "data/raw/test_images/coral_1.jpg",
    #     "data/raw/test_videos/coral_1.mp4",
    # )
    print("Image vs Video Enhancement Comparison ready.")