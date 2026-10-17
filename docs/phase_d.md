\# Phase D — Health Assessment \& Colour Analysis



\## Status



\- \*\*Flow B (Partial)\*\* — ✅ Complete (17 Oct 2026)

\- \*\*Flow A (Full)\*\* — 🔴 Pending (requires CoralWatch chart in future field images)



\## Flow B — What Was Built



| Sequence | Script | Output |

|---|---|---|

| D.1 | `run\_phase\_d\_1\_load\_detections.py` | `detections\_index.json` (263 colonies) |

| D.3B | `run\_phase\_d\_3\_segment\_coral.py` | `masks/` (263 bbox masks) |

| D.4B | `run\_phase\_d\_4\_coral\_crca.py` | `crca/` (263 relative colour reports) |

| D.6B | `run\_phase\_d\_6\_d\_to\_white.py` | `dwhite/` (263 relative D\_to\_White reports) |

| D.9 | `run\_phase\_d\_9\_aggregate.py` | `site\_summary.csv` (1 site) |

| D.10 | `run\_phase\_d\_10\_verify.py` | `verification.json` (all passed) |



\## Results



| Metric | Value |

|---|---|

| Colonies detected | 263 |

| Masks generated | 263 |

| Colour reports | 263 |

| D\_to\_White reports | 263 |

| Sites aggregated | 1 (C1) |

| Mean paleness | 0.4992 |



\## Flow B Limitations



\- \*\*No absolute KBI\*\* — the CoralWatch colour chart is not present in the existing 131 images

\- \*\*No calibration\*\* — cannot correlate against expert-assessed bleaching scores

\- \*\*No disease detection\*\* — model for disease types not trained

\- \*\*Relative only\*\* — paleness/D\_to\_White values are comparable within a site, not across sites or across time

\- \*\*No hypothesis testing for H2, H3\*\* — these require absolute KBI values



\## What's Needed to Upgrade to Flow A



1\. \*\*CoralWatch Coral Health Chart\*\* in every image — ordered (free from coralwatch.org), awaiting arrival for future field campaigns

2\. \*\*Expert bleaching scores\*\* for 50–100 calibration images — see Phase D doc for calibration procedure

3\. \*\*CoralSCOP\*\* for pixel-precise segmentation (optional but recommended)

4\. \*\*YOLOv11n-OBB chart detector\*\* trained on \~50 annotated chart images



\## Dependencies for Phase E



Phase E (Connectivity) consumes these Phase D Flow B outputs:

\- `site\_summary.csv` — site-level paleness/D\_to\_White ranking

\- `crca/\*.json` — per-colony colour data (for spatial mapping)

\- `masks/\*.png` — colony boundaries (for habitat maps)



\## What Was Committed



| Commit | Purpose |

|---|---|

| 3de2d3b | Phase D Flow B code (6 scripts + common logging module) |

| b98d4bb | Phase D housekeeping (resume.bat + run\_phase\_d\_flowB.bat) |



\## Files



| Path | Purpose |

|---|---|

| `src/azrai/common/logging.py` | Shared logging helper (used by all phase scripts) |

| `src/azrai/phase\_d/\_\_init\_\_.py` | Package marker |

| `scripts/phase\_d/run\_phase\_d\_\*.py` | Per-sequence runner scripts |

| `scripts/resume.bat` | Session activation (Phase 2, Sequence 2.9) |

| `scripts/run\_phase\_d\_flowB.bat` | Master runner for Flow B |

| `results/phase\_d/` | All outputs (gitignored) |



\## Next Steps



1\. \*\*Document Phase D in thesis\*\* — Chapter 4: Flow B relative analysis as proof-of-concept; Chapter 5: limitation acknowledged, Flow A as future work

2\. \*\*Await CoralWatch chart arrival\*\* — then run new field campaigns with chart in-frame

3\. \*\*Prepare Phase E\*\* — MIKE 21 FM license acquired; requires ADCP/bathymetry data

