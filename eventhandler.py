
from numpy.typing import NDArray
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backend_bases import FigureCanvasBase

class Modes:
    running: bool
    paused: bool
    canvas: FigureCanvasBase
    closeid: int
    keyid: int
    arrows: bool #velocity arrows visible
    exporting: bool #exporting in the current cycle
    connecting: bool
    disconnecting: bool
    creating: bool
    create: NDArray
    mass_to_create : float

    def __init__(self,canvas):
        self.running=True
        self.paused=False
        self.canvas=canvas
        self.hovered=np.array([0.0,0.0])
        self.arrows=False
        self.exporting=False
        self.connecting=False
        self.disconnecting=False
        self.create=np.array([0.0,0.0])
        self.creating=False
        self.closeid = plt.gcf().canvas.mpl_connect('close_event',self.closeing)
        self.keyid = plt.gcf().canvas.mpl_connect('key_press_event',self.key)
        self.clickid = None
        self.mass_to_create = 100000
        
    

    def connect(self):
        self.clickid = plt.gcf().canvas.mpl_connect('button_press_event',self.click)

    def disconnect(self):
        plt.gcf().canvas.mpl_disconnect(self.clickid)
        self.clickid = None

    def spaceclick(self):
        if self.paused:
            self.paused=False          
            self.arrows=False
            self.disconnecting=True

        else:
            self.paused=True
            self.disconnecting=False
            self.connecting=True
            self.arrows=True
    
    def click(self,event):
        if event.button == 2:
            self.create = np.array([event.xdata,event.ydata])
            self.creating=True

    def key(self,event):
        if event.key==' ':
            self.spaceclick()
        if event.key=='e':
            self.exporting=True
        if event.key=='v':
            self.arrows= not self.arrows
        if event.key=='shift':
            self.mass_to_create=self.mass_to_create*1.4
        if event.key=='control':
            self.mass_to_create=self.mass_to_create/1.4

    def closeing(self,event):
        self.running=False