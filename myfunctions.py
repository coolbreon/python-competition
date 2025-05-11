from math import*
import numpy as np
import matplotlib.pyplot as plt
from math import *


class Satellite:
    def __init__(self,data):#data is the number of stored datapoints
        self.mass = 1000
        self.position = np.zeros((data,2))
        self.velocity = np.zeros((data,2))
    
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
        unit_vector=np.array([pos[0]-self.position[t][0],pos[1]-self.position[t][0]])/dist   #Calculate the unit vector pointing from self planet to other planet
        F=unit_vector*((G*self.mass*mass)/(dist**2))    #Calculate the gravitational force
        a=F/self.mass    #Newton's second law
        return a
    
    #modifies position and velocity 
    def iterate(self,a,dt,t):
        self.position[t]=self.position[t-1]+self.velocity[t-1]*dt
        self.velocity[t]=self.velocity[t-1]+a*dt
                