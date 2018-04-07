
# coding: utf-8

# # FloPy
# 
# ### ZoneBudget Example
# 
# This notebook demonstrates how to use the `ZoneBudget` class to extract budget information from the cell by cell budget file using an array of zones.
# 
# First set the path and import the required packages. The flopy path doesn't have to be set if you install flopy from a binary installer. If you want to run this notebook, you have to set the path to your own flopy path.

# In[1]:


get_ipython().magic(u'matplotlib inline')
import os
import sys
import platform
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd

# run installed version of flopy or add local path
try:
    import flopy
except:
    fpth = os.path.abspath(os.path.join('..', '..'))
    sys.path.append(fpth)
    import flopy

print(sys.version)
print('numpy version: {}'.format(np.__version__))
print('matplotlib version: {}'.format(mpl.__version__))
print('pandas version: {}'.format(pd.__version__))
print('flopy version: {}'.format(flopy.__version__))


# In[15]:


# Set path to example datafiles
loadpth = os.path.join('..', 'data', 'zonbud_examples')
cbc_f = os.path.join(loadpth, 'freyberg.wingscbc')


# ### Read File Containing Zones
# Using the `read_zbarray` utility, we can import zonebudget-style array files.

# In[3]:


from flopy.utils import read_zbarray

zone_file = os.path.join(loadpth, 'zonef_mlt.zbr')
zon = read_zbarray(zone_file)
nlay, nrow, ncol = zon.shape

fig = plt.figure(figsize=(10, 4))

for lay in range(nlay):
    ax = fig.add_subplot(1, nlay, lay+1)
    im = ax.pcolormesh(zon[lay, :, :])
    cbar = plt.colorbar(im)
    plt.gca().set_aspect('equal')
    
plt.show()
np.unique(zon)


# ### Extract Budget Information from ZoneBudget Object
# 
# At the core of the `ZoneBudget` object is a numpy structured array. The class provides some wrapper functions to help us interogate the array and save it to disk.

# In[17]:


# Create a ZoneBudget object and get the budget record array
zb = flopy.utils.ZoneBudget(cbc_f, zon, kstpkper=(0, 1096))
zb.get_budget()


# In[18]:


# Get a list of the unique budget record names
zb.get_record_names()


# In[19]:


# Look at a subset of fluxes
names = ['FROM_RECHARGE', 'FROM_ZONE_1', 'FROM_ZONE_3']
zb.get_budget(names=names)


# In[20]:


# Look at fluxes in from zone 2
names = ['FROM_RECHARGE', 'FROM_ZONE_1', 'FROM_ZONE_3']
zones = ['ZONE_2']
zb.get_budget(names=names, zones=zones)


# In[21]:


# Look at all of the mass-balance records
names = ['TOTAL_IN', 'TOTAL_OUT', 'IN-OUT', 'PERCENT_DISCREPANCY']
zb.get_budget(names=names)


# ### Convert Units
# The `ZoneBudget` class supports the use of mathematical operators and returns a new copy of the object.

# In[32]:


cmd = flopy.utils.ZoneBudget(cbc_f, zon, kstpkper=(0, 1096))
cfd = cmd / 35.3147
inyr = (cfd / (250 * 250)) * 365 * 12

cmdbud = cmd.get_budget()
cfdbud = cfd.get_budget()
inyrbud = inyr.get_budget()

names = ['FROM_STORAGE']
rowidx = np.in1d(cmdbud['name'], names)
colidx = 'ZONE_1'

print('{:,.1f} cubic meters/day'.format(cmdbud[rowidx][colidx][0]))
print('{:,.1f} cubic feet/day'.format(cfdbud[rowidx][colidx][0]))
print('{:,.1f} inches/year'.format(inyrbud[rowidx][colidx][0]))


# In[33]:


cmd is cfd


# ### Alias Names
# A dictionary of {zone: "alias"} pairs can be passed to replace the typical "ZONE_X" fieldnames of the `ZoneBudget` structured array with more descriptive names.

