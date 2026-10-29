# Keycult66 and Keycult63 KiCad designs

**DRAFT C, not for fabrication or assembly.** Both variants use the same RP2040 circuit and stable key references. Open the corresponding project in **KiCad 10.0.7**. The schematic and PCB are native editable CAD.

| Variant | Project | Schematic | PCB | Validation |
| --- | --- | --- | --- | --- |
| 66 keys | [keycult66.kicad_pro](keycult66.kicad_pro) | [Schematic](keycult66.kicad_sch) | [PCB](keycult66.kicad_pcb) | [Report](reports/validation.json) |
| 63 keys | [keycult63.kicad_pro](63/keycult63.kicad_pro) | [Schematic](63/keycult63.kicad_sch) | [PCB](63/keycult63.kicad_pcb) | [Report](63/reports/validation.json) |

Both variants pass strict validation with zero ERC violations, DRC violations, unconnected items and schematic/PCB net mismatches. The reports contain the actual counts and CAD hashes. Static electrical checks do not establish powered operation or case fit. J1 implements the documented Unified Daughterboard (UDB) electrical interface; the owned Keycult daughterboard revision and stock-cable fit remain unverified. The sensor interface remains logical pads pending hardware identification.

## Review entry points

- [Native schematic](keycult66.kicad_sch), [native PCB](keycult66.kicad_pcb), [project](keycult66.kicad_pro).
- [Schematic PDF](exports/schematic.pdf), [front copper SVG](exports/front.svg), [back copper SVG](exports/back.svg), [ground plane SVG](exports/ground.svg), [layer PDF](exports/board-layers.pdf).
- 63-key exports: [schematic PDF](63/exports/schematic.pdf), [front](63/exports/front.svg), [back](63/exports/back.svg), [ground plane](63/exports/ground.svg), [layer PDF](63/exports/board-layers.pdf), [BOM](63/bom.csv), [key/GPIO map](63/gpio-map.csv).
- [Real validation summary](reports/validation.json), [KiCad ERC](reports/erc.json), [KiCad DRC including native schematic parity](reports/drc.json), [actual exported netlist](reports/netlist.xml).
The layer PDF is auto-fitted for review, **not a 1:1 print or manufacturing template**.

- [BOM with candidates/uncertainties](bom.csv), [key/GPIO map](gpio-map.csv), [QMK pin reference](qmk-config.h.example), [source/license record](sources.md).

## Implemented electrical content

66 or 63 MX PCB-mount solder switches and individual 1N4148W diodes. Cathode/pad 1 is
the ROW net; current path is COL → switch → diode anode → cathode → ROW. QMK
`COL2ROW`, five rows × fifteen columns; nine central intersections are absent in the 66-key variant and twelve in the 63-key variant. IDs, not labels, identify keys because labels repeat.

The 63-key variant omits SW7-SW9 and D7-D9 without renumbering the other parts. COL6-COL8 remain connected to bottom-row SW58-SW60. Removing only the three switches from a functioning 66-key board leaves open matrix cells; map those positions to `KC_NO` in the eventual firmware. Cutting the PCB is a separate mechanical and copper change, never implied by switch removal.

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

## USB daughterboard interface and compatibility limits

