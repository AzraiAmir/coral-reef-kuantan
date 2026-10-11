"""
Video Frame Extractor

Extracts frames from underwater video for image-based detection
and image-vs-video comparison analysis.
"""

import os
import csv
from pathlib import Path
import cv2


class VideoFrameExtractor:
    """Extracts frames from video files at regular intervals."""

    def __init__(self, output_dir="extracted_frames"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.metadata = []

    def extract_frames(self, video_path, site_id, quadrat_id,
                       interval_seconds=1.0, output_format="jpg", quality=95):
        """Extract frames at regular intervals."""
        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            raise ValueError(f"Could not open video: {video_path}")

        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps if fps > 0 else 0

        frame_interval = int(fps * interval_seconds)
        frame_dir = self.output_dir / f"{site_id}_{quadrat_id}"
        frame_dir.mkdir(parents=True, exist_ok=True)

        frames_saved = []
        frame_idx = 0
        saved_idx = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if frame_idx % frame_interval == 0:
                filename = f"{site_id}_{quadrat_id}_{saved_idx:04d}.{output_format}"
                filepath = frame_dir / filename
                params = [cv2.IMWRITE_JPEG_QUALITY, quality] if output_format == "jpg" else []
                cv2.imwrite(str(filepath), frame, params)
                frames_saved.append(str(filepath))
                self.metadata.append({
                    "video_path": str(video_path),
                    "frame_path": str(filepath),
                    "site_id": site_id,
                    "quadrat_id": quadrat_id,
                    "frame_index": frame_idx,
                    "timestamp_sec": frame_idx / fps if fps > 0 else 0,
                    "resolution": f"{frame.shape[1]}x{frame.shape[0]}",
                })
                saved_idx += 1
            frame_idx += 1

        cap.release()
        print(f"Extracted {len(frames_saved)} frames from {video_path}")
        print(f"Video FPS: {fps}, Duration: {duration:.1f}s, Resolution: {frames_saved and 'saved'}")
        return frames_saved

    def extract_frames_for_comparison(self, video_path, site_id,
                                       quadrat_id, n_frames=50):
        """Extract fixed number of frames for image-vs-video comparison."""
        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            raise ValueError(f"Could not open video: {video_path}")

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        step = max(1, total_frames // n_frames)

        frame_dir = self.output_dir / f"{site_id}_{quadrat_id}_compare"
        frame_dir.mkdir(parents=True, exist_ok=True)

        saved = []
        for i in range(n_frames):
            cap.set(cv2.CAP_PROP_POS_FRAMES, i * step)
            ret, frame = cap.read()
            if not ret:
                break
            filepath = frame_dir / f"frame_{i:04d}.jpg"
            cv2.imwrite(str(filepath), frame)
            saved.append(str(filepath))

        cap.release()
        print(f"Extracted {len(saved)} comparison frames")
        return saved

    def save_metadata(self, output_csv="frame_metadata.csv"):
        """Save frame metadata to CSV."""
        if not self.metadata:
            print("No metadata to save.")
            return
        with open(output_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.metadata[0].keys())
            writer.writeheader()
            writer.writerows(self.metadata)
        print(f"Metadata saved to {output_csv}")


if __name__ == "__main__":
    extractor = VideoFrameExtractor(output_dir="data/processed/frames")
    # extractor.extract_frames("data/raw/test_videos/coral_1.mp4", "KTN-01", "Q01")
    # extractor.save_metadata("frame_metadata.csv")