# In[34]:


aliases = {1: 'SURF', 2:'CONF', 3: 'UFA'}
zb = flopy.utils.ZoneBudget(cbc_f, zon, totim=[1097.], aliases=aliases)
zb.get_budget()


# ### Return the Budgets as a Pandas DataFrame
# Set `kstpkper` and `totim` keyword args to `None` (or omit) to return all times.
# The `get_dataframes()` method will return a DataFrame multi-indexed on `totim` and `name`.

# In[35]:


aliases = {1: 'SURF', 2:'CONF', 3: 'UFA'}
times = list(range(1092, 1097+1))
zb = flopy.utils.ZoneBudget(cbc_f, zon, totim=times, aliases=aliases)
zb.get_dataframes()


# Slice the multi-index dataframe to retrieve a subset of the budget.
# NOTE: We can pass "names" directly to the `get_dataframes()` method to return a subset of reocrds. By omitting the `"FROM_"` or `"TO_"` prefix we get both.

# In[43]:


dateidx1 = 1095.
dateidx2 = 1097.
names = ['FROM_RECHARGE', 'TO_WELLS', 'CONSTANT_HEAD']
zones = ['SURF', 'CONF']
df = zb.get_dataframes(names=names)
df.loc[(slice(dateidx1, dateidx2), slice(None)), :][zones]


# Look at pumpage (`TO_WELLS`) as a percentage of recharge (`FROM_RECHARGE`)

# In[44]:


dateidx1 = 1095.
dateidx2 = 1097.
zones = ['SURF']

# Pull out the individual records of interest
rech = df.loc[(slice(dateidx1, dateidx2), ['FROM_RECHARGE']), :][zones]
pump = df.loc[(slice(dateidx1, dateidx2), ['TO_WELLS']), :][zones]

# Remove the "record" field from the index so we can 
# take the difference of the two DataFrames
rech = rech.reset_index()
rech = rech.set_index(['totim'])
rech = rech[zones]
pump = pump.reset_index()
pump = pump.set_index(['totim'])
pump = pump[zones] * -1

# Compute pumping as a percentage of recharge
(pump / rech) * 100.


# In[45]:


bobj = flopy.utils.CellBudgetFile(cbc_f)
bobj.list_records()
times = bobj.get_times()
print(times)


# Pass `start_datetime` and `timeunit` keyword arguments to return a dataframe with a datetime multi-index

# In[46]:


dateidx1 = pd.Timestamp('1972-12-29')
dateidx2 = pd.Timestamp('1972-12-30')
names = ['FROM_RECHARGE', 'TO_WELLS', 'CONSTANT_HEAD']
zones = ['SURF', 'CONF']
df = zb.get_dataframes(start_datetime='1970-01-01', timeunit='D', names=names)
df.loc[(slice(dateidx1, dateidx2), slice(None)), :][zones]


# Pass `index_key` to indicate which fields to use in the multi-index (default is "totim"; valid keys are "totim" and "kstpkper")

# In[47]:


df = zb.get_dataframes(index_key='kstpkper')
df.head()


# ### Write Budget Output to CSV
# 
# We can write the resulting recarray to a csv file with the `.to_csv()` method of the `ZoneBudget` object.

# In[48]:


zb = flopy.utils.ZoneBudget(cbc_f, zon, kstpkper=[(0, 0), (0, 1096)])
f_out = os.path.join(loadpth, 'Example_output.csv')
zb.to_csv(f_out)

# Read the file in to see the contents
try:
    import pandas as pd
    print(pd.read_csv(f_out).to_string(index=False))
except:
    with open(fname, 'r') as f:
        for line in f.readlines():
            print('\t'.join(line.split(',')))


# ### Net Budget
# Using the "net" keyword argument, we can request a net budget for each zone/record name or for a subset of zones and record names. Note that we can identify the record names we want without the added `"_IN"` or `"_OUT"` string suffix.

