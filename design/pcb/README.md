# Keycult66 — native KiCad electrical/PCB review draft

**DRAFT A, not for fabrication or assembly.** This milestone implements the 66-key
baseline, not the 63-key alternative. Open `keycult66.kicad_pro` in **KiCad 10.0.7**.
The `.kicad_sch` and `.kicad_pcb` are native editable CAD, not SVG substitutes.

**Current electrical status:** ERC 0; geometric DRC rule violations 0; schematic
parity/netlist mismatches 0. **57 unconnected items on 27 nets remain**, including
MCU supply/GPIO, two flash data nets and XIN. Therefore this is a **partially
routed review draft, not a functioning or manufacturing-ready PCB**. All 66
switch/diode series cells and substantial matrix/main-circuit copper are present
(824 track segments, 102 vias in the checked snapshot). Remaining route details
are listed by endpoint in the native DRC report.

## Review entry points

- [Native schematic](keycult66.kicad_sch), [native PCB](keycult66.kicad_pcb), [project](keycult66.kicad_pro).
- [Schematic PDF](exports/schematic.pdf), [front copper SVG](exports/front.svg), [back copper SVG](exports/back.svg), [ground plane SVG](exports/ground.svg), [layer PDF](exports/board-layers.pdf).
- [Real validation summary](reports/validation.json), [KiCad ERC](reports/erc.json), [KiCad DRC including native schematic parity](reports/drc.json), [actual exported netlist](reports/netlist.xml).
The layer PDF is auto-fitted for review, **not a 1:1 print or manufacturing template**.

- [BOM with candidates/uncertainties](bom.csv), [key/GPIO map](gpio-map.csv), [QMK pin reference](qmk-config.h.example), [source/license record](sources.md).

## Implemented electrical content

66 MX PCB-mount solder switches and 66 individual 1N4148W diodes. Cathode/pad 1 is
the ROW net; current path is COL → switch → diode anode → cathode → ROW. QMK
`COL2ROW`, five rows × fifteen columns; nine central intersections intentionally
absent. IDs, not labels, identify keys because labels repeat.

RP2040 is directly mounted in its 7×7mm QFN, not represented by a development
board. The design includes AP2112K-3.3, input PTC, input/output bulk capacitors,
individual IOVDD/ADC/USB/core decoupling, the internal 1.1V regulator's 1µF caps,
W25Q16JVSSIQ QSPI flash, QSPI clock resistor, CS pull-up, BOOTSEL through 1kΩ,
12MHz ABM8-272-T3 oscillator with 15pF load caps and 1kΩ drive resistor, USB 27Ω
series resistors, RUN pull-up/reset button, and individual SWD pads. TESTEN is
GND. Unused GPIOs and regulator NC have explicit no-connect marks.

**W25Q16JVSSIQ uses the 208mil/5.3mm SOIC footprint**, not a similarly named
150mil SOIC. Passive MPNs, capacitor bias derating, crystal drive/startup and
supply thermal/load budgets remain a procurement/bring-up review, not claims of
qualification. No power LED was added. PTC hold rating does not authorize a
500mA USB device or prove USB descriptor/inrush compliance.

### GPIO budget

| Purpose | RP2040 GPIO |
|---|---|
| SPI0 MISO / CS / SCLK / MOSI | GP0 / GP1 / GP2 / GP3 |
| Rows 0–4 | GP4, GP5, GP6, GP7, GP8 |
| Columns 0–14 | GP9–GP22, GP26 |
| Optional sensor motion / reset | GP23 / GP24 |
| Explicit unused/NC | GP25 / GP27 / GP28 / GP29 |

26 of 30 GPIOs are allocated, including two optional sensor controls; four remain
unused. Dedicated QSPI, USB and SWD pins do not consume these 30 GPIOs.
`qmk-config.h.example` is a mapping aid, **not a compiled QMK port**. It does not
select a sensor revision, flash boot stage, descriptor power or a final keymap.

## Unresolved interfaces are deliberately not invented

**TP1–TP4 are individually named USB logical testpads, not a four-position JST
connector or pin-order claim.** No USB-C receptacle/CC network is placed on this
main board because the existing daughterboard is intended. Its connector,
polarity, VBUS/GND/shield arrangement, ESD/CC protection, cable and location need
issue #3 verification. No assumption of completed ESD protection is made.

**TP10–TP17 are MCU-side 3.3V logical/test pads only.** They are not the Keyball
7-pin connector. There is no 5V sensor feed, no sensor connector and no approved
5V module-to-RP2040 path. Exact module revision, supply, signal levels and the
appropriate translator/interface remain open in issue #2. Do not wire these
pads straight to an unverified sensor. Reset/motion are reserved, not mandatory
PMW3360 connections. Sensor and USB physical connector routing is not finalized.

## Geometry and construction assumptions

