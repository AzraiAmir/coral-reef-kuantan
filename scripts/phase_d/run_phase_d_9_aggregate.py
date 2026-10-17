"""
D.9 — Aggregate per-site health summary.
"""
import argparse
import csv
import json
import re
from collections import defaultdict
from pathlib import Path
from azrai.common.logging import phase_logger

FILENAME_PATTERN = re.compile(r"SAMPLE_(C\d+)_(DIP|POR)_(\d+)")

def parse_filename(name):
    match = FILENAME_PATTERN.search(name)
    return (match.group(1), match.group(2)) if match else (None, None)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--crca", default="results/phase_d/crca")
    parser.add_argument("--dwhite", default="results/phase_d/dwhite")
    parser.add_argument("--output", default="results/phase_d/site_summary.csv")
    args = parser.parse_args()

    log = phase_logger("phase_d_9_aggregate")
    log.info("=== D.9 — Per-site health aggregation ===")

    per_site = defaultdict(lambda: {"colonies": 0, "paleness": [], "dwhite": [], "dip": 0, "por": 0})

    for crca_file in sorted(Path(args.crca).glob("*.json")):
        crca = json.loads(crca_file.read_text())
        site, species = parse_filename(crca["image"])
        if not site: continue
        per_site[site]["colonies"] += 1
        per_site[site]["paleness"].append(crca["paleness"])
        if species == "DIP": per_site[site]["dip"] += 1
        elif species == "POR": per_site[site]["por"] += 1
        
        dwhite_file = Path(args.dwhite) / crca_file.name
        if dwhite_file.exists():
            per_site[site]["dwhite"].append(json.loads(dwhite_file.read_text())["mean_d_to_white"])

    rows = []
    for site, data in sorted(per_site.items()):
        pv, dv = data["paleness"], data["dwhite"]
        rows.append({
            "site": site, "colonies": data["colonies"], "dip_count": data["dip"], "por_count": data["por"],
            "mean_paleness": round(sum(pv) / len(pv), 4) if pv else "",
            "mean_d_to_white": round(sum(dv) / len(dv), 2) if dv else "",
        })

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys() if rows else [])
        writer.writeheader()
        writer.writerows(rows)

    log.info(f"✅ Wrote {len(rows)} sites to {out}")
    for row in rows:
        log.info(f"  {row['site']}: {row['colonies']} colonies (paleness={row['mean_paleness']})")

if __name__ == "__main__":
    main()