"""
Phase A Runner — Log all coral images via Image Video Logger (F.1)
"""

from pathlib import Path
from src.data_acquisition.image_video_logger import ImageVideoAcquisitionLogger


def main():
    # Configuration
    image_dir = Path("data/raw/test_images")
    site_id = "KTN-01"
    campaign = 1
    output_dir = "acquisition_logs"

    # Verify images exist
    image_files = sorted(image_dir.glob("*.jpg"))
    print(f"Found {len(image_files)} images in {image_dir}")

    if not image_files:
        print("No images found. Exiting.")
        return

    # Initialize logger
    logger = ImageVideoAcquisitionLogger(output_dir=output_dir)

    # Log each image
    for i, image_path in enumerate(image_files, 1):
        fname = image_path.stem  # e.g. SAMPLE_C1_POR_0001
        parts = fname.split("_")
        species = parts[2] if len(parts) > 2 else "UNK"
        number = parts[3] if len(parts) > 3 else "0000"

        logger.log_image(
            image_path=str(image_path),
            site_id=site_id,
            quadrat_id=f"C{campaign}_{species}",
            depth=0.0,
            temperature=0.0,
            salinity=0.0,
            pH=0.0,
            turbidity=0.0,
            gps_coords=(0.0, 0.0),
            input_type="image",
        )

        if i % 20 == 0:
            print(f"  Logged {i}/{len(image_files)}")

    # Save
    logger.save_log()

    # Summary
    summary = logger.generate_summary()
    print("\n=== Summary ===")
    for key, value in summary.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()