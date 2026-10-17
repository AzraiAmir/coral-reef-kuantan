"""
Generate a simple rectangular boundary file for MIKE Zero.
"""
import numpy as np

# The 4 corners of our domain (Closed loop)
lons = [103.0, 105.0, 105.0, 103.0, 103.0]
lats = [2.5, 2.5, 4.5, 4.5, 2.5]

# Create a MIKE-compatible .xyz file for boundaries
# Column 1: X (Longitude), Column 2: Y (Latitude), Column 3: Z (Dummy depth = 0)
with open("data/external/mike/boundary.xyz", "w") as f:
    for lon, lat in zip(lons, lats):
        f.write(f"{lon:.4f} {lat:.4f} 0.0\n")

print("✅ Created data/external/mike/boundary.xyz")