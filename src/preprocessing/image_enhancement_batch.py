"""
Image Enhancement Batch
Batch process image enhancement for large datasets.
"""

import os
import cv2
import numpy as np
from pathlib import Path
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed

from traditional_enhancement import TraditionalEnhancer
from dl_enhancement import UnderwaterImageEnhancerDL


class BatchEnhancer:
    def __init__(self, method='traditional', num_workers=4):
        self.method = method
        self.num_workers = num_workers

        if method == 'traditional':
            self.enhancer = TraditionalEnhancer()
        elif method == 'deep_learning':
            self.enhancer = UnderwaterImageEnhancerDL()
        else:
            raise ValueError(f"Unknown method: {method}")

    def enhance_single(self, input_path, output_path):
        """Enhance a single image."""
        image = cv2.imread(str(input_path))
        if image is None:
            return False

        if self.method == 'traditional':
            enhanced = self.enhancer.enhance(image)
        else:
            enhanced = self.enhancer.enhance(image)

        cv2.imwrite(str(output_path), enhanced)
        return True

    def enhance_batch(self, input_dir, output_dir):
        """Enhance a batch of images using parallel processing."""
        input_dir = Path(input_dir)
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        image_paths = list(input_dir.glob("*.jpg")) + list(input_dir.glob("*.png"))

        print(f"Enhancing {len(image_paths)} images using {self.method} method...")

        success_count = 0
        with tqdm(total=len(image_paths)) as pbar:
            for input_path in image_paths:
                output_path = output_dir / input_path.name
                if self.enhance_single(input_path, output_path):
                    success_count += 1
                pbar.update(1)

        print(f"Successfully enhanced {success_count}/{len(image_paths)} images.")
        return success_count

    def enhance_with_qc(self, input_dir, output_dir):
        """Enhance images and apply quality control."""
        from quality_control import ImageQualityControl

        qc = ImageQualityControl()
        input_dir = Path(input_dir)
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        image_paths = list(input_dir.glob("*.jpg"))
        results = []

        for input_path in tqdm(image_paths):
            qc_result = qc.assess_quality(str(input_path))

            if qc_result['pass']:
                output_path = output_dir / input_path.name
                self.enhance_single(input_path, output_path)
                results.append({
                    'filename': input_path.name,
                    'passed_qc': True,
                    'enhanced': True,
                })
            else:
                results.append({
                    'filename': input_path.name,
                    'passed_qc': False,
                    'reason': qc_result.get('reason', 'quality'),
                })

        return results


if __name__ == "__main__":
    enhancer = BatchEnhancer(method='traditional', num_workers=4)
    enhancer.enhance_batch(
        input_dir="raw_images/",
        output_dir="enhanced_images/"
    )
