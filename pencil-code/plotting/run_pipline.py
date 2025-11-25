# %%
import pencil as pc
import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path

PLOT_DIR = Path.cwd()
PROJECT_ROOT = PLOT_DIR.parent
RUNS_DIR = PROJECT_ROOT / "hydro_runs"
print(f"Project root directory: {PROJECT_ROOT}")

# %%
SIMS =  pc.get_sim(RUNS_DIR/"Kol288a")

# %%
specra = pc.read.power(datadir=SIMS.datadir)

# %%
specra_kin = specra.kin

# %%
specra_kin.shape
specra.krms

# %%
specra.keys()

# %%
for line in specra_kin:
    plt.loglog(specra.krms, line, alpha=0.5, color='blue' , linewidth=0.2, linestyle="--")
plt.xlabel('Wavenumber k')
plt.ylabel('Kinetic Energy Spectrum E(k)')

# %%
vars  = []
vars = pc.read.var(datadir=SIMS.datadir,  quiet=True, trimall=True)

# %%
uu  = vars.uu

# %%
uu.shape

# %%
## Read multiple var files
vars = []
for i in range(23):
    vars_i = pc.read.var(datadir=SIMS.datadir, var_file=f'VAR{i}', quiet=True, trimall=True)
    vars.append(vars_i)

# %%
vars = np.asanyarray(vars)
vars.shape

# %%
vars[0].uu[1]

# %%
for i in range(23):
    plt.plot(vars[i].t, vars[i].uu.mean(), 'o')

# %%



