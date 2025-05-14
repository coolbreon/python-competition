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
      

def acceleration(sat1,sat2,G,dt):
        '''
        Calculates the gravitational force between two objects.
        From this it calculates the accelerations and iterates with that.
        '''

        #Calculate distance
        r_vec=sat1.position-sat2.position
        dist = np.linalg.norm(r_vec)
        unit_vector = r_vec/dist                      
        
        #Calculate the unit vector pointing from self planet to other planet
        F=unit_vector*(G*sat1.mass*sat2.mass)/(dist**2)    
        
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
                mass=['mass'],
                pos=np.array(p['position']),
                vel=np.array(p['velocity'] ),
                datapoints=datapoints))
    return(planets)


class Trajectory:
    def __init__(self):#data is the number of stored datapoints
        self.center = np.array([0,0]) 
        self.a = 1000 #[m]
        self.b = 1000 #[m]
        self.angle = 0 #[rad]
    def calculate(self, pos, vel, earth,G):
        
        mu=earth.mass*G #calculates the planetary constant of the body in the centrum
        
        r_vec =pos-earth.position[0]
        d=np.linalg.norm(r_vec) #calculates the distance between the bodies
        
        H=np.linalg.norm(np.cross(r_vec,vel)) #calculates the angular momentum
        E=0.5*np.dot(vel,vel)-mu/d #calculates the energy
        self.a=-mu/(2*E)   #calculates the semi major axis
        P=(H**2)/mu       #calculates the ellipse parameter
        ex=sqrt(1-P/self.a) #calculates the eccentricity
        self.b=self.a*sqrt(1-ex**2) #calculates the semi minor axis
        theta=acos((P-d)/(d*ex))    #calculates the true anomaly
        alpha=2*atan(tan(theta/2)*sqrt((1+ex)/(1-ex))) #eccentric anomaly
        try:
            self.angle=atan(r_vec[0]/r_vec[1])-alpha
        except: 
            self.angle=pi/4-alpha
        rp=self.a*(1-ex)
        self.center=earth.position[0]-(self.a-rp)*np.array([cos(self.angle),sin(self.angle)])

    def visualise(self):
        t=np.linspace(0,2*pi,50)
        Ell0=np.array([self.a*np.cos(t),self.b*np.sin(t)])
        Rot=np.array([[cos(self.angle) , -sin(self.angle)],[sin(self.angle) , cos(self.angle)]])
        Ell = np.zeros((2,Ell0.shape[1]))
        Ell = Rot@Ell0
        ellipse, =ax.plot(self.center[0]+Ell[0,:], self.center[1]+Ell[1,:])
        return ellipse
        