from math import*
import numpy as np
import matplotlib.pyplot as plt
from math import *


class Satellite:
    def __init__(self,data):#data is the number of stored datapoints
        self.mass = 1000
        self.position = np.zeros((data,2))
        self.velocity = np.zeros((data,2))

    def init(self,mass,pos,vel):
        self.mass=mass
        self.velocity[0]=vel
        for i in range(len(self.velocity)):
            self.position[i]=pos
    #Take values from user:
    def take_input(self):
        self.mass=input("Please give the object a mass [kg]: ")
        self.position[0][0]=input("Please give the initial x position: ")
        self.position[0][1]=input("Please give the initial y position: ")
        self.velocity[0][0]=input("Please give the initial x velocity: ")
        self.velocity[0][1]=input("Please give the initial y velocity: ")
    
    #Print out own values:
    def print(self):
        print(f"Mass: {self.mass}\nInitial Position: {self.position[0]}\nInitial Velocity: {self.velocity[0]}")
    
    #Calculate acceleration to another body
    def acceleration(self,pos,mass,G,t):    #t is the index of the current position and velocity
        t=t-1
        dist = sqrt((pos[0]-self.position[t,0])**2+(pos[1]-self.position[t,1])**2)  #Calculate distance (Pythagoran theorem)
        unit_vector=np.array([pos[0]-self.position[t,0],pos[1]-self.position[t,1]])/dist   #Calculate the unit vector pointing from self planet to other planet
        a=unit_vector*((G*mass)/(dist**2))    #Calculate the gravitational force
        #Newton's second law
        return a
    
    #modifies position and velocity 
    def iterate(self,a,dt,t):
        self.position[t]=self.position[t-1]+self.velocity[t-1]*dt
        self.velocity[t]=self.velocity[t-1]+a*dt

class Trajectory:
    def __init__(self):#data is the number of stored datapoints
        self.center = np.array([0,0]) 
        self.a = 1000 #[m]
        self.b = 1000 #[m]
        self.angle = 0 #[rad]
    def calculate(self, pos, vel, earth,G):
        mu=earth.mass*G #calculates the planetary constant of the body in the centrum
        d=dist(pos,earth.position[0]) #calculates the distance between the bodies
        H=(pos-earth.pos[0])[0]*vel[1]-(pos-earth.pos[0])[1]*vel[0] #calculates the angular momentum
        E=np.dot(vel,vel)-mu/d #calculates the energy
        self.a=mu/2/E   #calculates the semi major axis
        P=H**2/mu       #calculates the ellipse parameter
        e=sqrt(1-P/self.a) #calculates the eccentricity
        self.b=self.a*sqrt(1-e^2) #calculates the semi minor axis
        theta=acos(P-1/e)    #calculates the true anomaly
        alpha=atan(tan(theta/2)*sqrt((1+e)/(1-e))) #eccentric anomaly
        try:
            self.angle=atan(pos[1]/pos[0])-alpha
        except: self.angle=pi/2-alpha

    def visualise(self):
        t=np.linespace(0,2*pi,50)
        Ell0=np.array([self.a*np.cos(t)],[self.b*np.sin(t)])
        Rot=np.array([[cos(self.angle) , -sin(self.angle)],[sin(self.angle) , cos(self.angle)]])
        Ell = np.zeros((2,Ell0.shape[1]))
        for i in range(Ell0.shape[1]):
            Ell[:,i] = np.dot(Rot,Ell[:,i])
        plt.plot(self.center[0]+Ell[0,:] , self.center[1]+Ell[1,:])