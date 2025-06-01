from math import*
import numpy as np
from numpy.typing import NDArray
import matplotlib.pyplot as plt
import json
from Satelliteobject import Satellite

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
        v1=sat1.velocity+a1*dt
        v2=sat2.velocity+a2*dt
        return v1,v2


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
    return maxposx,maxposy

def get_system_energy(planets,G,):
    e_kinetic=0.0
    e_potential=0.0
    for i,p in enumerate(planets):
        e_kinetic+=0.5*p.mass*(np.linalg.norm(p.velocity))**2
        for j,q in enumerate(planets[(i+1):]):
            e_potential-=G*p.mass*q.mass/np.linalg.norm(p.position-q.position)
    return e_kinetic+e_potential

def convert_time(t):
    s=t%60
    t=t//60
    m=t%60
    t=t//60
    h=t%24
    t=t//24
    d=t%365
    t=t//365
    y=t
    return(f'{y} years,\n{d} days,\n{h} hours,\n{m} minutes and\n{s} seconds')

def exporting(planets,name):
    out_lst = json.dumps([p.__dict__() for p in planets], indent=4)
    with open(f"presets/{name}.json", "w") as fout:
        fout.write(out_lst)

def export_naming():
    num=-1
    found=False
    
    while not found:
        num+=1
        try:
            f = open(f"presets/Preset{num}.json", "r")
        except:
            found=True
    return num
