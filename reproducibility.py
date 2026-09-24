"""
Reproducibility
Sets random seeds and logs environment for reproducibility.
"""

import random
import numpy as np
import torch
import os
import platform
import sys
from datetime import datetime


class Reproducibility:
    def __init__(self, seed=42):
        self.seed = seed

    def set_seeds(self):
        """Set random seeds for reproducibility."""
        random.seed(self.seed)
        np.random.seed(self.seed)
        torch.manual_seed(self.seed)
        torch.cuda.manual_seed_all(self.seed)

        # For deterministic behavior
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False

        os.environ['PYTHONHASHSEED'] = str(self.seed)

        print(f"Random seeds set to {self.seed}")

    def log_environment(self, output_file='environment_log.txt'):
        """Log environment information for reproducibility."""
        with open(output_file, 'w') as f:
            f.write(f"Environment Log\n")
            f.write(f"================\n")
            f.write(f"Date: {datetime.now().isoformat()}\n")
            f.write(f"Python Version: {sys.version}\n")
            f.write(f"Platform: {platform.platform()}\n")
            f.write(f"Processor: {platform.processor()}\n")
            f.write(f"PyTorch Version: {torch.__version__}\n")
            f.write(f"CUDA Available: {torch.cuda.is_available()}\n")
            if torch.cuda.is_available():
                f.write(f"CUDA Version: {torch.version.cuda}\n")
                f.write(f"GPU: {torch.cuda.get_device_name(0)}\n")
                f.write(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB\n")
            f.write(f"NumPy Version: {np.__version__}\n")

        print(f"Environment log saved to {output_file}")

    def get_environment_info(self):
        """Get environment information as dictionary."""
        return {
            'date': datetime.now().isoformat(),
            'python_version': sys.version,
            'platform': platform.platform(),
            'processor': platform.processor(),
            'pytorch_version': torch.__version__,
            'cuda_available': torch.cuda.is_available(),
            'cuda_version': torch.version.cuda if torch.cuda.is_available() else None,
            'gpu': torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
            'numpy_version': np.__version__,
            'seed': self.seed,
        }
