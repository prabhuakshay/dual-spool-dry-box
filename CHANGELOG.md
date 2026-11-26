# Changelog

All notable changes to this project. This project is 100% AI-generated (see the README).

## [2.0.0-beta] – 2026-11-26

First public release. **Not yet print-verified:** every fit was checked in CAD only.

### Design
- Cradle in two identical halves, joined by a moulded puzzle joint. A desiccant tray (about 85 g of silica) and a hygrometer pocket are built into each end.
- 8 identical wheels (Ø28 × 20 mm, one 608 bearing each), so each spool rolls on its own 4 wheels. Every wheel has a Ø32 train-wheel-style lip with a 45° guide cone on its bearing end. The lips face the towers, so they hold each spool in its lane from both sides.
- Spool fit: up to 206 mm in diameter (checked in CAD) and 50–67 mm wide.
- Keyed axles: a D-flat axle sits on flat-bottomed slots, so it can't turn.
- Low 10 mm stiffening rib between the spools (no bridges to print). The snap-in filament clip is on the tray lid tab.
- Tube-dock bridge, clamped under both feed couplers. One end is a slot, so it tolerates drilling errors. It carries 2 parking couplers that seal the PTFE tube when you're not printing.
- **DRY indicator:** square stencil letters cut through the tray end wall below the hygrometer, in front of a small chamber of colour-changing beads. The chamber is filled through a hole in the hygrometer shelf.
- All bead-facing openings are 1.4 mm wide or less, so beads of 2 mm or more can't escape.
- Guide nuts that hold the couplers on the inside, with a funnel that leads the filament into the coupler.
- Drill jig for the two 10 mm holes, with V-notches and two centre arrows in its window that line up with a pencil mark on the box.
- Large floor openings to save plastic: about 220 cm³ for the full set.

### Files
- `DualSpoolDryBox_PRINT_ALL.3mf` (a release download): every part, in its print quantity, on 3 plates (256 mm bed).
- Single-part STL and 3MF files, a STEP export, and the parametric SolidCraft model.
- Maintainer fit-test coupons in `dev/fit-tests` (about 14 g).

### How it evolved (during the AI design session)
- v1 had separate desiccant cassettes and a drilled-on hygrometer plate. These were replaced by trays and a pocket built into the cradle, which halved the plastic.
- A single full-width roller was tried and rejected, because one spool turned the other. It was replaced by independent wheels.
- The divider went from 80 to 45 mm. Once the wheel lips kept the spools apart, it became a low 10 mm rib, which also removed a 28 mm bridge from the print. The filament clip moved to the tray lid tab.
- First only the outer wheels had lips. All 8 wheels were then made identical, so there's only one wheel part and nothing to mix up.
- The floor openings were enlarged. The corner gauges for testing became full floor-quarter gauges.
