# Source provenance

Downloaded 2026-10-29 from the official Keycult plate files linked by:
<https://resources.keycult.com/downloads_plate_files.html>

Files are released by Keycult for **personal, non-commercial use**; personal modifications permitted; no warranty; commercial projects/group buys require written permission. Those terms do not explicitly grant public redistribution of original or modified CAD. This repository publishes source links, checksums, non-shape-replicating measurement summaries, historical scalar results and an independently authored layout. Public SVG/HTML/PNG/PDF use only a **generic 285.75 × 108.25mm rectangular plate bounding reference**, not the official contour, tabs or corner geometry. Original STEP/DXF/Gerber files and contour replicas are not bundled. Raw upstream downloads belong in ignored `upstream/`; extracted contour coordinates and new contour-check results belong in ignored `local/`, both relative to this directory. No blanket open-source license is asserted for third-party geometry.

Archive SHA-256:

- No160-Plate.zip: `3be328eba11d3477b3b38582f3f05cd27e3659f932a92da84854634483111a6d`
- No160-Rev1-Plates.zip: `515c2f6b745b6cd816b4747c9cfb575d02b4db2ce0aa1bff7950f1d48eab2f53`

Both at `https://resources.keycult.com/plate_files/<archive-name>`.

## Original extracted file hashes (not bundled)

- `No160-Plate/No160-Plate.dxf`: `cf77d96bb3a390868e65b2a3c16c4968322974e50347dd253ace4be5debb0031`
- `No160-Plate/No160-Plate.step`: `9d0aa3e4e43d59a3c7ac1414ee1ea803b7cc62734f6eddc49ea931962168344d`
- `No160-Rev1-Plates/Plate-Leaf.step`: `b038825c91d1d2fc3b710a22fd29a635f573bbdcea330b7618c9236ea5e35846`
- `No160-Rev1-Plates/Plate-NoLeaf.step`: `bf236229c06eff56717782319b435723cf583641a0352cc77b17366bb97ccd48`
- `No160-Rev1-Plates/Plate-Partial-NoLeaf.step`: `2fc7ae692e9e290e2fe10ae7fd0c432129ba683af3f8fd38a823b4b17d3de3fa`

## Public summaries and local contour reproduction

- [`measured-official-step.json`](measured-official-step.json) remains public: it contains bounding minima, maxima and lengths, not replicated shapes. Measurement used CadQuery `importers.importStep(...).val().BoundingBox()` (OpenCascade kernel). STEP declares millimetres. Native model y is thickness, x/z are plate plan axes. All four STEP models measure 285.75 × 108.25 × 1.5mm.
- `local/measured-official-dxf.json` is ignored: it contains the exact-contour extraction, including native bulge vertices and flattened points. The initial measurement used ezdxf `readfile`, verified `$INSUNITS=4`, and selected the first closed LWPOLYLINE as the outer contour. The reproduction script reads the DXF directly from its local ZIP, verifies the same units, and selects the largest-area valid closed LWPOLYLINE. Both flatten the contour via `ezdxf.path.make_path(...).flattening(0.01)`. The plot transform is `x=-x_DXF-142.875`, `y=y_DXF-47.625`; its registration still needs comparison with the physical plate.
- [`../plate-containment.json`](../plate-containment.json) is a **historical scalar record**, not a result recomputed from the public rectangle. The original check used Shapely polygon `covers` for every 14mm switch proxy and 18mm keycap proxy, plus rectangle distance to the polygon boundary. For the 66-key layout the recorded switch/keycap minima were 2.525/0.326654mm; for the 64-key alternative, 2.525/0.525mm. It contains no contour coordinates.
- Current public layout validation uses the generic rectangular bounding reference and planar clearance calculations only. `validation.json` holds the planar layout calculations; `envelope-containment.json`, both in the parent directory, holds the independently checked rectangular-reference results. **Passing a bounding-envelope check does not prove containment within the official contour**, and even a contour check does not prove passage through the case opening or assembly fit.

To reproduce the separate official-contour check, review the upstream terms and fetch the official archive containing the DXF with the existing `python3 scripts/fetch_sources.py` procedure. Then run `uv run scripts/verify_official_contour.py` from the repository root. That script re-extracts the contour from the local official DXF and writes coordinates, fresh verification results and `layout-overlay.svg` only under ignored `design/preliminary/sources/local/`. Public generation/validation do not require those coordinates and do not silently refresh the historical public record. See [reproduction.md](../../../docs/reproduction.md) for the complete procedure.

## Keyball primary evidence

Repository pinned at `e1d1948e6e60a83f6b3566a209326508200d64ce`. The sensor Gerber outline is from the Keyball46 2022 source; the vertical installation/34mm ball guide is Keyball44 Rev.1. These are explicitly not assumed to be a single fully measured modern assembly.

Archive SHA-256 (`Trackball_PCB_gerber.zip`): `2aa537eb96839a2ab50eac6131db09bdbac6ccb62818b79a50b4a7183c5faf9e`.

- `Keyball/ball_sensor-Edge_Cuts.gbr`: `f4ba35d5204a47a20cc252e9c543d26dfe9031c7eea7ea833a6a5fb753b3c584`
- `Keyball/buildguide-excerpt.txt`: `0b3d5671324d91acb8f329876f7250deaea2663f43832767bd94741b8c3ded88`

The guide excerpt was used in the initial local investigation but is not redistributed here; use the pinned source URL in `keyball-evidence.json`. No standalone holder geometry is included or inferred from keyboard-case STL dimensions.

Checksums describe the bytes examined during the initial investigation. The source archives can be fetched and hash-checked using `python3 scripts/fetch_sources.py` from the repository root. Upstream terms are summarized in [alternatives-and-licenses.md](../../../docs/alternatives-and-licenses.md).
