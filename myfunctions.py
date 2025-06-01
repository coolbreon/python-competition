from math import*
import numpy as np
from numpy.typing import NDArray
import matplotlib.pyplot as plt
import json
from Satelliteobject import Satellite

def acceleration(sat1:Satellite, sat2:Satellite, G:float, dt:float):
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


def importjson(filename:str,datapoints:int):
    '''
    Imports a preset json file named 'filename' and returns the list of satellite objects.
    A preset file is a list consisting of dictionaries like "{name:'Earth', mass:5.972e24,...}".
    '''

    #Open the preset file and load it as a list of dictionaries.
    with open(f'presets/{filename}.json', 'r') as fin:
        importlst=json.load(fin)

    #Convert the list of dictionaries to a list of Satellite objects
    planets=[]
    for p in importlst:
        planets.append(
            Satellite(name=p['name'], 
                mass=float(p['mass']),
                pos=np.array(p['position']),
                vel=np.array(p['velocity'] ),
                datapoints=datapoints))
    #return the converted list
    return(planets)

def new_frame(planet:list, maxposx:NDArray, maxposy:NDArray): 
    '''
    Finds new maxima and minima to which the coordinate frame should be adjusted.
    If a planet would be outside the current maxpos in any direction the corresponding maxpos is altered
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

def get_system_energy(planets:list,G:float):
    '''
    Calculates the total energy of the system 
    (the sum of kinetic and gravitational potential energy)
    This allows us to approximate the error of the simulation.
    '''

    e_kinetic=0.0
    e_potential=0.0
    
    for i,p in enumerate(planets):

        #calculates the kinetic energy of a planet from its velocity and mass
        e_kinetic+=0.5*p.mass*(np.linalg.norm(p.velocity))**2

        #calculates the potential energy for every two planet
        for j,q in enumerate(planets[(i+1):]):
            e_potential-=G*p.mass*q.mass/np.linalg.norm(p.position-q.position)
    return e_kinetic+e_potential

def convert_time(t:int):
    '''
    Converts the time ellapsed to days, hours, minutes and seconds.ű
    Returns the result as a string to be able to pringt it nex to the simmulation.
    '''
    s=t%60
    t=t//60
    m=t%60
    t=t//60
    h=t%24
    t=t//24
    d=t

    #Returns the time as a string
    return(f'{d} days,\n{h} hours,\n{m} minutes and\n{s} seconds')

def exporting(planets:list,name:str):
    '''
    Exports the list of Satellite objects to a json file.
    First it converst the planets to dictionarries and 
    '''
    out_lst = json.dumps([p.__dict__() for p in planets])
    with open(f"presets/{name}.json", "w") as fout:
        fout.write(out_lst)
    
    #Confirms the exportation
    print(f'Exported as {name}.json')

def export_naming():
    '''
    Generate a name for a new exported preset.
    The new name will be PresetX, where X is the smallest integer for which
    PresetX does not exist already.
    '''
    num=0
    while True:
        #tries to open a file named PresetX
        try:
            f = open(f"presets/Preset{num}.json", "r")
        #if it cannot be opened (as it does not exists) the current naming is the one
        except:
            break
        num+=1
    #returns the naming as a string
    return (f'Preset{num}')
