from PyQt5.QtWidgets import *
import matplotlib
matplotlib.rcParams.update({'font.size': 6})

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import mplcursors
from matplotlib.figure import Figure

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavTool

class Nav(NavTool):
    # only display the buttons we need

    toolitems = [t for t in NavTool.toolitems if
                 t[0] in ('Home','Back', 'Pan', 'Zoom','Save')]

    def set_message(self, msg):
        pass




class Gr1(QWidget):



    def __init__(self, parent=None):


    
        QWidget.__init__(self, parent)

        self.F = Figure((1.0, 1.0), facecolor = (1,1,1), edgecolor = (0,0,0))

        self.F.subplots_adjust(left=0.05, right=0.85)

        self.canvas = FigureCanvasQTAgg(self.F)

 
        self.toolbar = Nav(self.canvas, self)


        #self.toolbar_G.setMinimumWidth(self.canvas.width())
        #self.toolbar_G.setMinimumHeight(self.canvas.height())


        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        #vertical_layout.addWidget(self.toolbar)
        #vertical_layout.addWidget(self.toolbar_G)

        self.canvas.axes = self.canvas.figure.add_subplot()


        mplcursors.cursor(hover=True)


        self.setLayout(vertical_layout)

        #F.tight_layout()
        #F.tight_layout(rect=[0, 0, 0, 0])


    def reCreate(self):
        self.canvas.axes = None
        self.canvas.axes = self.canvas.figure.add_subplot()




