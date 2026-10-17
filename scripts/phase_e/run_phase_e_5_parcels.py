"""
E.5 — Lagrangian particle tracking using Parcels.
"""
import numpy as np
import pandas as pd
import xarray as xr
from pathlib import Path
from parcels import FieldSet, ParticleSet, JITParticle, AdvectionRK4
from azrai.common.logging import phase_logger

OUT_CSV = Path(r"C:\Users\mazra\Downloads\coral-reef-kuantan\results\phase_e\final_positions.csv")
OUT_CSV.parent.mkdir(parents=True, exist_ok=True)

SOURCES = {
    "Pulau_Tioman": (104.1, 2.8),
    "Pulau_Seri_Buat": (103.9, 2.7),
    "Pulau_Tokong_Burung": (103.95, 2.8)
}

def main():
    log = phase_logger("phase_e_5_parcels")
    log.info("=== E.5 — Parcels Particle Tracking ===")

    # 1. Create synthetic current field
    lon = np.linspace(103.0, 105.0, 50)
    lat = np.linspace(2.5, 4.5, 50)
    time = np.arange(0, 86400 * 10, 3600) 
    
    U = np.full((len(time), len(lat), len(lon)), 0.1) 
    V = np.full((len(time), len(lat), len(lon)), 0.2) 
    
    ds = xr.Dataset(
        {"U": (("time", "lat", "lon"), U), "V": (("time", "lat", "lon"), V)},
        coords={"time": time, "lat": lat, "lon": lon}
    )
    ds.to_netcdf("synthetic_currents.nc")

    filenames = {'U': 'synthetic_currents.nc', 'V': 'synthetic_currents.nc'}
    variables = {'U': 'U', 'V': 'V'}
    dimensions = {'lon': 'lon', 'lat': 'lat', 'time': 'time'}
    fieldset = FieldSet.from_netcdf(filenames, variables, dimensions)

    # 2. Release particles
    lons, lats, source_names = [], [], []
    for name, (lon, lat) in SOURCES.items():
        lons.extend([lon] * 100)
        lats.extend([lat] * 100)
        source_names.extend([name] * 100)
    
    log.info(f"Released {len(lons)} particles from {len(SOURCES)} source reefs")

    pset = ParticleSet.from_list(fieldset, JITParticle, lon=lons, lat=lats)

    # 3. Run simulation
    runtime = 8 * 24 * 3600 
    log.info("Simulating 8 days...")
    pset.execute(AdvectionRK4, runtime=runtime, dt=3600)

    # 4. Extract final positions directly from the particles
    log.info("Extracting final positions...")
    final_lon = [p.lon for p in pset]
    final_lat = [p.lat for p in pset]
    
    df = pd.DataFrame({
        "source": source_names,
        "final_lon": final_lon,
        "final_lat": final_lat
    })
    
    df.to_csv(OUT_CSV, index=False)
    log.info(f"✅ Final positions saved to {OUT_CSV}")

if __name__ == "__main__":
    main()