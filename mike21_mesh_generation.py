"""
MIKE 21 Mesh Generation
Generate flexible mesh for MIKE 21 FM.
"""

import numpy as np
from scipy.spatial import Delaunay
from pathlib import Path


class MIKE21MeshGenerator:
    def __init__(self, output_dir='mike21_mesh'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_mesh(self, boundary_coords, resolution=0.01):
        """Generate flexible mesh using Delaunay triangulation."""
        # Create boundary polygon
        boundary = np.array(boundary_coords)

        # Generate interior points
        x_min, y_min = boundary.min(axis=0)
        x_max, y_max = boundary.max(axis=0)

        x_points = np.arange(x_min, x_max, resolution)
        y_points = np.arange(y_min, y_max, resolution)
        xx, yy = np.meshgrid(x_points, y_points)
        interior_points = np.column_stack([xx.ravel(), yy.ravel()])

        # Filter points inside boundary
        from matplotlib.path import Path as MplPath
        path = MplPath(boundary)
        inside = path.contains_points(interior_points)
        interior_points = interior_points[inside]

        # Combine boundary and interior points
        all_points = np.vstack([boundary, interior_points])

        # Delaunay triangulation
        tri = Delaunay(all_points)

        # Save mesh
        self._save_mesh(all_points, tri.simplices)

        return all_points, tri.simplices

    def _save_mesh(self, points, triangles):
        """Save mesh to file."""
        mesh_file = self.output_dir / 'mesh.txt'

        with open(mesh_file, 'w') as f:
            f.write(f"{len(points)} {len(triangles)}\n")
            for p in points:
                f.write(f"{p[0]} {p[1]}\n")
            for t in triangles:
                f.write(f"{t[0]} {t[1]} {t[2]}\n")

        print(f"Mesh saved to {mesh_file}")
        print(f"  Nodes: {len(points)}")
        print(f"  Elements: {len(triangles)}")


if __name__ == "__main__":
    # Example boundary (simplified Pahang coastal region)
    boundary = [
        [103.0, 2.5],
        [105.0, 2.5],
        [105.0, 4.5],
        [103.0, 4.5],
    ]

    generator = MIKE21MeshGenerator()
    generator.generate_mesh(boundary, resolution=0.05)
