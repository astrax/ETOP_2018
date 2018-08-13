# -*- coding: utf-8 -*-
# PART 1): Importing libraries and functions
import matplotlib
matplotlib.use("Qt5Agg")

from PyQt5.QtWidgets import QSizePolicy, QWidget, QVBoxLayout

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar

from matplotlib.figure import Figure
import matplotlib.pyplot as plt
plt.style.use(['dark_background'])
from cycler import cycler
default_cycler = cycler('color', ['r', 'g', 'b', 'y']) \
                    + cycler('linestyle', ['-', '-', '-', '-.'])

plt.rc('lines', linewidth=2)
plt.rc('axes', prop_cycle=default_cycler)

from matplotlib import rcParams
rcParams['font.size'] = 9
# PART 2): Wdget class


class MplCanvas(FigureCanvas):

    def __init__(self, dpi=100):
        self.fig = Figure(dpi=dpi)
        self.ax = self.fig.add_subplot(111)
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(
            self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


class MPL_WIDGET_2D(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.canvas = MplCanvas()  # create canvas that will hold our plot
        # createa navigation toolbar for our plot canvas
        self.navi_toolbar = NavigationToolbar(self.canvas, self)

        self.vbl = QVBoxLayout()
        self.vbl.addWidget(self.canvas)
        self.vbl.addWidget(self.navi_toolbar)
        self.setLayout(self.vbl)
