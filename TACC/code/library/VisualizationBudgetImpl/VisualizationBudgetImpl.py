#!/usr/bin/env python
import matplotlib
matplotlib.use("Agg")
import sys
import matplotlib as mpl
import matplotlib.pyplot as plt
import flopy
import zipfile

mflist = flopy.utils.MfListBudget(sys.argv[1])

flx,vol = mflist.get_dataframes(start_datetime=sys.argv[2])

flx.plot(figsize=(20,20))
plt.savefig(sys.argv[3],format = "png")

vol.plot(figsize=(20,20),subplots=True)
plt.savefig(sys.argv[4],format = "png")