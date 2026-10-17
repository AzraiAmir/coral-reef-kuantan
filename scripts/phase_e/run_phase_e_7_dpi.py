"""
E.7 — Calculate Dispersal Potential Index (DPI).
"""
import json
import pandas as pd
from pathlib import Path
from azrai.common.logging import phase_logger

MATRIX_CSV = Path(r"C:\Users\mazra\Downloads\coral-reef-kuantan\results\phase_e\connectivity_matrix.csv")
OUT_JSON = Path(r"C:\Users\mazra\Downloads\coral-reef-kuantan\results\phase_e\dpi.json")

def main():
    log = phase_logger("phase_e_7_dpi")
    log.info("=== E.7 — Dispersal Potential Index (DPI) ===")

    df = pd.read_csv(MATRIX_CSV, index_col=0)
    
    # DPI = total larvae exported to any sink (excluding self-retention)
    sources = df.index
    dpi_values = {}
    
    for src in sources:
        export_prob = df.loc[src].sum() - df.loc[src, src]
        dpi_values[src] = round(float(export_prob), 4)

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(dpi_values, indent=2))
    
    log.info(f"✅ DPI calculated and saved to {OUT_JSON}")
    log.info(f"  {dpi_values}")

if __name__ == "__main__":
    main()