# Customising the design

[← Back to README](../README.md)

The whole design is one parametric model: [`src/cad/DualSpoolDryBox.sc`](../src/cad/DualSpoolDryBox.sc), made in the **SolidCraft** CAD app.
Open it, change a parameter, and every part updates.
The model contains the real parts plus a few hidden stand-ins (the box, the spools, the couplers, a hygrometer) that are only there to check fit. Don't export those.

For other CAD tools there's a non-parametric [STEP export](../src/cad/DualSpoolDryBox_parts.step).

## Key parameters

All values are in millimetres.

### Box

| Parameter | Default | Meaning |
|---|---|---|
| `boxL` | 267 | Box inside floor length |
| `boxW` | 165.5 | Box inside floor width |
| `boxR` | 50 | Box inside corner radius (seen from above) |
| `clr` | 1.5 | Gap between the cradle and the box wall, each side |

To fit a **different container**, measure its inside floor and set these four. Then check that the inside height is at least about 215 mm, because the top of a 200 mm spool sits at about 210 mm.

### Spools and wheels

| Parameter | Default | Meaning |
|---|---|---|
| `spoolD` | 200 | Spool diameter for the spool stand-in. The design was checked up to 206 mm. |
| `rx` | 72 | Distance from the box centre to each axle |
| `za` | 22 | Axle height above the floor |
| `rD` | 28 | Wheel diameter |
| `ww` | 20 | Wheel width |
| `brgD` / `brgW` | 22.1 / 7 | Bearing pocket diameter (press fit for a 22 mm 608) and depth |
| `lipD` / `lipW` | 32 / 2 | Lip on every wheel's bearing end: diameter and width (it has a 1.5 mm 45° cone). Don't go above about 33 mm: the lip would hit the tray wall. The usable spool width is about 50–67 mm. |
| `axD` | 7.9 | Axle diameter (sliding fit in the 8 mm bearing bore) |
| `slotW` | 8.3 | Axle slot width |

The spool centre height is worked out from these as `zc = za + sqrt((spoolD/2 + rD/2)² − rx²)`, about 110 mm.
To lower the spool by about 5 mm, set `za = 18` and `rx = 74`. The trays then get 2 mm shorter.

### Desiccant trays and hygrometer

| Parameter | Default | Meaning |
|---|---|---|
| `tray_top` | 30 | Tray height |
| `wall` | 1.6 | Tray wall thickness |
| `hy_w` / `hy_h` / `hy_d` | 48.5 / 29 / 15.5 | Hygrometer width, height and depth |
| `hy_lift` | 10 | How far the hygrometer sticks up above the pocket, for pulling it out. It also sets the height of the DRY bead chamber under the shelf. |

The **DRY** letters are square stencil letters, 9 mm tall with 1.3 mm strokes, cut through the tray end wall (features `TxtD*`, `TxtR*`, `TxtY*`).
They're square because the wall prints vertically: square letters only need short flat bridges, while curved ones would sag.
All openings next to beads (tray slots, lid slots, letters) are 1.4 mm wide or less, so beads of 1.5 mm or more stay in.

### Couplers and tube dock

| Parameter | Default | Meaning |
|---|---|---|
| `fp` | 75 | Distance between the two couplers |
| `hz` | 196 | Coupler height above the box floor (28 mm below the rim band) |
| `cp_tap` | 9.2 | Self-tapping bore for the M10 coupler thread (guide nut, parking holes) |
| `cp_clear` | 10.4 | Clearance hole for the coupler thread (bridge) |
| `slot_adj` | 3 | ± adjustment range of the bridge's slotted end |
| `tab_t` | 2.4 | Bridge thickness where it's clamped under the coupler |

### Cradle

| Parameter | Default | Meaning |
|---|---|---|
| `floor_t` | 2.4 | Floor thickness |
| `fin_h` / `fin_t` | 10 / 2.4 | Height and thickness of the low stiffening rib between the spools. The old tall divider's features are suppressed in the model, not deleted. |

## After changing the model

1. Export each part as STL into `src/stl/` (and as 3MF into `src/3mf/`), lying in its print orientation, with the same file names. In the model, the print-oriented copies are the bodies named `Print_*`, plus `CradleHalf`, `TrayLid` and `Axle`, which are already in print orientation.
2. Rebuild the all-in-one print file:
   ```
   python dev/tools/build_3mf.py
   ```
3. Check the plate layout:
   ```
   python dev/tools/plates_check.py DualSpoolDryBox_PRINT_ALL.3mf docs/images/print_plates.png
   ```
   The print file isn't tracked in git. Attach it to a new GitHub release (`gh release create vX.Y.Z DualSpoolDryBox_PRINT_ALL.3mf`).
4. If you changed any fit (box size, bearing, coupler, hygrometer), print the coupons in [`dev/fit-tests`](../dev/fit-tests) first. They take about 14 g and check each fit before you spend 250 g on the full set.
