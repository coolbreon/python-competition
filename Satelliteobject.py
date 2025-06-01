from math import*
import numpy as np
from numpy.typing import NDArray
import matplotlib.pyplot as plt

class Satellite:

    name: str
    mass: float
    position: NDArray[np.float64]
    velocity: NDArray[np.float64]
    position_history: NDArray[np.float64]
    init_energy: float

    maxpos : np.float64
    hovered : bool
    selected : bool
    draged : bool

    pressid : int
    hoverid : int
    releaseid : int
    keyid : int

    def __init__(self, name:str, mass:float, pos:NDArray[np.float64],vel:NDArray[np.float64],datapoints=1024):
        """
        Initializes the class.

        name: name of the object (e.g. Moon)
        mass: mass of the object in[kg] (e.g.7.348e22)
        pos: initial position vector [m,m] (e.g. [0, 384000000])
        vel: initial velocity vector [m/s, m/s] (e.g [-1023,0])
        datapoints: number of stored datapoints
        """
        self.name=name
        self.mass=mass
        self.position=pos
        self.velocity=vel
        self.initial_energy=np.linalg.norm(vel)**2/2
        self.actual_energy=self.initial_energy
        self.position_history=np.zeros((datapoints,2), dtype=np.float64)

        self.maxpos=max(self.position[0],self.position[1])
        self.hovered=False
        self.selected=False
        self.draged=False

        self.hoverid=None
        self.pressid=None
        self.releaseid=None
        self.keyid=None

        for i in range(datapoints):
            self.position_history[i]=self.position.copy()

    #Take values from user:
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
    
    #Print out own values:
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
        return({'name':self.name, 
                'mass':self.mass,
                'position':self.position.tolist(),
                'velocity':self.velocity.tolist()})
    
    
    #modifies position and velocity 
    def move(self,dt):
        '''
        Iterates the position with the speed. 
        Also stores the new position in the self.history array.
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
        i is the last position with stored data
        '''
        return(np.concatenate((self.position_history[i+1:], self.position_history[:i+1])))
    
    def connect(self):
        self.hoverid=plt.gcf().canvas.mpl_connect('motion_notify_event',self.on_hover)
        self.pressid=plt.gcf().canvas.mpl_connect('button_press_event',self.on_click)
        self.releaseid=plt.gcf().canvas.mpl_connect('button_release_event',self.on_release)
        self.keyid=plt.gcf().canvas.mpl_connect('key_press_event',self.on_keypress)

    def disconnect(self):
        plt.gcf().canvas.mpl_disconnect(self.hoverid)
        plt.gcf().canvas.mpl_disconnect(self.pressid)
        plt.gcf().canvas.mpl_disconnect(self.releaseid)
        plt.gcf().canvas.mpl_disconnect(self.keyid)
    
    def on_hover(self,event):
        if event.xdata==None or event.ydata==None:
            return

        if np.linalg.norm(self.position-np.array([event.xdata,event.ydata]))<self.maxpos*0.1:
                self.hovered=True
        else:
            self.hovered=False

        if self.draged:
            self.position=np.array([event.xdata,event.ydata])
    
    def on_click(self,event):
        if event.xdata==None or event.ydata==None:
            self.selected=False
            return
        close=np.linalg.norm(self.position-np.array([event.xdata,event.ydata]))<self.maxpos*0.1
        if self.selected and event.button==1:
            self.velocity=(np.array([event.xdata,event.ydata])-self.position)/self.maxpos*5e3
        if close:
            if event.button==1:
                self.draged=True 
            if event.button==3:
                self.selected=True
                print(self)
        
        else:
            self.selected=False
    
    def on_release(self,event):
        self.draged=False

    def on_keypress(self,event):
        if event.key=='right' and self.selected:
            self.velocity+=np.array([200,0])
        if event.key=='left' and self.selected:
            self.velocity+=np.array([-200,0])
        if event.key=='up' and self.selected:
            self.velocity+=np.array([0,200])
        if event.key=='down' and self.selected:
            self.velocity+=np.array([0,-200])