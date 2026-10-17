"""
E.8 — Verify Phase E outputs.
"""
import json
from pathlib import Path
from azrai.common.logging import phase_logger

ROOT = Path(r"C:\Users\mazra\Downloads\coral-reef-kuantan")

def main():
    log = phase_logger("phase_e_8_verify")
    log.info("=== E.8 — Final Verification ===")
    
    checks = {
        "Connectivity Matrix": (ROOT / "results/phase_e/connectivity_matrix.csv").exists(),
        "DPI JSON": (ROOT / "results/phase_e/dpi.json").exists(),
    }
    
    report = {"checks": checks, "all_passed": all(checks.values())}
    out = ROOT / "results/phase_e/verification.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2))
    
    for k, v in checks.items():
        log.info(f"  {'✅' if v else '⚠️ '} {k}")
    log.info(f"All passed: {report['all_passed']}")

if __name__ == "__main__":
    main()