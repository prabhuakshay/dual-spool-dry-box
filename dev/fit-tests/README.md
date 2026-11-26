# Fit tests (maintainer tool)

> These coupons are for **checking the design files** (and adapting them to another box), not part of the build. Users just print `DualSpoolDryBox_PRINT_ALL.3mf` from the latest release.

**Step-by-step guide with pictures: [HOW_TO_TEST.md](HOW_TO_TEST.md).** This page is the quick-reference table.

These are small coupons cut from the real parts in `../../src/cad/DualSpoolDryBox.sc`, so each one has the same dimensions as the part it tests.
Together they use about 11 cm³ (≈14 g of PLA, ≈₹11), compared with ≈250 g for a full set. The tallest coupon is 15 mm.
Print them first and fix any failures before releasing changed files in `src/`.

**Quickest way:** open `3mf/00_ALL_TESTS_PLATE.3mf`. It holds all 13 pieces (4 floor quarter gauges and 9 coupons) on one 152 × 194 mm plate.
If your slicer asks whether to load it as a single object with multiple parts, answer **No**, so each coupon stays a separate object.

**Use the same slicer profile (layer height, walls, filament) you'll use for the real parts.**
Fits depend on how your printer prints, so a test printed with different settings proves nothing.
Infill hardly matters, since almost every coupon is solid walls.

## Run tests in two tiers

- **Tier 1, checks your box and hardware (always run):** 01, 02, 05, 06a.
- **Tier 2, checks your printer's clearances:** 03, 04, 06b, 07. Skip these if this printer already makes good press-fit and snap parts.

| # | File | Checks | Pass | If it fails, change |
|---|------|--------|------|---------------------|
| 01 | `01_FloorQuarter_x4` (4 copies, nested on the plate) | The whole box floor: length, width and all 4 corners. Each strip is one quarter of the floor outline; push one into each corner (flip 2 of them over). | The ends meet at the middle of every side, every strip lies flat, and the arcs sit evenly | A gap at a join means the box is bigger by that much; colliding ends mean it's smaller. Send me the gaps or overlaps. An arc that touches only in the middle or only at its ends means `boxR` is wrong. |
| 02 | `02_BearingRing` | 608 press fit in the wheel, and the guide lip prints cleanly | The bearing presses in with a thumb or a vice and doesn't fall out; the lip's cone has no droop | `brgD` (22.1 → 22.0 tighter, 22.2 looser) |
| 03 | `03a_AxleSlot` + `03b_AxleStub` | The axle drops into the slot flat side down and can't turn; a bearing slides onto the stub | Axle seats without forcing and won't rotate; bearing slides on by hand | `slotW`, `axD` |
| 04 | `04a_JointTab` + `04b_JointSocket` | Puzzle-joint clearance (turn the socket coupon 180°) | Presses in by hand with little play | Socket head Ø8.4 / neck 5.4 (0.2 mm clearance) |
| 05 | `05_HygroPocket` | The pocket from the floor up to just above the window bottom: shelf and fill hole, DRY chamber and letters, hygrometer fit | The hygrometer sits on the shelf without forcing, the bottom of the LCD lines up with the window, the DRY letters printed cleanly, and 2 mm beads don't pass through them | `hy_w`, `hy_d`, `hy_h`, `hy_lift` |
| 06a | `06a_CouplerThread` | The PC4-M10 coupler self-taps into the 9.2 mm bore (same bore as the guide nut) | Screws in firmly with a spanner and doesn't strip or crack | `cp_tap` (9.2 → 9.4 if it cracks, 9.0 if it strips) |
| 06b | `06b_DockSlot` | The coupler thread fits the 10.4 mm width and slides along the ±3 mm slot (the round hole is the same width) | Slides along the whole slot with little play | `cp_clear`, `slot_adj` |
| 07 | `07_FilamentClip` (tray lid tab) | 1.75 mm filament snaps in and stays put | Clicks in, holds when shaken, and pulls out by hand | Neck width 1.6 mm (1.5 = tighter, 1.7 = looser) |

Check these by measuring instead of printing:
- **Box inside height:** at least 215 mm. The spool top sits about 210 mm above the box floor.
- **Hygrometer height:** about 29 mm, so it sticks up about 8 mm above the pocket.
