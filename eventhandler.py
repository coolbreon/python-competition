
from numpy.typing import NDArray
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backend_bases import FigureCanvasBase

class Modes:
    '''
    Handles the different modes of simulation
    while handling the events assosiated with global commands
    '''
    running: bool               #controls the main loop (if False the program ends)
    paused: bool                #contols if the simulation is running or paused
    arrows: bool                #velocity arrows visible

    closeid: int                #ID of close event
    keyid: int                  #ID of keypress event
    clickid: int                #ID of mouse click event

    exporting: bool             #exporting in the current cycle
    #some events only operate when paused
    connecting: bool            #connecting temporary events in the current cycle 
    disconnecting: bool         #disconnecting temporary events in the current cycle 
    creating: bool              #creating new satellite in the current cycle
    create: NDArray             #create a new satellite at this position
    mass_to_create : float      #[kg] the created satellite will have this mass

    def __init__(self,canvas):
        '''
        Initialises Modes
        '''

        self.running=True
        self.paused=False
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
        self.mass_to_create = 1e8
        
    

    def connect(self):
        '''
        The only temporary event is the creation of anew planet with middle mouse click
        This function connects that event.
        '''
        self.clickid = plt.gcf().canvas.mpl_connect('button_press_event',self.click)

    def disconnect(self):
        '''
        This function disconnects the temporary event to make the simulation faster
        '''
        plt.gcf().canvas.mpl_disconnect(self.clickid)
        self.clickid = None
    
    def click(self,event):
        '''
        If the middle mouse button clicks somewhere on
        the canvas a new satellite is created there.
        This happens by changing createing to True and
        the create array to the current mouse position.
        The main program will create a new satellite in
        the next cycle.
        '''

        #if clicked outside of the figure nothing happens
        if event.xdata==None or event.ydata==None:
            return
        if event.button == 2:
            self.create = np.array([event.xdata,event.ydata])
            self.creating=True

    def key(self,event):
        '''
        Handles the different key press events
        '''
        #if the space is clicked the spaceclick function is called
        if event.key==' ':
            self.spaceclick()
        #if e is pressed the current layout of satellites is exported in the nex cycle
        if event.key=='e':
            self.exporting=True
        #if v is pressed the arrows can be hidden/shown (only if paused)
        if event.key=='v':
            self.arrows= not self.arrows
        #Shift increases while control decreses the mass of a satellite created in the future
        if event.key=='shift':
            self.mass_to_create=self.mass_to_create*10
        if event.key=='control':
            self.mass_to_create=self.mass_to_create/10

    def closeing(self,event):
        '''
        If the window is closed the main loop exits.
        '''
        self.running=False
    
    def spaceclick(self):
        '''
        Handles the space click, the change between paused and unpaused simmulkation
        '''
        #If it was already paused it becomes unpaused, the arrows become hidden
        #And the temporary events disconnect
        if self.paused:
            self.paused=False          
            self.arrows=False
            self.disconnecting=True
        #If it wasn't already paused it becomes paused, the arrows become visible
        #And the temporary events connect
        else:
            self.paused=True
            self.disconnecting=False
            self.connecting=True
            self.arrows=True