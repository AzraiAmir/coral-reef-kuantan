"""
E.1 — Convert GEBCO GeoTIFF to XYZ format for MIKE 21 mesh generation.
"""
from pathlib import Path
import rasterio
import numpy as np
from azrai.common.logging import phase_logger

BATHY_TIF = Path(r"C:\Users\mazra\Downloads\coral-reef-kuantan\data\external\bathymetry\gebco_pahang.tif")
OUT_XYZ = Path(r"C:\Users\mazra\Downloads\coral-reef-kuantan\data\external\bathymetry\mike_bathy.xyz")

def main():
    log = phase_logger("phase_e_1_bathymetry")
    log.info("=== E.1 — Extract Bathymetry for MIKE ===")

    if not BATHY_TIF.exists():
        log.error(f"Missing file: {BATHY_TIF}")
        return

    with rasterio.open(BATHY_TIF) as src:
        elev = src.read(1)
        transform = src.transform
        log.info(f"Loaded GEBCO grid: {src.shape[0]} x {src.shape[1]}")
        log.info(f"Bounds: {list(src.bounds)}")

    # Generate XYZ grid
    rows, cols = elev.shape
    lons = []
    lats = []
    depths = []

    for r in range(rows):
        for c in range(cols):
            # Calculate lon/lat from pixel coordinates
            lon, lat = transform * (c, r)
            z = elev[r, c]
            if z < 0: # Valid ocean depth (GEBCO uses negative for below sea level)
                lons.append(lon)
                lats.append(lat)
                depths.append(z)

    # Write XYZ file
    OUT_XYZ.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_XYZ, "w") as f:
        for lon, lat, z in zip(lons, lats, depths):
            f.write(f"{lon:.6f} {lat:.6f} {z:.2f}\n")

    log.info(f"✅ Exported {len(lons):,} points to {OUT_XYZ}")

if __name__ == "__main__":
    main()