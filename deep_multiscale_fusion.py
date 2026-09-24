"""
Deep Multiscale Fusion
Deep multiscale fusion for turbid environments.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import cv2
import numpy as np


class MultiscaleFusionModule(nn.Module):
    def __init__(self, channels=64):
        super(MultiscaleFusionModule, self).__init__()

        self.conv1 = nn.Conv2d(channels, channels, 3, 1, 1)
        self.conv2 = nn.Conv2d(channels, channels, 3, 1, 1)
        self.conv3 = nn.Conv2d(channels, channels, 3, 1, 1)

        self.fusion = nn.Conv2d(channels * 3, channels, 1, 1, 0)

    def forward(self, x):
        # Multi-scale feature extraction
        f1 = F.relu(self.conv1(x))
        f2 = F.relu(self.conv2(F.max_pool2d(x, 2)))
        f2 = F.interpolate(f2, size=x.shape[2:], mode='bilinear')
        f3 = F.relu(self.conv3(F.max_pool2d(x, 4)))
        f3 = F.interpolate(f3, size=x.shape[2:], mode='bilinear')

        # Concatenate and fuse
        concat = torch.cat([f1, f2, f3], dim=1)
        out = self.fusion(concat)

        return out


class DeepMultiscaleFusion:
    def __init__(self, device='cuda' if torch.cuda.is_available() else 'cpu'):
        self.device = device
        self.model = MultiscaleFusionModule().to(device)

    def fuse(self, image):
        """Apply multiscale fusion to image."""
        self.model.eval()
        with torch.no_grad():
            if isinstance(image, np.ndarray):
                image = torch.from_numpy(image).permute(2, 0, 1).float()
                image = image.unsqueeze(0).to(self.device)

            fused = self.model(image)
            fused = fused.squeeze(0).permute(1, 2, 0).cpu().numpy()

        return fused
