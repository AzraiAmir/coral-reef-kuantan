"""
Config Loader
Loads configuration from YAML files.
"""

import yaml
from pathlib import Path


class ConfigLoader:
    def __init__(self, config_path):
        self.config_path = Path(config_path)
        self.config = None

    def load(self):
        """Load configuration from YAML file."""
        with open(self.config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        return self.config

    def get(self, key, default=None):
        """Get configuration value."""
        if self.config is None:
            self.load()

        keys = key.split('.')
        value = self.config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def save(self, output_path):
        """Save configuration to YAML file."""
        with open(output_path, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False)
