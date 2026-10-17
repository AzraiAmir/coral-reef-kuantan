"""
Setup MIKE 21 Flow Model FM directly via Python (bypassing the GUI).
"""
import os
from pathlib import Path
import mikeio

PROJECT_DIR = Path(r"C:\Users\mazra\Downloads\coral-reef-kuantan\data\external\mike\pahang_hydro")
PROJECT_DIR.mkdir(parents=True, exist_ok=True)

BATHY_FILE = PROJECT_DIR / "bathy.dfs2"

print("=== Generating MIKE 21 FM setup files ===")

# 1. Create the .m21fm file (Model Setup)
m21fm_content = """[Domain]
        domain_type = dfs2
        bathy_file = bathy.dfs2

[Time]
        simulation_start = 2024-01-01 00:00:00
        simulation_end = 2024-01-05 00:00:00

[Boundaries]
        ; Add boundary definitions here
"""
with open(PROJECT_DIR / "pahang.m21fm", "w") as f:
    f.write(m21fm_content)

print(f"✅ Created setup file: {PROJECT_DIR / 'pahang.m21fm'}")
print("\nNext step: Run the simulation via command line.")