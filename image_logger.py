"""
Image Acquisition Logger
Records metadata for each captured image during CVT surveys.
"""

import os
import csv
import json
from datetime import datetime
from PIL import Image
import exifread


class ImageAcquisitionLogger:
    def __init__(self, output_dir="acquisition_logs"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.log_file = os.path.join(
            output_dir,
            f"acquisition_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )
        self.metadata = []

    def log_image(self, image_path, site_id, transect_id, depth,
                  temperature, salinity, pH, gps_coords):
        """Log metadata for a single image."""
        with open(image_path, 'rb') as f:
            tags = exifread.process_file(f)

        img = Image.open(image_path)
        width, height = img.size

        record = {
            'timestamp': datetime.now().isoformat(),
            'image_filename': os.path.basename(image_path),
            'image_path': image_path,
            'site_id': site_id,
            'transect_id': transect_id,
            'depth_m': depth,
            'temperature_c': temperature,
            'salinity_psu': salinity,
            'ph': pH,
            'gps_latitude': gps_coords[0],
            'gps_longitude': gps_coords[1],
            'image_width_px': width,
            'image_height_px': height,
            'camera_model': str(tags.get('Image Model', 'Unknown')),
            'exposure_time': str(tags.get('EXIF ExposureTime', 'Unknown')),
            'f_number': str(tags.get('EXIF FNumber', 'Unknown')),
            'iso': str(tags.get('EXIF ISOSpeedRatings', 'Unknown')),
        }

        self.metadata.append(record)
        return record

    def save_log(self):
        """Save all logged metadata to CSV."""
        if not self.metadata:
            print("No metadata to save.")
            return

        fieldnames = self.metadata[0].keys()
        with open(self.log_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.metadata)

        print(f"Acquisition log saved to {self.log_file}")
        print(f"Total images logged: {len(self.metadata)}")

    def generate_summary(self):
        """Generate a summary of the acquisition session."""
        if not self.metadata:
            return "No data available."

        summary = {
            'total_images': len(self.metadata),
            'sites_covered': list(set(r['site_id'] for r in self.metadata)),
            'depth_range': (
                min(r['depth_m'] for r in self.metadata),
                max(r['depth_m'] for r in self.metadata)
            ),
            'temperature_range': (
                min(r['temperature_c'] for r in self.metadata),
                max(r['temperature_c'] for r in self.metadata)
            ),
            'salinity_range': (
                min(r['salinity_psu'] for r in self.metadata),
                max(r['salinity_psu'] for r in self.metadata)
            ),
            'ph_range': (
                min(r['ph'] for r in self.metadata),
                max(r['ph'] for r in self.metadata)
            ),
        }
        return summary


if __name__ == "__main__":
    logger = ImageAcquisitionLogger()

    for i in range(10):
        logger.log_image(
            image_path=f"survey_images/site01_transect01_{i:04d}.jpg",
            site_id="KTN-01",
            transect_id="T01",
            depth=15.5 + i * 0.1,
            temperature=29.2 + i * 0.05,
            salinity=33.1 + i * 0.02,
            pH=8.05 + i * 0.01,
            gps_coords=(3.9367 + i * 0.0001, 103.3967 + i * 0.0001)
        )

    logger.save_log()
    summary = logger.generate_summary()
    print(json.dumps(summary, indent=2))
