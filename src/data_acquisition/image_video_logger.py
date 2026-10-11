"""
Image and Video Acquisition Logger

Records metadata for each captured image and video during
50 m² quadrat-based coral photo transect (CPT) surveys.
"""

import os
import csv
import json
from datetime import datetime
from PIL import Image
import exifread


class ImageVideoAcquisitionLogger:
    """Logs image and video metadata during field surveys."""

    def __init__(self, output_dir="acquisition_logs"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.log_file = os.path.join(
            output_dir,
            f"acquisition_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        )
        self.metadata = []

    def log_image(self, image_path, site_id, quadrat_id, depth,
                  temperature, salinity, pH, turbidity, gps_coords,
                  input_type="image"):
        """Log metadata for a single image."""
        try:
            with open(image_path, "rb") as f:
                tags = exifread.process_file(f)
            img = Image.open(image_path)
            width, height = img.size
        except Exception:
            tags = {}
            width, height = (0, 0)

        record = {
            "timestamp": datetime.now().isoformat(),
            "input_type": input_type,
            "filename": os.path.basename(image_path),
            "path": image_path,
            "site_id": site_id,
            "quadrat_id": quadrat_id,
            "depth_m": depth,
            "temperature_c": temperature,
            "salinity_psu": salinity,
            "ph": pH,
            "turbidity_ntu": turbidity,
            "gps_latitude": gps_coords[0],
            "gps_longitude": gps_coords[1],
            "image_width_px": width,
            "image_height_px": height,
            "camera_model": str(tags.get("Image Model", "Unknown")),
            "exposure_time": str(tags.get("EXIF ExposureTime", "Unknown")),
            "f_number": str(tags.get("EXIF FNumber", "Unknown")),
            "iso": str(tags.get("EXIF ISOSpeedRatings", "Unknown")),
        }
        self.metadata.append(record)
        return record

    def log_video(self, video_path, site_id, quadrat_id, depth,
                  temperature, salinity, pH, turbidity, gps_coords,
                  fps=30, duration_seconds=None):
        """Log metadata for a single video."""
        record = {
            "timestamp": datetime.now().isoformat(),
            "input_type": "video",
            "filename": os.path.basename(video_path),
            "path": video_path,
            "site_id": site_id,
            "quadrat_id": quadrat_id,
            "depth_m": depth,
            "temperature_c": temperature,
            "salinity_psu": salinity,
            "ph": pH,
            "turbidity_ntu": turbidity,
            "gps_latitude": gps_coords[0],
            "gps_longitude": gps_coords[1],
            "fps": fps,
            "duration_seconds": duration_seconds,
        }
        self.metadata.append(record)
        return record

    def save_log(self):
        """Save all logged metadata to CSV."""
        if not self.metadata:
            print("No metadata to save.")
            return
        fieldnames = self.metadata[0].keys()
        with open(self.log_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.metadata)
        print(f"Acquisition log saved to {self.log_file}")
        print(f"Total records logged: {len(self.metadata)}")

    def generate_summary(self):
        """Generate a summary of the acquisition session."""
        if not self.metadata:
            return "No data available."
        return {
            "total_records": len(self.metadata),
            "images": sum(1 for r in self.metadata if r["input_type"] == "image"),
            "videos": sum(1 for r in self.metadata if r["input_type"] == "video"),
            "sites_covered": list({r["site_id"] for r in self.metadata}),
            "quadrats_covered": list({r["quadrat_id"] for r in self.metadata}),
        }


if __name__ == "__main__":
    logger = ImageVideoAcquisitionLogger()
    logger.log_image(
        image_path="data/raw/test_images/coral_1.jpg",
        site_id="KTN-01",
        quadrat_id="Q01",
        depth=15.5,
        temperature=29.2,
        salinity=33.1,
        pH=8.05,
        turbidity=4.5,
        gps_coords=(3.9367, 103.3967),
        input_type="image",
    )
    logger.save_log()
    print(json.dumps(logger.generate_summary(), indent=2))