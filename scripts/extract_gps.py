import os
import csv
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from pathlib import Path

# --- PATH TO YOUR RAW IMAGES ---
RAW_DIR = Path(r"C:\Users\mazra\Downloads\coral-reef-kuantan\data\raw")
OUTPUT_CSV = Path(r"C:\Users\mazra\Downloads\coral-reef-kuantan\results\phase_d\gps_coordinates.csv")

def get_decimal_coordinates(info):
    """Converts EXIF GPS tags to decimal degrees."""
    def to_decimal(values):
        d, m, s = values
        return float(d) + (float(m) / 60.0) + (float(s) / 3600.0)

    lat_info = info.get('GPSLatitude')
    lat_ref = info.get('GPSLatitudeRef')
    lon_info = info.get('GPSLongitude')
    lon_ref = info.get('GPSLongitudeRef')

    if lat_info and lat_ref and lon_info and lon_ref:
        lat = to_decimal(lat_info)
        lon = to_decimal(lon_info)
        
        # South and West are negative
        if lat_ref != 'N': lat = -lat
        if lon_ref != 'E': lon = -lon
        
        return lat, lon
    return None, None

def main():
    print(f"Scanning folder: {RAW_DIR}")
    
    # Find all images recursively
    image_extensions = ('.jpg', '.jpeg', '.png')
    images = [p for p in RAW_DIR.rglob('*') if p.suffix.lower() in image_extensions]
    
    print(f"Found {len(images)} images. Extracting GPS data...")
    
    results = []
    
    for img_path in images:
        try:
            with Image.open(img_path) as img:
                exif_data = img._getexif()
                if exif_data:
                    gps_info = {}
                    for tag, value in exif_data.items():
                        tag_name = TAGS.get(tag, tag)
                        if tag_name == 'GPSInfo':
                            for gps_tag, gps_val in value.items():
                                gps_tag_name = GPSTAGS.get(gps_tag, gps_tag)
                                gps_info[gps_tag_name] = gps_val
                    
                    lat, lon = get_decimal_coordinates(gps_info)
                    
                    if lat is not None and lon is not None:
                        results.append({
                            "image_name": img_path.name,
                            "file_path": str(img_path),
                            "latitude": lat,
                            "longitude": lon
                        })
        except Exception as e:
            # Silently skip images that are corrupted or don't have EXIF
            pass

    # Save to CSV
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    
    if results:
        with open(OUTPUT_CSV, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["image_name", "file_path", "latitude", "longitude"])
            writer.writeheader()
            writer.writerows(results)
        print(f"✅ Success! Extracted GPS for {len(results)} images.")
        print(f"Saved to: {OUTPUT_CSV}")
    else:
        print("⚠️ No images with GPS EXIF data found.")

if __name__ == "__main__":
    main()