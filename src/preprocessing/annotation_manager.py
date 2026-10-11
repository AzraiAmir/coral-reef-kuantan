"""
Annotation Manager
Handles annotation import, export, and quality control.
"""

import json
from pathlib import Path
import pandas as pd


class AnnotationManager:
    def __init__(self, dataset_root):
        self.dataset_root = Path(dataset_root)
        self.annotations_dir = self.dataset_root / "annotations"
        self.annotations_dir.mkdir(parents=True, exist_ok=True)

    def export_to_yolo_format(self, annotations_json, output_dir):
        """Convert COCO annotations to YOLO format."""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        with open(annotations_json, 'r') as f:
            data = json.load(f)

        all_classes = [
            'Live_Coral', 'Dead_Coral', 'Rubble', 'Sand', 'Rock',
            'Macroalgae', 'Turf_Algae', 'Coralline_Algae', 'Sponge',
            'Soft_Coral', 'Other',
            'Acropora', 'Montipora', 'Porites', 'Dipsastraea', 'Favites',
            'Platygyra', 'Goniastrea', 'Pocillopora', 'Stylophora',
            'Seriatopora', 'Fungia', 'Lobophyllia', 'Symphyllia',
            'Echinopora', 'Hydnophora', 'Merulina', 'Pectinia',
            'Turbinaria', 'Pavona', 'Leptoseris', 'Astreopora',
            'Cyphastrea', 'Leptastrea', 'Psammocora', 'Coeloseris',
            'Gardineroseris', 'Anacropora', 'Isopora', 'Acanthastrea',
            'Micromussa', 'Favia', 'Goniopora', 'Alveopora',
            'Uncertain_Genus',
            'Healthy', 'Partially_Bleached', 'Severely_Bleached',
            'Dead', 'Band_Disease', 'White_Disease', 'Tip_Necrosis',
            'Predation_Scars', 'Physical_Damage', 'Algal_Overgrowth',
            'Other_Condition'
        ]
        class_to_id = {cls: i for i, cls in enumerate(all_classes)}

        with open(output_dir / "classes.txt", 'w') as f:
            for cls in all_classes:
                f.write(f"{cls}\n")

        for image_info in data['images']:
            image_id = image_info['id']
            filename = image_info['file_name']
            width = image_info['width']
            height = image_info['height']

            image_annotations = [
                ann for ann in data['annotations']
                if ann['image_id'] == image_id
            ]

            lines = []
            for ann in image_annotations:
                category = ann['category_name']
                if category not in class_to_id:
                    continue

                class_id = class_to_id[category]
                bbox = ann['bbox']

                x_center = (bbox[0] + bbox[2] / 2) / width
                y_center = (bbox[1] + bbox[3] / 2) / height
                w = bbox[2] / width
                h = bbox[3] / height

                lines.append(f"{class_id} {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}")

            txt_filename = filename.replace('.jpg', '.txt').replace('.png', '.txt')
            with open(output_dir / txt_filename, 'w') as f:
                f.write('\n'.join(lines))

        print(f"YOLO format annotations saved to {output_dir}")

    def generate_statistics(self, annotations_json):
        """Generate annotation statistics."""
        with open(annotations_json, 'r') as f:
            data = json.load(f)

        class_counts = {}
        for ann in data['annotations']:
            cls = ann['category_name']
            class_counts[cls] = class_counts.get(cls, 0) + 1

        stats = {
            'total_images': len(data['images']),
            'total_annotations': len(data['annotations']),
            'class_distribution': class_counts,
        }

        return stats
