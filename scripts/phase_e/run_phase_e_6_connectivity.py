"""
E.6 — Compute Connectivity Matrix from final particle positions.
"""
import pandas as pd
from pathlib import Path
from azrai.common.logging import phase_logger

IN_CSV = Path(r"C:\Users\mazra\Downloads\coral-reef-kuantan\results\phase_e\final_positions.csv")
OUT_CSV = Path(r"C:\Users\mazra\Downloads\coral-reef-kuantan\results\phase_e\connectivity_matrix.csv")

SITES = {
    "Pulau_Tioman": (104.1, 2.8),
    "Pulau_Seri_Buat": (103.9, 2.7),
    "Pulau_Tokong_Burung": (103.95, 2.8),
    "Pulau_Berhala": (103.6, 3.2),
    "Raja_Muda": (103.4, 3.6),
    "Balok": (103.3, 3.8)
}

def find_nearest_site(lon, lat):
    min_dist = float('inf')
    nearest = "Open_Ocean"
    for name, (slon, slat) in SITES.items():
        dist = (lon - slon)**2 + (lat - slat)**2
        if dist < min_dist:
            min_dist = dist
            nearest = name
    return nearest

def main():
    log = phase_logger("phase_e_6_connectivity")
    log.info("=== E.6 — Connectivity Matrix ===")

    if not IN_CSV.exists():
        log.error(f"Missing positions file: {IN_CSV}")
        return

    df = pd.read_csv(IN_CSV)
    
    # Assign each final position to the nearest sink site
    df['sink'] = df.apply(lambda row: find_nearest_site(row['final_lon'], row['final_lat']), axis=1)
    
    # Calculate connectivity probabilities (Source -> Sink)
    sources = list(SITES.keys())[:3]
    sinks = list(SITES.keys())
    
    matrix = {s: {d: 0 for d in sinks} for s in sources}
    
    for src in sources:
        src_df = df[df['source'] == src]
        total_particles = len(src_df)
        
        for sink in sinks:
            count = len(src_df[src_df['sink'] == sink])
            matrix[src][sink] = round(count / total_particles, 4) if total_particles > 0 else 0

    out_df = pd.DataFrame(matrix).T
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    out_df.to_csv(OUT_CSV)
    
    log.info(f"✅ Matrix saved to {OUT_CSV}")
    print(out_df)

if __name__ == "__main__":
    main()