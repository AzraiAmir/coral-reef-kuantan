"""
Annotation Conversion
Convert between annotation formats (COCO, YOLO, Pascal VOC).
"""

import json
import xml.etree.ElementTree as ET
from pathlib import Path
import pandas as pd


class AnnotationConverter:
    def __init__(self):
        pass

    def coco_to_yolo(self, coco_json, output_dir):
        """Convert COCO JSON to YOLO format."""
        with open(coco_json, 'r') as f:
            data = json.load(f)

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Category mapping
        category_map = {cat['id']: i for i, cat in enumerate(data['categories'])}

        # Image mapping
        image_map = {img['id']: img for img in data['images']}

        # Group annotations by image
        anns_by_image = {}
        for ann in data['annotations']:
            img_id = ann['image_id']
            if img_id not in anns_by_image:
                anns_by_image[img_id] = []
            anns_by_image[img_id].append(ann)

        for img_id, anns in anns_by_image.items():
            img_info = image_map[img_id]
            width = img_info['width']
            height = img_info['height']
            filename = img_info['file_name'].replace('.jpg', '.txt').replace('.png', '.txt')

            lines = []
            for ann in anns:
                cat_id = category_map[ann['category_id']]
                bbox = ann['bbox']

                x_center = (bbox[0] + bbox[2] / 2) / width
                y_center = (bbox[1] + bbox[3] / 2) / height
                w = bbox[2] / width
                h = bbox[3] / height

                lines.append(f"{cat_id} {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}")

            with open(output_dir / filename, 'w') as f:
                f.write('\n'.join(lines))

        # Write classes.txt
        with open(output_dir / "classes.txt", 'w') as f:
            for cat in data['categories']:
                f.write(f"{cat['name']}\n")

        print(f"Converted {len(data['annotations'])} annotations to YOLO format.")

    def coco_to_voc(self, coco_json, output_dir):
        """Convert COCO JSON to Pascal VOC XML format."""
        with open(coco_json, 'r') as f:
            data = json.load(f)

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        category_map = {cat['id']: cat['name'] for cat in data['categories']}
        image_map = {img['id']: img for img in data['images']}

        anns_by_image = {}
        for ann in data['annotations']:
            img_id = ann['image_id']
            if img_id not in anns_by_image:
                anns_by_image[img_id] = []
            anns_by_image[img_id].append(ann)

        for img_id, anns in anns_by_image.items():
            img_info = image_map[img_id]

            root = ET.Element("annotation")
            ET.SubElement(root, "folder").text = "images"
            ET.SubElement(root, "filename").text = img_info['file_name']

            size = ET.SubElement(root, "size")
            ET.SubElement(size, "width").text = str(img_info['width'])
            ET.SubElement(size, "height").text = str(img_info['height'])
            ET.SubElement(size, "depth").text = "3"

            for ann in anns:
                obj = ET.SubElement(root, "object")
                ET.SubElement(obj, "name").text = category_map[ann['category_id']]
                ET.SubElement(obj, "difficult").text = "0"

                bbox = ann['bbox']
                bndbox = ET.SubElement(obj, "bndbox")
                ET.SubElement(bndbox, "xmin").text = str(int(bbox[0]))
                ET.SubElement(bndbox, "ymin").text = str(int(bbox[1]))
                ET.SubElement(bndbox, "xmax").text = str(int(bbox[0] + bbox[2]))
                ET.SubElement(bndbox, "ymax").text = str(int(bbox[1] + bbox[3]))

            tree = ET.ElementTree(root)
            output_path = output_dir / img_info['file_name'].replace('.jpg', '.xml')
            tree.write(output_path)

        print(f"Converted annotations to Pascal VOC format.")

    def yolo_to_coco(self, yolo_dir, classes_file, output_json):
        """Convert YOLO format to COCO JSON."""
        yolo_dir = Path(yolo_dir)

        with open(classes_file, 'r') as f:
            classes = [line.strip() for line in f.readlines()]

        categories = [{'id': i, 'name': name} for i, name in enumerate(classes)]

        images = []
        annotations = []
        ann_id = 1

        txt_files = list(yolo_dir.glob("*.txt"))
        txt_files = [f for f in txt_files if f.name != "classes.txt"]

        for img_id, txt_file in enumerate(txt_files, 1):
            img_name = txt_file.stem + ".jpg"

            # Get image dimensions
            import cv2
            img_path = yolo_dir / img_name
            if img_path.exists():
                img = cv2.imread(str(img_path))
                height, width = img.shape[:2]
            else:
                width, height = 1920, 1080

            images.append({
                'id': img_id,
                'file_name': img_name,
                'width': width,
                'height': height,
            })

            with open(txt_file, 'r') as f:
                for line in f.readlines():
                    parts = line.strip().split()
                    if len(parts) == 5:
                        cat_id = int(parts[0])
                        x_center = float(parts[1]) * width
                        y_center = float(parts[2]) * height
                        w = float(parts[3]) * width
                        h = float(parts[4]) * height

                        x = x_center - w / 2
                        y = y_center - h / 2

                        annotations.append({
                            'id': ann_id,
                            'image_id': img_id,
                            'category_id': cat_id,
                            'bbox': [x, y, w, h],
                            'area': w * h,
                            'iscrowd': 0,
                        })
                        ann_id += 1

        coco_data = {
            'images': images,
            'annotations': annotations,
            'categories': categories,
        }

        with open(output_json, 'w') as f:
            json.dump(coco_data, f, indent=2)

        print(f"Converted {len(annotations)} annotations to COCO format.")


if __name__ == "__main__":
    converter = AnnotationConverter()

    converter.coco_to_yolo(
        coco_json="coral_dataset/annotations/train.json",
        output_dir="coral_dataset/yolo_labels/train"
    )
