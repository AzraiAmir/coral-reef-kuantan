"""
Lagrangian Particle Tracking for Coral Larvae Dispersal
Using Parcels Framework.
"""

import numpy as np
import xarray as xr
from parcels import FieldSet, ParticleSet, JITParticle, AdvectionRK4, ErrorCode
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature


class CoralLarvaeDispersalModel:
    def __init__(self, hydrodynamic_data_path=None):
        self.hydrodynamic_data_path = hydrodynamic_data_path
        self.fieldset = None
        self.particleset = None

        self.source_sites = {
            'Pulau_Tioman': (2.8039, 104.1000),
            'Pulau_Seri_Buat': (2.7195, 103.8978),
            'Pulau_Tokong_Burung': (2.7839, 103.9601),
        }

        self.sink_sites = {
            'Pulau_Berhala': (3.2450, 103.6551),
            'Raja_Muda_Reef': (3.6412, 103.4676),
            'Balok_Reef': (3.8564, 103.4522),
        }

        self.pld_range = (6, 8)
        self.spawning_month = 4
        self.larval_mortality_rate = 0.1

    def load_hydrodynamic_data(self, u_path, v_path, dimensions):
        """Load hydrodynamic data for particle tracking."""
        u_data = xr.open_dataset(u_path)
        v_data = xr.open_dataset(v_path)

        self.fieldset = FieldSet.from_data(
            data={'U': u_data, 'V': v_data},
            dimensions=dimensions,
            mesh='spherical'
        )

        print("Hydrodynamic data loaded successfully.")
        return self.fieldset

    def create_particles(self, n_particles_per_site=1000, release_depth=5.0):
        """Create particle set for larval dispersal simulation."""
        if self.fieldset is None:
            raise ValueError("Hydrodynamic data not loaded.")

        lons = []
        lats = []

        for site_name, (lat, lon) in self.source_sites.items():
            site_lons = lon + np.random.normal(0, 0.01, n_particles_per_site)
            site_lats = lat + np.random.normal(0, 0.01, n_particles_per_site)
            lons.extend(site_lons)
            lats.extend(site_lats)

        self.particleset = ParticleSet(
            fieldset=self.fieldset,
            pclass=JITParticle,
            lon=lons,
            lat=lats,
        )

        print(f"Created {len(lons)} particles for dispersal simulation.")
        return self.particleset

    def simulate_dispersal(self, simulation_days=20, dt=timedelta(minutes=5)):
        """Run the dispersal simulation."""
        if self.particleset is None:
            raise ValueError("Particles not created.")

        def DeleteParticle(particle, fieldset, time):
            if particle.state == ErrorCode.EvolutionOutsideDomain:
                particle.delete()

        output_file = self.particleset.ParticleFile(
            name="coral_larvae_dispersal",
            outputdt=timedelta(hours=1)
        )

        self.particleset.execute(
            [AdvectionRK4, DeleteParticle],
            endtime=datetime.now() + timedelta(days=simulation_days),
            dt=dt,
            output_file=output_file,
        )

        print("Simulation complete.")
        return output_file

    def analyze_connectivity(self, output_file, sink_radius_km=10):
        """Analyze connectivity between source and sink sites."""
        data = xr.open_zarr(output_file)

        final_lons = data['lon'].isel(obs=-1).values
        final_lats = data['lat'].isel(obs=-1).values

        connectivity = np.zeros((len(self.source_sites), len(self.sink_sites)))
        source_names = list(self.source_sites.keys())
        sink_names = list(self.sink_sites.keys())

        for i, (source_name, (source_lat, source_lon)) in enumerate(self.source_sites.items()):
            for j, (sink_name, (sink_lat, sink_lon)) in enumerate(self.sink_sites.items()):
                distances = self._haversine_distance(
                    final_lats, final_lons, sink_lat, sink_lon
                )
                n_arrived = np.sum(distances <= sink_radius_km)
                connectivity[i, j] = n_arrived

        n_per_site = len(final_lons) // len(self.source_sites)
        connectivity_normalized = connectivity / n_per_site

        import pandas as pd
        connectivity_df = pd.DataFrame(
            connectivity_normalized,
            index=source_names,
            columns=sink_names
        )

        return connectivity_df

    def _haversine_distance(self, lat1, lon1, lat2, lon2):
        """Calculate Haversine distance between points."""
        R = 6371

        lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
        c = 2 * np.arcsin(np.sqrt(a))

        return R * c
