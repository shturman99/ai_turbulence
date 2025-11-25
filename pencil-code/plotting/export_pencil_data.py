#!/usr/bin/env python
from pathlib import Path
import re

import numpy as np
import pencil as pc


def export_pencil_fields_to_single_txt(
    run_dir,
    out_dir,
    out_filename="1D_Kol256_all_VAR.txt",
):
    """
    Use pc.get_sim(run_dir) and pc.read.var(...) to export
    uu and rho from all VAR* files into ONE large text file.

    Columns:
      1: var_index
      2: t
      3: x
      4: ux
      5: uy
      6: uz
      7: rho
    """

    run_dir = Path(run_dir).resolve()
    out_dir = Path(out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # Get simulation handle exactly as in your notebook
    # ------------------------------------------------------------------
    sim = pc.get_sim(str(run_dir))
    datadir = Path(sim.datadir)  # .../1D_Kol256/data

    print(f"Using run_dir: {run_dir}")
    print(f"datadir:       {datadir}")

    # Collect VAR* files (same style as your VAR loop)
    var_files = sorted(datadir.glob("proc0/VAR*"))
    if not var_files:
        raise RuntimeError(f"No VAR* files found in {datadir}")

    print("\nUsing VAR files:")
    for vf in var_files:
        print(f"  {vf.name}")

    # Output file
    out_path = out_dir / out_filename

    header = (
        "# Columns:\n"
        "# 1: var_index\n"
        "# 2: t\n"
        "# 3: x\n"
        "# 4: ux\n"
        "# 5: uy\n"
        "# 6: uz\n"
        "# 7: rho\n"
        f"# Simulation dir: {run_dir}\n"
        f"# datadir:        {datadir}\n"
    )

    with out_path.open("w") as f:
        f.write(header)

    var_index_re = re.compile(r"VAR(\d+)")

    # ------------------------------------------------------------------
    # Loop over VAR* files using the same pattern you know works
    # ------------------------------------------------------------------
    for vf in var_files:
        # This matches your working call:
        # pc.read.var(datadir=SIMS.datadir, var_file=f'VAR{i}', quiet=True, trimall=True)
        v = pc.read.var(
            datadir=str(datadir),
            var_file=vf.name,
            quiet=True,
            trimall=True,
        )

        # var_index from file name
        m = var_index_re.match(vf.name)
        var_index = int(m.group(1)) if m else -1

        # time
        t_val = float(getattr(v, "t", np.nan))

        # full velocity field from uu (same object you plotted)
        uu = v.uu  # shape should be (3, nx, 1, 1) in your 1D run
        _, nx, _, _ = uu.shape

        ux = uu[0, :, 0, 0]
        uy = uu[1, :, 0, 0]
        uz = uu[2, :, 0, 0]

        # x grid (same v.x you saw in vars.keys())
        try:
            x = np.asarray(v.x)
        except Exception:
            x = np.arange(nx)

        if x.shape[0] != nx:
            raise RuntimeError(
                f"In {vf.name}: x length {x.shape[0]} != nx {nx}"
            )

        # density from lnrho
        try:
            rho = np.exp(v.lnrho[:, 0, 0])
        except Exception:
            rho = np.full(nx, np.nan)

        # columns, all length nx
        var_col = np.full(nx, var_index)
        t_col = np.full(nx, t_val)

        table = np.column_stack([var_col, t_col, x, ux, uy, uz, rho])

        with out_path.open("a") as f:
            np.savetxt(f, table, fmt="%.8e")

        print(f"Appended {vf.name}: {nx} rows")

    print(f"\nDONE. File written to: {out_path}")
    return out_path


if __name__ == "__main__":
    # Match your notebook paths:
    PLOT_DIR = Path.cwd()
    PROJECT_ROOT = PLOT_DIR.parent
    RUNS_DIR = PROJECT_ROOT / "hydro_runs"

    run_dir = RUNS_DIR / "1D_Kol256"

    # Where you want the big text file:
    aipoincare_root = Path("/home/mgurgeni/programming/aipoincare")
    out_dir = aipoincare_root / "backend" / "data_text"

    export_pencil_fields_to_single_txt(
        run_dir=run_dir,
        out_dir=out_dir,
        out_filename="1D_Kol256_all_VAR.txt",
    )
