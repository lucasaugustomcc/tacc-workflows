import os
import sys
import platform
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import flopy
from flopy.utils import read_zbarray

# Set path to example datafiles
cbc_f = sys.argv[2]
zon = read_zbarray(sys.argv[1])

zb = flopy.utils.ZoneBudget(cbc_f, zon, kstpkper=None)
zb.to_csv(sys.argv[3])