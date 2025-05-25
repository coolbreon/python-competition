from math import*
import numpy as np
from numpy.typing import NDArray
import matplotlib.pyplot as plt
from math import *
fig, ax = plt.subplots()

class Satellite:

    name: str
    mass: float
    position: NDArray[np.float64]
    velocity: NDArray[np.float64]
    position_history: NDArray[np.float64]
    init_energy: float
    #firstIndex: int                       # First index with stored data
    #lastIndex: int                        # Next free index for storing data
    #maxIndex: int                         # Number of stored data points

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

class Modes:
    running: bool
    paused: bool
    #canvas: plt.figure.Figure
    hoverid: int
    clickid: int
    hovered: NDArray[np.float64] #last hovered point
    arrows: bool #velocity arrows visible
    def __init__(self,canvas):
        self.running=True
        self.paused=False
        self.canvas=canvas
        self.hovered=np.array([0.0,0.0])
        self.arrows=False
    def spaceclick(self):
        if self.paused:
            self.paused=False
            plt.gcf().canvas.mpl_disconnect(self.hoverid)
            
            self.arrows=False
        else:
            self.paused=True
            self.hoverid=plt.gcf().canvas.mpl_connect('motion_notify_event',self.hover)
            self.arrows=True
    def key(self,event):
        if event.key==' ':
            self.spaceclick()
    
    def closeing(self,event):
        self.running=False
    def hover(self,event):
        self.hovered=np.array([event.xdata,event.ydata])


def closeto(arr1:NDArray,arr2:NDArray,maxposx,maxposy):
    trashold=0.04
    maxaxislength=max(maxposx[1]-maxposx[0],maxposy[1]-maxposy[0])
    
    if np.linalg.norm(arr1-arr2)<maxaxislength*trashold:
        return True
    else:
        return False
  

def acceleration(sat1,sat2,G,dt):
        '''
        Calculates the gravitational force between two objects.
        From this it calculates the accelerations and iterates with that.
        '''

        #Calculate distance
        r_vec = sat1.position-sat2.position
        dist = np.linalg.norm(r_vec)
        unit_vector = r_vec/dist                      
        
        #Calculate the unit vector pointing from self planet to other planet
        F=unit_vector*G*(sat1.mass*sat2.mass)/(dist**2)    
        
        #Newton's second law
        a1=-F/sat1.mass                                    
        a2=F/sat2.mass
        
        #Iteration
        sat1.velocity=sat1.velocity+a1*dt
        sat2.velocity=sat2.velocity+a2*dt


def importjson(lst,datapoints):
    planets=[]
    for p in lst:
        
        planets.append(
            Satellite(name=p['name'], 
                mass=float(p['mass']),
                pos=np.array(p['position']),
                vel=np.array(p['velocity'] ),
                datapoints=datapoints))
    return(planets)

def new_frame(planet, maxposx, maxposy): 
    '''
    Finds new maxima and minima to which the coordinate frame should be adjusted
    '''
    if planet.position[0] > maxposx[1]:
        maxposx[1]=planet.position[0]
    elif planet.position[0] < maxposx[0]:
        maxposx[0]=planet.position[0]
    if planet.position[1] > maxposy[1]:
        maxposy[1]=planet.position[1]
    elif planet.position[1] < maxposy[0]:
        maxposy[0]=planet.position[1]
    return [maxposx,maxposy]

def get_system_energy(planets,G,):
    e_kinetic=0.0
    e_potential=0.0
    for i,p in enumerate(planets):
        e_kinetic+=0.5*p.mass*(np.linalg.norm(p.velocity))**2
        for j,q in enumerate(planets[(i+1):]):
            e_potential-=G*p.mass*q.mass/np.linalg.norm(p.position-q.position)
    return e_kinetic+e_potential