# PCB source and tool provenance

Checked 2026-10-29. This is an independently authored electrical design and a
scalar working-envelope reference. **No Keycult restricted CAD, contour, STEP,
DXF, mounting-tab geometry, sensor Gerber or third-party original PCB is bundled.**
Original GH60 downloads are only in ignored `../preliminary/sources/upstream/gh60/`.

## GH60 scalar working envelope

- Author/project: komar007, GH60.
- Fixed commit: [`e7948cf44dbd3d43eb70296023a6fe3f471b44ba`](https://github.com/komar007/gh60/tree/e7948cf44dbd3d43eb70296023a6fe3f471b44ba).
- [PCB source](https://raw.githubusercontent.com/komar007/gh60/e7948cf44dbd3d43eb70296023a6fe3f471b44ba/keyboard.kicad_pcb): SHA-256 `a99aafb9f1ca77c5cac67037d161fa849b9b200de5dec9f63964520af3ff3daf`.
- [Schematic source](https://raw.githubusercontent.com/komar007/gh60/e7948cf44dbd3d43eb70296023a6fe3f471b44ba/keyboard.sch): SHA-256 `659cbbf3c524710a617a34f7e9e0e1f667a0dfc7f4fc812cc7136119a2a5d4a5`.
- [README](https://raw.githubusercontent.com/komar007/gh60/e7948cf44dbd3d43eb70296023a6fe3f471b44ba/README.md): SHA-256 `6167e6710f057082b5d1223cb28b95cfe735bf11d132adafb27dbcbe0bfd7946`.
- **License evidence and limitation:** the [designer's official project page](https://komar.blog/projects/gh60-programmable-keyboard/#downloads) labels Rev A/B/C design downloads **CC BY-SA 3.0**. The pinned repository has **no root LICENSE**, and README/CAD headers contain no explicit license notice. There is no invented LICENSE-file hash. This project does not redistribute the downloaded board/schematic or copy its footprint layout, traces, rounded contour or mounting holes; only its scalar envelope dimensions inform the new rectangle.
- Measurement: four Edge.Cuts lines and four arcs, centreline extent excluding
  graphic stroke, X 62.29…347.29mm and Y 64.62…159.22mm → **285.000×94.600mm**.
  Source thickness is 1.6002mm. Native source origin is not the new design origin.
- New board: a centred **285.0×94.6mm rectangle**, stock switch coordinates from
  the independent 66-key layout; no inherited GH60 mounting holes/USB cutout.
  This is distinct from the **285.75×108.25mm plate bounding reference**.

## Electrical references

- [Raspberry Pi, Hardware design with RP2040](https://datasheets.raspberrypi.com/rp2040/hardware-design-with-rp2040.pdf), §§2.1–2.4: power rails, decoupling, flash, USB, BOOTSEL and ABM8-272-T3 oscillator. Facts and recommended circuit values were consulted; no source CAD copied.
- [RP2040 datasheet](https://datasheets.raspberrypi.com/rp2040/rp2040-datasheet.pdf): pin functions, SPI0 GP0/1/2/3, TESTEN, USB and GPIO electrical limits.
- [W25Q16JV Rev D](https://www.winbond.com/resource-files/w25q16jv%20spi%20revd%2008122016.pdf): 2.7–3.6V, 16Mbit/2MiB, SPI/QSPI pinout; **SS = 208mil SOIC**, different from SI = 150mil. QE/boot-stage/part-ordering suffix must be checked before firmware/assembly.
- [AP2112 datasheet](https://www.diodes.com/assets/Datasheets/AP2112.pdf): 3.3V variant, enable tied to input, 1µF ceramic input/output support. Thermal dissipation and USB load remain unresolved system-level checks.
- [Bourns MF-PSMF datasheet](https://bourns.com/docs/product-datasheets/mf-psmf.pdf): MF-PSMF050X-2 is an 0805 resettable fuse. Both variants use `Fuse_0805_2012Metric`; USB budget and thermal behavior remain to be qualified.
- [QMK RP2040](https://docs.qmk.fm/platformdev_rp2040), [pointing-device driver](https://docs.qmk.fm/features/pointing_device#pmw-3360-and-pmw-3389-sensor): pin-map reference, not a copied firmware or claimed build result.
- Keyball published interface evidence and restrictions remain in the existing [design document](../preliminary/design.md) and [license comparison](../../docs/alternatives-and-licenses.md). The old Keyball46 connector is **not asserted as the actual sensor's pin order**.

## USB daughterboard evidence

Checked 2026-10-29. These sources establish an electrical design target, not the identity or measured fit of the user's installed daughterboard.

- [Wilba WT60-D at Salvun](https://salvun.com/products/wilba-60-pcb-wt60-d): describes its JST footprint as Unified Daughterboard-compatible and explicitly lists Keycult No.1/60 support after removing USB-C and soldering JST. This is the primary bridge between No.1/60 and the UDB electrical interface.
- [Keycult WT60-A](https://keycult.com/products/wt60-a-pcb-60) and its official product photograph: a left-edge, outward-facing main-board connector is visible. No exact connector coordinates or cable length are provided. The new `(40.6,112.0)mm` position is independently selected for the ortholinear PCB, not measured from this photograph.
- [NovelKeys No.1/60 replacement PCB](https://novelkeys.com/products/keycult-no-1-60-pcb): its pictured board differs from the older red WT60-A. No owned-revision identification or pinout guarantee is inferred from the replacement product name.
- [UDB PCB-side specification](https://github.com/Unified-Daughterboard/UDB-C-Legacy/wiki/PCB-side-design-resources): JST `SM04B-SRSS-TB(LF)(SN)`, 1:1 contact-number cable and identical main-board/daughterboard pinout. This archived specification is used for legacy Wilba/Keycult compatibility, not to propose replacing the installed daughterboard with a newly manufactured C3.
- [UDB C3 schematic](https://github.com/Unified-Daughterboard/UDB-C-Legacy/blob/2ecdd7e0482ecbd3ffe9af04966ab3555f7fc33c/KiCad/C3/Unified-Daughterboard.sch), commit `2ecdd7e0482ecbd3ffe9af04966ab3555f7fc33c`: J2 maps 1=VCC, 2=DN, 3=DP, 4=GND. Original Git blob `86f8bea12f75fce34009c3bc10643d38e6eaba47`; downloaded bytes SHA-256 `7d150e1e955eca3ec802049248848f61f5315a891d0e1c15e4abd5037f3fe6fb`. Local original is ignored under `../preliminary/sources/upstream/udb-c3/`. The repository is [MIT, copyright 2019 ai03](https://github.com/Unified-Daughterboard/UDB-C-Legacy/blob/2ecdd7e0482ecbd3ffe9af04966ab3555f7fc33c/LICENSE). No source CAD, artwork or layout is redistributed; the new connector uses stock KiCad symbols/footprints and independently authored copper.
- [JST SH series datasheet](https://www.jst-mfg.com/product/pdf/eng/eSH.pdf), pages 1-3: 1.00mm pitch, side-entry header and mounting-surface pin numbering; `SHR-04V-S` mating housing and nominal 2.9mm header body height. Installed height and cable clearance still require a case model or measurements.
- C3's CC/ESD/overvoltage/fuse/shield implementation is evidence about **C3 only**. It is not evidence that the unidentified Keycult daughterboard carries those components. The main-board fuse remains, and protection coordination is an open assembly requirement.

## Maintained tools and stock libraries

- **KiCad 10.0.7** GUI/CLI and its installed Python `pcbnew` binding, Python 3.14.7.
  Native ERC, DRC, zone refill, schematic parity, XML netlist, PDF/SVG exports and
  Specctra transfer are performed by KiCad, not fabricated report text.
- Installed **kicad-symbols revision `1b2b42d49b`**, **kicad-footprints revision
  `25a0b01dd7`**, **kicad-packages3d revision `dd37eac8d2`** (Nix package labels).
  Project tables use `${KICAD10_SYMBOL_DIR}` / `${KICAD10_FOOTPRINT_DIR}`; stock
  symbols are embedded in the schematic and stock footprints in the PCB.
  No global library configuration is modified.
- [KiCad library license](https://www.kicad.org/libraries/license/): CC BY-SA 4.0
  with the KiCad library exception for use in electronic designs. Embedded stock
  content is attributable to the KiCad library contributors; this does not
  relicense third-party CAD or assert a blanket license over this repository.
- `sexpdata 1.0.2`: maintained S-expression serialization; `shapely 2.1.2`:
  independent geometry checks; `pymupdf 1.26.7`: readback/raster inspection of the
  actual KiCad-generated PDF. Their dependencies are declared in scripts.
- [Freerouting **v2.0.1**](https://github.com/freerouting/freerouting/releases/tag/v2.0.1), GPL-3.0 tool, run locally with Java 21. The installed Java21 cannot execute the newer Java25-built v2.5.0, so v2.0.1 is explicitly pinned. The JAR is ignored, not bundled. Usage analytics are disabled via `--usage_and_diagnostic_data.disable_analytics=true`; no cloud routing service is used. Routing output is our board data, not copied router source.

The exact router artifact checksum and route-snapshot checksums are recorded in
[route-manifest.json](route-manifest.json). Saved SES files contain only this
independent design's editable copper connectivity. Hash mismatches must be
investigated; do not silently replace pinned inputs.

The 63-key route has its own [manifest](63/route-manifest.json). The router wrapper rejects empty/invalid SES output before replacing a saved route and retries up to three times for the v2.0.1 CLI export race: its CLI observes `COMPLETED` before the scheduler has necessarily populated the output bytes. The upstream [CLI](https://github.com/freerouting/freerouting/blob/v2.0.1/src/main/java/app/freerouting/Freerouting.java) and [scheduler](https://github.com/freerouting/freerouting/blob/v2.0.1/src/main/java/app/freerouting/management/RoutingJobScheduler.java) establish this ordering. The tool JAR is unchanged.
