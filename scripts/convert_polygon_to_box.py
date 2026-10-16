"""
Converts Roboflow polygon labels to YOLO bounding box format.

Input format (polygon):
    class_id x1 y1 x2 y2 x3 y3 ...

Output format (box):
    class_id x_center y_center width height
"""

from pathlib import Path
import shutil


def convert_polygon_file(input_path, output_path):
    """Convert a single polygon file to YOLO box format."""
    with open(input_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    box_lines = []
    for line in lines:
        parts = line.split()
        if len(parts) < 5:
            continue

        class_id = parts[0]
        coords = [float(x) for x in parts[1:]]

        xs = coords[0::2]
        ys = coords[1::2]

        if len(xs) < 2 or len(ys) < 2:
            continue

        x_min = min(xs)
        x_max = max(xs)
        y_min = min(ys)
        y_max = max(ys)

        x_center = (x_min + x_max) / 2
        y_center = (y_min + y_max) / 2
        width = x_max - x_min
        height = y_max - y_min

        x_center = max(0.0, min(1.0, x_center))
        y_center = max(0.0, min(1.0, y_center))
        width = max(0.0, min(1.0, width))
        height = max(0.0, min(1.0, height))

        box_lines.append(
            f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}"
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        f.write("\n".join(box_lines))


def main():
    base_dirs = [
        Path("data/annotations/train/labels"),
        Path("data/annotations/valid/labels"),
        Path("data/annotations/test/labels"),
    ]

    total_converted = 0

    for labels_dir in base_dirs:
        if not labels_dir.exists():
            print(f"Skip (not found): {labels_dir}")
            continue

        backup_dir = labels_dir.parent / f"{labels_dir.name}_polygon_backup"
        if not backup_dir.exists():
            shutil.copytree(labels_dir, backup_dir)
            print(f"Backed up to: {backup_dir}")

        files = list(labels_dir.glob("*.txt"))
        print(f"Processing {len(files)} files in {labels_dir}...")

        for txt_path in files:
            convert_polygon_file(txt_path, txt_path)
            total_converted += 1

        print(f"  Converted {len(files)} files")

    print(f"\nDone. Total converted: {total_converted}")


if __name__ == "__main__":
    main()