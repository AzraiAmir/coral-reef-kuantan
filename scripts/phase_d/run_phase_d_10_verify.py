"""
D.10 — Verify all Phase D outputs.
"""
import argparse
import json
from pathlib import Path
from azrai.common.logging import phase_logger

PROJECT_ROOT = Path(r"C:\Users\mazra\Downloads\coral-reef-kuantan")

def check_dir(path):
    if not path.exists(): return False
    return len(list(path.glob("*.json")) + list(path.glob("*.png"))) > 0

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(PROJECT_ROOT))
    parser.add_argument("--output", default="results/phase_d/verification.json")
    args = parser.parse_args()

    log = phase_logger("phase_d_10_verify")
    log.info("=== D.10 — Final verification ===")
    root = Path(args.root)

    checks = {
        "detections_index": (root / "results/phase_d/detections_index.json").exists(),
        "masks": check_dir(root / "results/phase_d/masks"),
        "crca": check_dir(root / "results/phase_d/crca"),
        "dwhite": check_dir(root / "results/phase_d/dwhite"),
        "site_summary": (root / "results/phase_d/site_summary.csv").exists(),
    }

    report = {"flow": "B (partial)", "checks": checks, "all_passed": all(checks.values())}
    out = root / args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2))

    for k, v in checks.items():
        log.info(f"  {'✅' if v else '⚠️ '} {k}")
    log.info(f"All passed: {report['all_passed']}")

if __name__ == "__main__":
    main()