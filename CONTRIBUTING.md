# Contributing

Thanks for helping! This design was **generated entirely by AI** and **hasn't been printed yet**, so real-world feedback is the most valuable contribution.

## Print reports (most wanted)

Built one? Please [open a print report](../../issues/new?template=print_report.md):
- your printer, filament and slicer settings;
- what fitted and what didn't: box, bearings, couplers, hygrometer, joint;
- photos, if you can.

## Reporting a problem

Use the [bug report template](../../issues/new?template=bug_report.md). Include measurements where you can, for example "the bearing pocket measures 21.8 mm".

## Changing the design

1. Edit the parametric model `src/cad/DualSpoolDryBox.sc` (see [docs/CUSTOMIZE.md](docs/CUSTOMIZE.md)).
2. If you changed a fit, check it with the coupons in [`dev/fit-tests`](dev/fit-tests).
3. Re-export the parts into `src/stl` and `src/3mf` in print orientation, keeping the file names.
4. Rebuild the print file with `python dev/tools/build_3mf.py`, and check it with `dev/tools/plates_check.py`.
5. Add a line to `CHANGELOG.md` and open a pull request with before/after renders or photos.

**Adapting to another container?** Please contribute it as a separate print file, for example `DualSpoolDryBox_<Box>_PRINT_ALL.3mf`, with the box's dimensions in the README.

Contributions made with AI help are welcome. Please say so in the pull request, the same way this project does.

## License

By contributing, you agree that your design changes are licensed under CC BY-SA 4.0 and your script changes under MIT, the same as the rest of the project.
