"""
Dataset Splitter
Splits annotated dataset into train/validation/test sets with stratification.
"""

import os
import json
import random
from pathlib import Path
from collections import defaultdict

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


class DatasetSplitter:
    def __init__(self, random_seed=42):
        self.random_seed = random_seed
        random.seed(random_seed)
        np.random.seed(random_seed)

    def split_dataset(self, annotation_file, output_dir,
                      train_ratio=0.7, val_ratio=0.15, test_ratio=0.15):
        """
        Split dataset into train, validation, and test sets.

        Args:
            annotation_file: Path to COCO JSON annotation file
            output_dir: Directory to save split files
            train_ratio: Proportion for training
            val_ratio: Proportion for validation
            test_ratio: Proportion for testing
        """
        assert abs(train_ratio + val_ratio + test_ratio - 1.0) < 1e-6, \
            "Ratios must sum to 1.0"

        with open(annotation_file, 'r') as f:
            data = json.load(f)

        # Group images by site (extracted from filename)
        images_by_site = defaultdict(list)
        for img in data['images']:
            filename = img['file_name']
            site = filename.split('_')[0] if '_' in filename else 'unknown'
            images_by_site[site].append(img)

        train_images = []
        val_images = []
        test_images = []

        for site, images in images_by_site.items():
            n = len(images)
            n_train = int(n * train_ratio)
            n_val = int(n * val_ratio)

            random.shuffle(images)

            train_images.extend(images[:n_train])
            val_images.extend(images[n_train:n_train + n_val])
            test_images.extend(images[n_train + n_val:])

        # Create split datasets
        splits = {
            'train': self._create_split(data, train_images),
            'val': self._create_split(data, val_images),
            'test': self._create_split(data, test_images)
        }

        # Save splits
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        for split_name, split_data in splits.items():
            output_file = output_dir / f"{split_name}.json"
            with open(output_file, 'w') as f:
                json.dump(split_data, f, indent=2)
            print(f"{split_name}: {len(split_data['images'])} images, "
                  f"{len(split_data['annotations'])} annotations")

        return splits

    def _create_split(self, full_data, images):
        """Create a split dataset containing only specified images."""
        image_ids = {img['id'] for img in images}

        split_data = {
            'images': images,
            'annotations': [
                ann for ann in full_data['annotations']
                if ann['image_id'] in image_ids
            ],
            'categories': full_data['categories'],
            'info': full_data.get('info', {}),
            'licenses': full_data.get('licenses', [])
        }

        return split_data

    def verify_split(self, splits):
        """Verify that splits are correct."""
        train_ids = {img['id'] for img in splits['train']['images']}
        val_ids = {img['id'] for img in splits['val']['images']}
        test_ids = {img['id'] for img in splits['test']['images']}

        assert len(train_ids & val_ids) == 0, "Train and val overlap"
        assert len(train_ids & test_ids) == 0, "Train and test overlap"
        assert len(val_ids & test_ids) == 0, "Val and test overlap"

        total = len(train_ids) + len(val_ids) + len(test_ids)
        print(f"Verification passed. Total images: {total}")
        print(f"  Train: {len(train_ids)} ({len(train_ids)/total*100:.1f}%)")
        print(f"  Val: {len(val_ids)} ({len(val_ids)/total*100:.1f}%)")
        print(f"  Test: {len(test_ids)} ({len(test_ids)/total*100:.1f}%)")

        return True


if __name__ == "__main__":
    splitter = DatasetSplitter(random_seed=42)

    splits = splitter.split_dataset(
        annotation_file="coral_dataset/annotations/full_dataset.json",
        output_dir="coral_dataset/splits",
        train_ratio=0.7,
        val_ratio=0.15,
        test_ratio=0.15
    )

    splitter.verify_split(splits)
