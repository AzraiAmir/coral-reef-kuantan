"""
Class Distribution Calculator
Calculates the distribution of coral genera in the annotated dataset.
"""

import json
import pandas as pd
from collections import Counter


class ClassDistributionCalculator:
    def __init__(self, annotations_json):
        self.annotations_json = annotations_json
        self.data = None

    def load_annotations(self):
        """Load annotations from COCO JSON file."""
        with open(self.annotations_json, 'r') as f:
            self.data = json.load(f)
        return self.data

    def calculate_distribution(self):
        """Calculate class distribution."""
        category_map = {cat['id']: cat['name'] for cat in self.data['categories']}
        counts = Counter()

        for ann in self.data['annotations']:
            cat_name = category_map.get(ann['category_id'], 'Unknown')
            counts[cat_name] += 1

        total = sum(counts.values())
        distribution = []
        for genus, count in counts.most_common():
            distribution.append({
                'Genus': genus,
                'Count': count,
                'Percentage': f"{(count / total * 100):.1f}%"
            })

        df = pd.DataFrame(distribution)
        return df


if __name__ == "__main__":
    calculator = ClassDistributionCalculator(
        "coral_dataset/annotations/train.json"
    )
    calculator.load_annotations()
    df = calculator.calculate_distribution()
    print(df.to_string(index=False))