**J1 is a JST SM04B-SRSS-TB(LF)(SN), a 4-contact, 1.00mm-pitch side-entry header on B.Cu.** The [Wilba WT60-D product documentation](https://salvun.com/products/wilba-60-pcb-wt60-d) explicitly identifies its JST connection as UDB-compatible and lists Keycult No.1/60 compatibility after removing the on-board USB connector and fitting JST. The [UDB designer specification](https://github.com/Unified-Daughterboard/UDB-C-Legacy/wiki/PCB-side-design-resources) and [pinned C3 schematic](https://github.com/Unified-Daughterboard/UDB-C-Legacy/blob/2ecdd7e0482ecbd3ffe9af04966ab3555f7fc33c/KiCad/C3/Unified-Daughterboard.sch) establish the connector and pinout. This supports the UDB electrical design target; it does not identify the user's uninspected daughterboard as a particular UDB revision.

| J1 contact | Signal | Existing test pad |
| --- | --- | --- |
| 1 | VBUS_USB, USB supply before main-board F1 | TP1 |
| 2 | USB_DM, D- | TP3 |
| 3 | USB_DP, D+ | TP4 |
| 4 | GND | TP2 |
| MP | Mechanical solder anchors, tied to GND locally | Not a cable contact |

Use a **1:1 contact-number cable**, 1-to-1 through 4-to-4. Wire color and apparent left-to-right order are not pin-number evidence. TP1-TP4 retain their earlier numbering and are test access, not the connector's contact order. The validator independently checks J1 against the UDB map, including rejection of reversed power and swapped data contacts.

J1's footprint origin is PCB **(40.6,112.0)mm**, B.Cu, rotation 90 degrees, with its mouth facing keyboard-left. Looking down from the switch side, pad centres are x=42.6mm and y=113.5,112.5,111.5,110.5mm for contacts 1-4. The [official WT60-A photo](https://keycult.com/products/wt60-a-pcb-60) supports a left-edge connector facing outward, but supplies no exact coordinates. Our position is an independent placement between the ortholinear switch/diode footprints, **not a measured WT60-A connector registration**. Stock cable reach, case-channel alignment, mating clearance and the connector's full installed height below the PCB need physical checking. JST specifies a nominal 2.9mm body height; do not infer assembled clearance from the footprint courtyard alone.

J1's data pair runs together on In2.Cu along the left and top margins, referenced to the In1.Cu ground pour, then joins the existing local USB route. VBUS uses a separate 0.4mm feed to the retained main-board fuse. Trace width/gap and cable length still require stackup and signal-integrity review; the route is not impedance-qualified.

No USB-C receptacle or CC resistors are placed on the main board: CC must be handled at the daughterboard's USB-C connector. A UDB C3 schematic has CC and protection components, but **the actual Keycult board's ESD, overvoltage, fuse and shield circuitry has not been established**. Main-board F1 remains fitted; confirm total resistance/drop and protection coordination if the daughterboard also has a fuse. The [current NovelKeys replacement PCB](https://novelkeys.com/products/keycult-no-1-60-pcb) has a different board design from the old WT60-A, so its name alone does not establish the owned interface revision.

Before connection, identify the board/revision, verify all four cable paths with USB power disconnected, and check the actual connector position, cable reach and protection arrangement in issue #3. The electrical interface is implemented; installed compatibility remains conditional on those checks.

## Sensor interface remains unresolved

**TP10–TP17 are MCU-side 3.3V logical/test pads only.** They are not the Keyball
7-pin connector. There is no 5V sensor feed, no sensor connector and no approved
5V module-to-RP2040 path. Exact module revision, supply, signal levels and the
appropriate translator/interface remain open in issue #2. Do not wire these
pads straight to an unverified sensor. Reset/motion are reserved, not mandatory
PMW3360 connections. The sensor connector is not finalized; J1's electrical routing is complete but its case and cable fit is provisional.

## Geometry and construction assumptions

- Layout `(0,0)` maps to PCB **(180,100)mm**, +X right, +Y toward the bottom row. Coordinates come from `../preliminary/layout.json`, using `preferred.keys` for 66 keys and `rear_clearance.keys` for 63 keys.
- Stock `SW_Cherry_MX_1.00u_PCB` has its anchor at **electrical pin 1**, not the
  stem. The stem NPTH is local `(-2.54,+5.08)mm`; generation compensates and
  validation reads the actual stem holes. Pitch remains exactly 19.05mm.
- Both variants move the common MCU, flash, clock, power and interface-pad group 76.2mm left from the original draft, with decoupler positions adjusted separately. The original SW7-SW9 area contained essential electronics; the original board must not be cut to obtain the 63-key variant.
- The **285.0 × 94.6mm** working rectangle uses only scalar dimensions measured
  from the pinned GH60 PCB. It does **not** copy GH60's rounded corners/holes,
  any Keycult contour, or the 285.75×108.25mm plate reference rectangle.
- The 66-key all-copper-layer rule area is the centred **50 x 50mm** reservation. The 63-key rule area extends across the nominal empty key band, clipped at the board edge: PCB x=151.425..208.575mm, y=52.7..128.575mm, **57.15 x 75.875mm**. Both prohibit footprints, pads, tracks, vias and copper fill. Neither is an Edge.Cuts opening or a measured holder outline. This larger electrical reservation preserves future placement flexibility; mounting and any eventual cutout still require measurements.
- Four copper layers: F.Cu and B.Cu plus In2.Cu carry most signals. In1.Cu carries the GND reference pour outside the reserved centre, with short local +3V3 and COL12 routes beside the MCU. These routes stay away from the USB pair and the filled ground remains connected. Pad/via antipads and the central reservation still require return-path review; this is not an
  impedance-qualified stackup. Bottom SMT electronics coexist
  with top MX switch bodies, with actual drill/courtyard checks. Board thickness
  is the draft 1.6mm KiCad default, not a verified case height requirement.
- Review rules are 0.15mm clearance/minimum trace, 0.55-0.6mm via copper diameter with 0.3mm drill, and 0.25mm
  hole/copper-edge clearance. These are **draft routing constraints, not a
  selected manufacturer's process approval**. 0.4mm pitch QFN fan-out, solder
  mask, assembly tolerances and stackup need explicit manufacturing review.
- USB routes need a paired 90Ω differential/return-path review against a chosen
  stackup. Mere routed connectivity or DRC clearance does not establish signal
  integrity. QSPI/crystal/decoupling placement and path lengths need layout
  engineering review before a fabrication release.
- [3D check record](reports/3d-review.json) describes the original draft only. Neither revised variant has component-height or case-assembly approval. The current CLI environment omits component 3D libraries.
- STEP models are linked from installed KiCad stock libraries; no Keycult case
  or sensor assembly STEP is redistributed. A valid 2D board does **not** prove
  Z-stack, actuator clearance, cable bend space, assembly access or case fit.

## Reproduction

The initial seed uses KiCad's maintained `pcbnew` API and installed stock
libraries. `sexpdata` only serializes the native schematic, embedding actual
stock symbols and their electrical pin types. No custom autorouter was written.
Freerouting performs local detailed routing via KiCad's Specctra DSN/SES API.
A small cleanup script removes only KiCad-reported dead-ended copper after zone refill; it never suppresses checks or unconnected nets. Native CAD and each variant's saved SES retain the editable route.
The saved copper includes manual QFN escapes and local routing corrections. Replaying the saved SES reproduces those edits; rerunning the autorouter from a new seed does not replace layout review or guarantee completion.
See [sources](sources.md) for versions, licenses and hashes.

From the repository root, with the Python version matching KiCad's installed
binding (this Nix installation is **Python 3.14**):

```bash
uv run --python "$(command -v python3)" scripts/build_pcb.py --keys 66
uv run --python "$(command -v python3)" scripts/route_pcb.py --keys 66 --import-saved
uv run --python "$(command -v python3)" scripts/validate_pcb.py --keys 66
uv run --python "$(command -v python3)" scripts/build_pcb.py --keys 63
uv run --python "$(command -v python3)" scripts/route_pcb.py --keys 63 --import-saved
uv run --python "$(command -v python3)" scripts/validate_pcb.py --keys 63
uv run scripts/test_pcb_validation_gate.py
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

- The original draft had 57 unconnected items across 27 nets. Both revised variants complete the internal circuit and matrix routing, with zero unconnected items after rebuilding and replaying their saved copper.
- The original C13/C14 placement was 16.60/17.52mm from the MCU supply pads; these capacitors and the core decouplers have been repositioned beside their actual rotated supply pins.
- F1's MF-PSMF050X-2 candidate requires an 0805 land pattern; the original 1206 footprint has been corrected.
- USB impedance and return paths still require review against a selected stackup and the actual daughterboard/cable before bring-up. Connectivity alone is not signal-integrity qualification.
- The exposed MCU ground pad has a 0.3mm ground via. Via tenting/filling and solder-paste process must be agreed with the assembler to control solder loss; static DRC does not qualify QFN assembly.
- Local In1.Cu exceptions use 0.15mm traces: +3V3 runs `(102.32,64) -> (103,64.25) -> (106.2,64.25) -> (106.979,65.6)`; COL12 escapes through `(102.35,67.25) -> (102.35,65.5) -> (101.8,64.8) -> (98.7,64.8)`, in PCB mm. The signal is a keyboard column, not USB or QSPI. These short routes trade local ground-plane area for feasible QFN escape routing; the connected pour and USB reference region must be preserved in later edits.
- Draft validation permits unfinished connections only. Any geometric DRC
  finding fails in both strict and draft modes.

## Release gates still open

Issues #1–#6 remain the mechanical/interface/bring-up gate. No Gerber fabrication
release, production BOM, final sensor connector, module-level translator, firmware
build, USB/keyboard/sensor bench test or assembly-fit approval is supplied.
Read the exact outstanding electrical/route counts in each variant's `reports/validation.json`;
a zero ERC or a matching netlist is not a manufacturing-ready assertion.
