from math import*
import numpy as np
from numpy.typing import NDArray
import matplotlib.pyplot as plt

class Satellite:
    '''
    Definition of the Satellite object. 
    This object is a planet/satellite/asteroid floating in space,
    while gravitationally interacting with the othet Satellites
    '''

    name: str                               #name of the onject (eg. Earth)
    mass: float                             #[kg] mass of the object 
    position: NDArray[np.float64]           #[m] position vector
    velocity: NDArray[np.float64]           #[m/s] velocity vector
    position_history: NDArray[np.float64]   #[m] list of position vectors for visualisation
    
    maxpos : np.float64                     #[m] stores the length of the axes to sense if the mouse is close
    hovered : bool                          #True if the mouse is on the satellite
    selected : bool                         #True if the satellite was selected (by rightclick)
    draged : bool                           #True if the satellite is being draged (mouse pressed and on the satellite)

    pressid : int                           #stores the id of mouse click event connection
    hoverid : int                           #stores the id of mouse move event connection
    releaseid : int                         #stores the id of mouse release event connection
    keyid : int                             #stores the id of key press  event connection

    def __init__(self, name:str, mass:float, pos:NDArray[np.float64],vel:NDArray[np.float64],datapoints=1024):
        """
        Initializes the class.
        name: name of the object (e.g. Moon)
        mass: mass of the object in[kg] (e.g.7.348e22)
        pos: initial position vector [m,m] (e.g. [0, 384000000])
        vel: initial velocity vector [m/s, m/s] (e.g [-1023,0])
        datapoints: number of stored datapoints
        ...
        """
        self.name = name
        self.mass = mass
        self.position = pos
        self.velocity = vel
        self.initial_energy = np.linalg.norm(vel)**2/2
        self.actual_energy = self.initial_energy
        self.position_history = np.zeros((datapoints,2), dtype=np.float64)

        self.maxpos = max(self.position[0],self.position[1])
        self.hovered = False
        self.selected = False
        self.draged = False

        self.hoverid = None
        self.pressid = None
        self.releaseid = None
        self.keyid = None

        #fills the history array with the current position
        for i in range(datapoints):
            self.position_history[i]=self.position.copy()

    def take_input(self):
        '''
        Takes the data of an object from the user.
        '''

        self.name=input("Please give the object a name:")
        self.mass=input("Please give the object a mass [kg]: ")
        self.position[0][0]=input("Please give the initial x position: ")
        self.position[0][1]=input("Please give the initial y position: ")
        self.velocity[0][0]=input("Please give the initial x velocity: ")
        self.velocity[0][1]=input("Please give the initial y velocity: ")
    
    def __str__(self):
        '''
        Creates a readable representation of the data of an object.
        (e.g.print(Moon))
        '''
        return (f"Object '{self.name}':\n"
                f"\tMass: {self.mass} [kg]\n"
                f"\tPosition: {self.position[0]:.1f}, {self.position[1]:.1f} [m] \n"
                f"\tVelocity: {self.position[0]:.1f}, {self.position[1]:.1f} [m/s]")
    
    def __dict__(self) ->dict:
        '''
        Creates a dictionary representation of the object.
        This will be used to store a Satellite as a dictionary file
        '''
        return({'name':self.name, 
                'mass':self.mass,
                'position':self.position.tolist(),
                'velocity':self.velocity.tolist()})
     
    def move(self,dt):
        '''
        Iterates the position with the speed. 
        '''
        self.position+=self.velocity*dt

    def store(self,i):
        '''
        Stores the current position in the ith place of the history list
        '''
        self.position_history[i]=self.position.copy()
    
    def getHistory(self,i):
        '''
        Returns the stored position data as a 2D array in order.
        i is the last position with stored data.
        '''
        return(np.concatenate((self.position_history[i+1:], self.position_history[:i+1])))
    
    def connect(self):
        '''
        Connects the different events to the functions called by the events.
        Also stores the ID of the connections.
        '''
        self.hoverid=plt.gcf().canvas.mpl_connect('motion_notify_event',self.on_hover)
        self.pressid=plt.gcf().canvas.mpl_connect('button_press_event',self.on_click)
        self.releaseid=plt.gcf().canvas.mpl_connect('button_release_event',self.on_release)
        self.keyid=plt.gcf().canvas.mpl_connect('key_press_event',self.on_keypress)

    def disconnect(self):
        '''
        Disconnects the events so that the program does not need to monitor them.
        This makes the simulation faster while it is not paused.
        '''
        plt.gcf().canvas.mpl_disconnect(self.hoverid)
        plt.gcf().canvas.mpl_disconnect(self.pressid)
        plt.gcf().canvas.mpl_disconnect(self.releaseid)
        plt.gcf().canvas.mpl_disconnect(self.keyid)
    
    def on_hover(self,event):
        '''
        Handles the mouse movement event
        '''

        #If the mouse is outside the figure then this object is not draged nor hovered
        if event.xdata==None or event.ydata==None:
            self.hovered=False
            self.draged=False
            return

        #If the mouse is moved close enough to this satellite then it is 'hovered'
        if np.linalg.norm(self.position-np.array([event.xdata,event.ydata]))<self.maxpos*0.1:
                self.hovered=True
        else:
            self.hovered=False

        #If the Satellite is draged update it's position
        if self.draged:
            self.position=np.array([event.xdata,event.ydata])
    
    def on_click(self,event):
        '''
        Handles the mouse click event.
        Different things happen with right and left click.
        '''
        
        #If click is outside of the figure then the object is not selected
        if event.xdata==None or event.ydata==None:
            self.selected=False
            return
        
        #If the planet is selected then leftclick updates its velocity (converted from xdata to m/s)
        if self.selected and event.button==1:
            self.velocity=(np.array([event.xdata,event.ydata])-self.position)/self.maxpos*5e3

        #If clicked on the Satellite
        if np.linalg.norm(self.position-np.array([event.xdata,event.ydata]))<self.maxpos*0.1:
            #If it is clicked by left click the Satellite becomes draged
            if event.button==1:
                self.draged=True
            #If it is clicked by right click the Satellite becomes selected and its data is printed 
            if event.button==3:
                self.selected=True
                print(self)
        
        #If the click happens somewhere else the Satellite is unselected
        else:
            self.selected=False
    
    def on_release(self,event):
        '''
        If the mouse is released the Satellite is no longer draged
        '''
        self.draged=False

    def on_keypress(self,event):
        '''
        If a Satellite is seleced than its velocity can be modified with the arrows.
        '''
        #if the Satellite is not selected dont do anything
        if not self.selected:
            return
        #If it is selected modify its velocity in the corresponding direction
        if event.key=='right':
            self.velocity+=np.array([200,0])
        if event.key=='left':
            self.velocity+=np.array([-200,0])
        if event.key=='up':
            self.velocity+=np.array([0,200])
        if event.key=='down':
            self.velocity+=np.array([0,-200])