# In[49]:


zon = np.ones((nlay, nrow, ncol), np.int)
zon[1, :, :] = 2
zon[2, :, :] = 3

aliases = {1: 'SURF', 2:'CONF', 3: 'UFA'}
times = list(range(1092, 1097+1))
zb = flopy.utils.ZoneBudget(cbc_f, zon, totim=times, aliases=aliases)
zb.get_budget(names=['STORAGE', 'WELLS'], zones=['SURF', 'UFA'], net=True)


# In[50]:


df = zb.get_dataframes(names=['STORAGE', 'WELLS'], zones=['SURF', 'UFA'], net=True)
df.head(6)


# ## Plot Budget Components
# The following is a function that can be used to better visualize the budget components using matplotlib.

# In[51]:


def tick_label_formatter_comma_sep(x, pos):
    return '{:,.0f}'.format(x)


def volumetric_budget_bar_plot(values_in, values_out, labels, **kwargs):
    if 'ax' in kwargs:
        ax = kwargs.pop('ax')
    else:
        ax = plt.gca()

    x_pos = np.arange(len(values_in))
    rects_in = ax.bar(x_pos, values_in, align='center', alpha=0.5)

    x_pos = np.arange(len(values_out))
    rects_out = ax.bar(x_pos, values_out, align='center', alpha=0.5)

    plt.xticks(list(x_pos), labels)
    ax.set_xticklabels(ax.xaxis.get_majorticklabels(), rotation=90)
    ax.get_yaxis().set_major_formatter(mpl.ticker.FuncFormatter(tick_label_formatter_comma_sep))

    ymin, ymax = ax.get_ylim()
    if ymax != 0:
        if abs(ymin) / ymax < .33:
            ymin = -(ymax * .5)
        else:
            ymin *= 1.35
    else:
        ymin *= 1.35
    plt.ylim([ymin, ymax * 1.25])

    for i, rect in enumerate(rects_in):
        label = '{:,.0f}'.format(values_in[i])
        height = values_in[i]
        x = rect.get_x() + rect.get_width() / 2
        y = height + (.02 * ymax)
        vertical_alignment = 'bottom'
        horizontal_alignment = 'center'
        ax.text(x, y, label, ha=horizontal_alignment, va=vertical_alignment, rotation=90)

    for i, rect in enumerate(rects_out):
        label = '{:,.0f}'.format(values_out[i])
        height = values_out[i]
        x = rect.get_x() + rect.get_width() / 2
        y = height + (.02 * ymin)
        vertical_alignment = 'top'
        horizontal_alignment = 'center'
        ax.text(x, y, label, ha=horizontal_alignment, va=vertical_alignment, rotation=90)

    # horizontal line indicating zero
    ax.plot([rects_in[0].get_x() - rects_in[0].get_width() / 2,
             rects_in[-1].get_x() + rects_in[-1].get_width()], [0, 0], "k")

    return rects_in, rects_out


# In[52]:


fig = plt.figure(figsize=(16, 5))

times = [2., 500., 1000., 1095.]

for idx, t in enumerate(times):

    ax = fig.add_subplot(1, len(times), idx + 1)

    zb = flopy.utils.ZoneBudget(cbc_f, zon, kstpkper=None, totim=t, aliases=aliases)

    recname = 'STORAGE'
    values_in = zb.get_dataframes(names='FROM_{}'.format(recname)).T.squeeze()
    values_out = zb.get_dataframes(names='TO_{}'.format(recname)).T.squeeze() * -1
    labels = values_in.index.tolist()

    rects_in, rects_out = volumetric_budget_bar_plot(values_in, values_out, labels, ax=ax)

    plt.ylabel('Volumetric rate, in Mgal/d')
    plt.title('{} @ totim = {}'.format(recname, t))

plt.tight_layout()
plt.show()

