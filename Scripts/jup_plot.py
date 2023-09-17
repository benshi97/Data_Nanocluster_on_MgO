#!/usr/bin/env python
# coding: utf-8

# Script to set up the plotting environment for Jupyter notebooks
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator


def texfalse_import():
    plt.rcParams.update(
        {
            "font.family": "sans serif",  # use serif/main font for text elements
            "font.size": 8,
            "text.usetex": False,  # use inline math for ticks
        }
    )

def textrue_import():
    import matplotlib as mpl
    mpl.use("pgf")
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

# Dictionary of colors for the color scheme in our plots
color_dict = {
    "red": "#e6194b",
    "green": "#3cb44b",
    "yellow": "#ffe119",
    "blue": "#4363d8",
    "orange": "#f58231",
    "purple": "#911eb4",
    "cyan": "#42d4f4",
    "magenta": "#f032e6",
    "lime": "#bfef45",
    "pink": "#fabed4",
    "teal": "#469990",
    "lavendar": "#dcbeff",
    "brown": "#9A6324",
    "beige": "#fffac8",
    "maroon": "#800000",
    "mint": "#aaffc3",
    "olive": "#808000",
    "apricot": "#ffd8b1",
    "navy": "#000075",
    "grey": "#a9a9a9",
    "white": "#ffffff",
    "black": "#000000",
}

# Colors to cycle through for our plots
plt.rcParams["axes.prop_cycle"] = plt.cycler(
    color=[
        "#4363d8",
        "#e6194B",
        "#3cb44b",
        "#f58231",
        "#ffe119",
        "#911eb4",
        "#42d4f4",
        "#f032e6",
        "#bfef45",
        "#fabed4",
        "#469990",
        "#dcbeff",
        "#9A6324",
        "#fffac8",
        "#800000",
        "#aaffc3",
        "#808000",
        "#ffd8b1",
        "#000075",
        "#a9a9a9",
        "#ffffff",
        "#000000",
    ]
)

# Script for plotting radial plots
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D
import numpy as np


def radar_factory(num_vars, frame='circle',rotation=0):
    """
    Create a radar chart with `num_vars` axes.

    This function creates a RadarAxes projection and registers it.

    Parameters
    ----------
    num_vars : int
        Number of variables for radar chart.
    frame : {'circle', 'polygon'}
        Shape of frame surrounding axes.

    """
    # calculate evenly-spaced axis angles
    theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False) 

    class RadarTransform(PolarAxes.PolarTransform):

        def transform_path_non_affine(self, path):
            # Paths with non-unit interpolation steps correspond to gridlines,
            # in which case we force interpolation (to defeat PolarTransform's
            # autoconversion to circular arcs).
            if path._interpolation_steps > 1:
                path = path.interpolated(num_vars)
            return Path(self.transform(path.vertices), path.codes)

    class RadarAxes(PolarAxes):

        name = 'radar'
        PolarTransform = RadarTransform

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # rotate plot such that the first axis is at the top
            self.set_theta_zero_location('N')
            self.set_theta_offset(rotation)


        def fill(self, *args, closed=True, **kwargs):
            """Override fill so that line is closed by default"""
            return super().fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super().plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.append(x, x[0])
                y = np.append(y, y[0])
                line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels)

        def _gen_axes_patch(self):
            # The Axes patch must be centered at (0.5, 0.5) and of radius 0.5
            # in axes coordinates.
            if frame == 'circle':
                return Circle((0.5, 0.5), 0.5)
            elif frame == 'polygon':
                return RegularPolygon((0.5, 0.5), num_vars,
                                      radius=.5, edgecolor="k",orientation=rotation)
                # return RegularPolygon((0.5, 0.5), num_vars,
                #                       radius=.5, edgecolor="k")
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)

        def _gen_axes_spines(self):
            if frame == 'circle':
                return super()._gen_axes_spines()
            elif frame == 'polygon':
                # spine_type must be 'left'/'right'/'top'/'bottom'/'circle'.
                spine = Spine(axes=self,
                              spine_type='circle',
                              path=Path.unit_regular_polygon(num_vars))
                # unit_regular_polygon gives a polygon of radius 1 centered at
                # (0, 0) but we want a polygon of radius 0.5 centered at (0.5,
                # 0.5) in axes coordinates.
                # spine.set_transform(Affine2D().scale(.5).translate(.5, .5)
                #                     + self.transAxes)
                spine.set_transform(Affine2D().rotate(rotation).scale(.5).translate(.5, .5)
                                    + self.transAxes)
                # print(spine)
                return {'polar': spine}
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)

    register_projection(RadarAxes)
    return theta
