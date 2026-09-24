"""
Data Versioning
Version control for datasets.
"""

import hashlib
import json
import os
from pathlib import Path
from datetime import datetime


class DataVersioning:
    def __init__(self, data_dir, version_file='data_versions.json'):
        self.data_dir = Path(data_dir)
        self.version_file = version_file
        self.versions = self._load_versions()

    def _load_versions(self):
        """Load existing versions."""
        if os.path.exists(self.version_file):
            with open(self.version_file, 'r') as f:
                return json.load(f)
        return {}

    def _save_versions(self):
        """Save versions to file."""
        with open(self.version_file, 'w') as f:
            json.dump(self.versions, f, indent=2)

    def calculate_hash(self, file_path):
        """Calculate SHA256 hash of a file."""
        sha256 = hashlib.sha256()

        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                sha256.update(chunk)

        return sha256.hexdigest()

    def create_version(self, version_name, description=""):
        """Create a new version of the dataset."""
        files = {}
        for file_path in self.data_dir.rglob('*'):
            if file_path.is_file():
                relative_path = str(file_path.relative_to(self.data_dir))
                files[relative_path] = {
                    'hash': self.calculate_hash(file_path),
                    'size': file_path.stat().st_size,
                }

        version = {
            'name': version_name,
            'description': description,
            'created_at': datetime.now().isoformat(),
            'files': files,
            'total_files': len(files),
        }

        self.versions[version_name] = version
        self._save_versions()

        print(f"Version '{version_name}' created with {len(files)} files.")

        return version

    def compare_versions(self, version1, version2):
        """Compare two versions and identify changes."""
        if version1 not in self.versions or version2 not in self.versions:
            raise ValueError("One or both versions not found.")

        v1_files = set(self.versions[version1]['files'].keys())
        v2_files = set(self.versions[version2]['files'].keys())

        added = v2_files - v1_files
        removed = v1_files - v2_files

        modified = []
        for f in v1_files & v2_files:
            if self.versions[version1]['files'][f]['hash'] != \
               self.versions[version2]['files'][f]['hash']:
                modified.append(f)

        return {
            'added': list(added),
            'removed': list(removed),
            'modified': modified,
        }