- Layout `(0,0)` maps to PCB **(180,100)mm**, +X right, +Y toward the bottom row.
  Coordinates come from `../preliminary/layout.json` → `preferred.keys`.
- Stock `SW_Cherry_MX_1.00u_PCB` has its anchor at **electrical pin 1**, not the
  stem. The stem NPTH is local `(-2.54,+5.08)mm`; generation compensates and
  validation reads the actual stem holes. Pitch remains exactly 19.05mm.
- The **285.0 × 94.6mm** working rectangle uses only scalar dimensions measured
  from the pinned GH60 PCB. It does **not** copy GH60's rounded corners/holes,
  any Keycult contour, or the 285.75×108.25mm plate reference rectangle.
- The centred **50×50mm all-copper-layer rule area** prohibits footprints, pads,
  tracks, vias and copper fill. It is **NOT an Edge.Cuts opening**. No machining
  hole or holder dimension has been asserted. Matrix connections detour around
  it. Actual mechanical mounting remains unresolved.
- Four copper layers: F.Cu and B.Cu plus In2.Cu carry signals; In1.Cu carries the GND
  reference pour outside the reserved centre. The checked snapshot has zero signal tracks on In1.Cu;
  pad/via antipads and the central reservation still require return-path review; this is not an
  impedance-qualified stackup. Bottom SMT electronics coexist
  with top MX switch bodies, with actual drill/courtyard checks. Board thickness
  is the draft 1.6mm KiCad default, not a verified case height requirement.
- Review rules are 0.15mm clearance/minimum trace, 0.6/0.3mm vias and 0.25mm
  hole/copper-edge clearance. These are **draft routing constraints, not a
  selected manufacturer's process approval**. 0.4mm pitch QFN fan-out, solder
  mask, assembly tolerances and stackup need explicit manufacturing review.
- USB routes need a paired 90Ω differential/return-path review against a chosen
  stackup. Mere routed connectivity or DRC clearance does not establish signal
  integrity. QSPI/crystal/decoupling placement and path lengths need layout
  engineering review before a fabrication release.
- [3D check record](reports/3d-review.json): board-only STEP export passed; component STEP export and native 3D rendering both crashed with SIGSEGV while loading models in this KiCad installation. Component heights are therefore **unverified**, not silently passed.
- STEP models are linked from installed KiCad stock libraries; no Keycult case
  or sensor assembly STEP is redistributed. A valid 2D board does **not** prove
  Z-stack, actuator clearance, cable bend space, assembly access or case fit.

## Reproduction

The initial seed uses KiCad's maintained `pcbnew` API and installed stock
libraries. `sexpdata` only serializes the native schematic, embedding actual
stock symbols and their electrical pin types. No custom autorouter was written.
Freerouting performs local detailed routing via KiCad's Specctra DSN/SES API.
The saved draft also includes explicit QFN escape vias. A small cleanup script
removes only KiCad-reported dead-ended copper after zone refill and repairs one
close same-net via pair with a physical bridge; it never suppresses checks or
unconnected nets. Native CAD and the saved SES retain the editable route.
See [sources](sources.md) for versions, licenses and hashes.

From the repository root, with the Python version matching KiCad's installed
binding (this Nix installation is **Python 3.14**):

```bash
uv run --python "$(command -v python3)" scripts/build_pcb.py
uv run --python "$(command -v python3)" scripts/route_pcb.py --import-saved
uv run --python "$(command -v python3)" scripts/validate_pcb.py --draft
uv run scripts/validate.py
```

**Regeneration overwrites the current CAD seed.** The delivered native CAD is the
review/edit surface; preserve manual edits before rebuilding. The preliminary
layout generator remains the source for key coordinates. A changed layout
requires a new seed, route and inspection, not reuse of an old route snapshot.
The saved route is a reproducible initial draft, not a promise that arbitrary
edits autoroute the same way. Validation writes actual check reports and native
SVG/PDF exports; it does not mask or exclude violations. Running validation
without `--draft` returns nonzero for *any* DRC finding or unconnected item.

## Independent layout review findings

- VREG input/output capacitors C13/C14 are currently about 16.60/17.52mm from
  the corresponding MCU pads. Relocate them close to the pins before completing
  supply routing; adding copper alone is not an acceptable fix.
- USB connector-side D−/D+ copper paths are currently about 52.13/43.75mm and
  use different layer transitions. Deliberately reroute them as a differential
  pair with continuous return paths against the selected stackup before bring-up.
- Draft validation permits unfinished connections only. Any geometric DRC
  finding fails in both strict and draft modes.

## Release gates still open

Issues #1–#6 remain the mechanical/interface/bring-up gate. No Gerber fabrication
release, production BOM, final connector, module-level translator, firmware
build, USB/keyboard/sensor bench test or assembly-fit approval is supplied.
Read the exact outstanding electrical/route counts in `reports/validation.json`;
a zero ERC or a matching netlist is not a manufacturing-ready assertion.
