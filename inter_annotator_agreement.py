"""
Inter-Annotator Agreement
Calculates Cohen's Kappa and IoU for inter-annotator agreement.
"""

import numpy as np
from sklearn.metrics import cohen_kappa_score, confusion_matrix
from scipy.optimize import linear_sum_assignment


class InterAnnotatorAgreement:
    def __init__(self):
        self.results = {}

    def calculate_iou(self, box1, box2):
        """Calculate IoU between two bounding boxes [x, y, w, h]."""
        x1, y1, w1, h1 = box1
        x2, y2, w2, h2 = box2

        # Convert to [x1, y1, x2, y2]
        b1 = [x1, y1, x1 + w1, y1 + h1]
        b2 = [x2, y2, x2 + w2, y2 + h2]

        inter_x1 = max(b1[0], b2[0])
        inter_y1 = max(b1[1], b2[1])
        inter_x2 = min(b1[2], b2[2])
        inter_y2 = min(b1[3], b2[3])

        inter_area = max(0, inter_x2 - inter_x1) * max(0, inter_y2 - inter_y1)
        area1 = w1 * h1
        area2 = w2 * h2
        union_area = area1 + area2 - inter_area

        return inter_area / union_area if union_area > 0 else 0

    def calculate_agreement(self, annotations1, annotations2, iou_threshold=0.5):
        """Calculate agreement between two annotators."""
        matched_iou = []
        labels1 = []
        labels2 = []

        # Match annotations using Hungarian algorithm
        if len(annotations1) > 0 and len(annotations2) > 0:
            cost_matrix = np.zeros((len(annotations1), len(annotations2)))

            for i, a1 in enumerate(annotations1):
                for j, a2 in enumerate(annotations2):
                    cost_matrix[i, j] = -self.calculate_iou(a1['bbox'], a2['bbox'])

            row_ind, col_ind = linear_sum_assignment(cost_matrix)

            for i, j in zip(row_ind, col_ind):
                iou = -cost_matrix[i, j]
                if iou >= iou_threshold:
                    matched_iou.append(iou)
                    labels1.append(annotations1[i]['category'])
                    labels2.append(annotations2[j]['category'])

        kappa = cohen_kappa_score(labels1, labels2) if labels1 else 0

        self.results = {
            'mean_iou': np.mean(matched_iou) if matched_iou else 0,
            'std_iou': np.std(matched_iou) if matched_iou else 0,
            'cohens_kappa': kappa,
            'matched_annotations': len(matched_iou),
            'percentage_agreement': (
                sum(1 for a, b in zip(labels1, labels2) if a == b) / len(labels1) * 100
                if labels1 else 0
            ),
            'passed': kappa > 0.80 and np.mean(matched_iou) > 0.85 if matched_iou else False,
        }

        return self.results


if __name__ == "__main__":
    iaa = InterAnnotatorAgreement()

    ann1 = [
        {'bbox': [10, 20, 90, 100], 'category': 'Porites'},
        {'bbox': [150, 30, 100, 100], 'category': 'Acropora'},
    ]
    ann2 = [
        {'bbox': [12, 22, 92, 102], 'category': 'Porites'},
        {'bbox': [148, 28, 98, 98], 'category': 'Acropora'},
    ]

    results = iaa.calculate_agreement(ann1, ann2)
    print(f"Mean IoU: {results['mean_iou']:.4f}")
    print(f"Cohen's Kappa: {results['cohens_kappa']:.4f}")
    print(f"Passed: {results['passed']}")
