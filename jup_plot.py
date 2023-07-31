#!/usr/bin/env python
# coding: utf-8

# In[2]:


from ase import io
import math
from ase.units import Hartree,Bohr
from matplotlib.gridspec import GridSpec
from matplotlib.ticker import FormatStrFormatter
import numpy as np
from scipy.stats import norm
from scipy import stats
import matplotlib.mlab as mlab
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.ticker import AutoMinorLocator
import matplotlib as mpl
mpl.use("pgf")
import matplotlib.pyplot as plt
plt.rcParams.update({
    "font.family": "serif",  # use serif/main font for text elements
    "font.size": 9,
    "text.usetex": True,     # use inline math for ticks
    "pgf.rcfonts": False,    # don't setup fonts from rc parameters
    "pgf.preamble":"\n".join([
         r"\usepackage{amsmath}",            # load additional packages
         r"\usepackage{amssymb}",   # unicode math setup
         r"\usepackage[mathrm=sym]{unicode-math}",  # serif font via preamble
         r"\setmathfont{FiraMath-Regular.otf}",
         r"\setmainfont[BoldFont={FiraSans-SemiBold.otf}]{FiraSans-Regular.otf}",
         r"\setmathfont[version=bold]{FiraMath-Bold.otf}",
         r"\newcommand{\minus}{\scalebox{0.5}[1.0]{$-$}}" # serif font via preamble
    ])
})

color_dict = {'red':'#e6194b',
'green': '#3cb44b',
'yellow': '#ffe119',
'blue': '#4363d8',
'orange': '#f58231',
'purple': '#911eb4',
'cyan':  '#42d4f4',
'magenta': '#f032e6',
'lime':  '#bfef45',
'pink': '#fabed4',
'teal': '#469990',
'lavendar': '#dcbeff',
'brown': '#9A6324',
'beige':'#fffac8',
'maroon':'#800000',
'mint': '#aaffc3',
'olive': '#808000',
'apricot':'#ffd8b1', 
'navy':'#000075',
'grey': '#a9a9a9',
'white': '#ffffff', 
'black':'#000000'}

plt.rcParams["axes.prop_cycle"] = plt.cycler(color=['#4363d8', '#e6194B', '#3cb44b', '#f58231', '#ffe119', '#911eb4', '#42d4f4', '#f032e6', '#bfef45', '#fabed4', '#469990', '#dcbeff', '#9A6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#a9a9a9', '#ffffff', '#000000'])

# fig, axs = plt.subplots(figsize=(3.37,2),dpi=600, constrained_layout=True)
# fig, axs = plt.subplots(figsize=(6.69,2),dpi=600, constrained_layout=True)


# In[ ]:




