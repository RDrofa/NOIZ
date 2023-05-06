from PyQt5.QtWidgets import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

from matplotlib.figure import Figure

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavTool

class Nav(NavTool):
    # only display the buttons we need
    toolitems = [t for t in NavTool.toolitems if
                 t[0] in ('Pan', 'Zoom')]


class Gr_map(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        F = Figure((1.0, 1.0), facecolor = (1,1,1), edgecolor = (0,0,0))

        self.canvas = FigureCanvasQTAgg(F)
        
        F.set_facecolor('gainsboro')
        
        self.ax = F.gca()


        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)

        self.canvas.axes = self.canvas.figure.add_subplot()
        self.canvas.axes.set_facecolor('gainsboro')

        self.setLayout(vertical_layout)

        #self.canvas.axes.get_xaxis().set_visible(False)
        #self.canvas.axes.get_yaxis().set_visible(False)

        self.toolbar_map = Nav(self.canvas, self)



        '''self.canvas.axes.spines['right'].set_position(('axes', 1.9))
        self.canvas.axes.spines['left'].set_position(('axes', 0.4))
        self.canvas.axes.spines['top'].set_position(('axes', 1))
        self.canvas.axes.spines['bottom'].set_position(('axes', 1))'''
     
        #cid = self.canvas.mpl_connect('button_press_event', self.onclick)

        #F.tight_layout()
        #F.tight_layout(rect=[0, 0, 0, 0])
        F.subplots_adjust(left=0, right=0.999, bottom = 0.001, top = 1)


    #def onclick(self, event):
     #   print (event.xdata, event.ydata)
        