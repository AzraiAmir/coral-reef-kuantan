"""
CoralSCOP Segmentation
CoralSCOP segmentation pipeline for coral tissue segmentation.
"""

import torch
import numpy as np
import cv2
from segment_anything import sam_model_registry, SamPredictor


class CoralSCOPSegmentation:
    def __init__(self, model_type='vit_h', checkpoint_path='coralscop.pth',
                 device='cuda' if torch.cuda.is_available() else 'cpu'):
        self.device = device
        self.model = sam_model_registry[model_type](checkpoint=checkpoint_path)
        self.model.to(device)
        self.predictor = SamPredictor(self.model)

    def segment(self, image, bbox):
        """Segment coral colony within bounding box."""
        self.predictor.set_image(image)

        input_box = np.array(bbox)
        masks, scores, logits = self.predictor.predict(
            point_coords=None,
            point_labels=None,
            box=input_box[None, :],
            multimask_output=True,
        )

        # Select best mask based on score
        best_idx = np.argmax(scores)
        best_mask = masks[best_idx]

        return best_mask, scores[best_idx]

    def segment_batch(self, image, bboxes):
        """Segment multiple coral colonies."""
        self.predictor.set_image(image)
        results = []

        for bbox in bboxes:
            input_box = np.array(bbox)
            masks, scores, logits = self.predictor.predict(
                point_coords=None,
                point_labels=None,
                box=input_box[None, :],
                multimask_output=True,
            )

            best_idx = np.argmax(scores)
            results.append({
                'bbox': bbox,
                'mask': masks[best_idx],
                'score': scores[best_idx]
            })

        return results

    def filter_masks(self, masks, iou_threshold=0.8, stability_threshold=0.8):
        """Filter masks based on IoU and stability scores."""
        filtered = []
        for mask in masks:
            if mask['iou'] >= iou_threshold and mask['stability'] >= stability_threshold:
                filtered.append(mask)
        return filtered
