\# Git History — Coral Reef Kuantan



\## Overview



This document maps the actual Git commit history to the phase structure of the project.



From \*\*Phase D onwards\*\*, each phase produces exactly two commits following the standard pattern:



1\. `Add Phase N: <description>` — phase code

2\. `Housekeeping: organise Phase N scripts into scripts/phase\_N/ + append Phase N outputs to .gitignore`



Phases A, B, and C were committed before this convention was finalized. Their history is preserved as-is and documented below.



\## Actual History



| Commit | Message | Phase(s) Covered | Notes |

|---|---|---|---|

| dc8d8cb | Remove reorganize.bat from tracking | — | Pre-phase setup |

| b5277f9 | Add Phase A runner scripts + README + update .gitignore for data/models exclusion | A | Phase A code |

| 852cba9 | Housekeeping: move runner scripts to scripts/ + clean .gitignore | A | Phase A housekeeping (partial — moved scripts into `scripts/`) |

| 01c4304 | Add Phase B runner scripts (QC, murky water, enhancement, metrics, comparison) | B | Phase B code only |

| 6e71350 | Housekeeping: organise phase scripts into scripts/phase\_X/ + clean .gitignore | A, B, C | Retroactive consolidation: split flat `scripts/` into `scripts/phase\_a/`, `scripts/phase\_b/`, `scripts/phase\_c/` and consolidated `.gitignore` for all three phases |



\## Rationale



Phases A, B, and C were developed iteratively. The standardized two-commits-per-phase convention was finalized during Phase C. Rather than rewrite history — which would fabricate commits that never existed — the actual commits are preserved and mapped here for traceability.



Phases A, B, and C all conform to the standard \*structure\* (scripts organized under `scripts/phase\_X/`, `.gitignore` covering all phase outputs, one code commit + one housekeeping commit per phase), even if the commit boundaries don't map 1:1 to phase boundaries.



\## Standard from Phase D Onwards



| Phase | Commit 1 | Commit 2 |

|---|---|---|

| D | `Add Phase D: <description>` | `Housekeeping: organise Phase D scripts into scripts/phase\_d/ + append Phase D outputs to .gitignore` |

| E | `Add Phase E: <description>` | `Housekeeping: organise Phase E scripts into scripts/phase\_e/ + append Phase E outputs to .gitignore` |

| F | `Add Phase F: <description>` | `Housekeeping: organise Phase F scripts into scripts/phase\_f/ + append Phase F outputs to .gitignore` |



\## Convention Reference



For the full housekeeping procedure followed by all phases, see the Post-Execution Housekeeping section of each phase's appendix document:



\- Phase A — Sequence A.7

\- Phase B — Sequence B.8

\- Phase C — Sequence C.11

\- Phase D+ — Sequence D.X (etc.)

