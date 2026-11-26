# Maintainer area

This folder is **not needed to build the dry box**. It holds the tools used to develop and check the design.

| Folder | What |
|---|---|
| [`fit-tests/`](fit-tests) | About 14 g of small coupons cut from the real parts. They check every critical fit (box floor, bearing, axle slot, joint, hygrometer, coupler thread and slot, filament clip) before anyone prints the full set. See [`fit-tests/HOW_TO_TEST.md`](fit-tests/HOW_TO_TEST.md). |
| [`tools/`](tools) | `build_3mf.py` builds `DualSpoolDryBox_PRINT_ALL.3mf` from `src/stl`. `plates_check.py` draws the plates to check them. `diagrams.py` draws the fit-test diagrams. Python 3; `build_3mf.py` uses only the standard library, and the other two need matplotlib (plus Pillow for the labelled image). |
| `archive/` | Local only (git-ignored): superseded exports and work-in-progress images. |
