"""
XAI Interpretability
Implements Grad-CAM and LIME for model interpretability.
"""

import torch
import numpy as np
import cv2
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.image import show_cam_on_image


class XAIInterpreter:
    def __init__(self, model, target_layers):
        self.model = model
        self.target_layers = target_layers
        self.grad_cam = GradCAM(model=model, target_layers=target_layers)

    def generate_grad_cam(self, input_tensor, target_category=None):
        """Generate Grad-CAM heatmap."""
        grayscale_cam = self.grad_cam(
            input_tensor=input_tensor,
            target_category=target_category
        )
        return grayscale_cam

    def visualize_grad_cam(self, image, grayscale_cam):
        """Overlay Grad-CAM heatmap on original image."""
        visualization = show_cam_on_image(
            image.astype(dtype=np.float32) / 255.,
            grayscale_cam,
            use_rgb=True
        )
        return visualization

    def generate_lime_explanation(self, image, num_samples=1000):
        """Generate LIME explanation for a single prediction."""
        from lime import lime_image
        from skimage.segmentation import mark_boundaries

        explainer = lime_image.LimeImageExplainer()
        explanation = explainer.explain_instance(
            image,
            self.model.predict,
            top_labels=1,
            hide_color=0,
            num_samples=num_samples
        )

        temp, mask = explanation.get_image_and_mask(
            explanation.top_labels[0],
            positive_only=True,
            num_features=5,
            hide_rest=False
        )

        return mark_boundaries(temp / 255.0, mask)
