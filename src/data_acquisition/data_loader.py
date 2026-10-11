"""
Data Loader
Loads and preprocesses data for training and analysis.
"""

import pandas as pd
import numpy as np
import cv2
from pathlib import Path
from torch.utils.data import Dataset, DataLoader
import torch


class CoralDataset(Dataset):
    """PyTorch Dataset for coral images and annotations."""

    def __init__(self, image_dir, annotation_file, transform=None):
        self.image_dir = Path(image_dir)
        self.annotations = pd.read_csv(annotation_file)
        self.transform = transform

    def __len__(self):
        return len(self.annotations)

    def __getitem__(self, idx):
        row = self.annotations.iloc[idx]
        image_path = self.image_dir / row['filename']
        image = cv2.imread(str(image_path))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        if self.transform:
            image = self.transform(image)

        label = row['label']
        return image, label


class CoralDataLoader:
    def __init__(self, data_dir):
        self.data_dir = Path(data_dir)

    def load_annotations(self, annotation_file):
        """Load annotations from CSV."""
        return pd.read_csv(annotation_file)

    def load_images(self, image_dir):
        """Load all images from directory."""
        images = []
        image_paths = []

        for img_path in Path(image_dir).glob("*.jpg"):
            img = cv2.imread(str(img_path))
            if img is not None:
                images.append(img)
                image_paths.append(str(img_path))

        return images, image_paths

    def create_dataloader(self, image_dir, annotation_file,
                          batch_size=16, shuffle=True, num_workers=4):
        """Create PyTorch DataLoader."""
        dataset = CoralDataset(image_dir, annotation_file)
        return DataLoader(
            dataset,
            batch_size=batch_size,
            shuffle=shuffle,
            num_workers=num_workers
        )
