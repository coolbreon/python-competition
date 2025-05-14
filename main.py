from myfunctions import *
import json


plt.ion()
ax.set_aspect('equal', adjustable='box')
ax.set_title("Simulation (Testing Movement)")
ax.set_xlim(-10e7, 10e7)
ax.set_ylim(-10e7, 10e7)

#Contants
G=6.67430e-11 # [m3/kgs2]
datapoints=1000
dt=10
storefrequency=40
showfrequency=100
imp=True
export=False

planets = [
   Satellite(name="Asteroid1", mass=4.0e24,
              pos=np.array([0.0, 4.27e7]),
              vel=np.array([-3.0e3, 0.0]),
              datapoints=datapoints),

    Satellite(name="Asteroid2", mass=4.0e24,
              pos=np.array([0.0, 0.0]),
              vel=np.array([3.5e3, 0.0]),
              datapoints=datapoints),
    Satellite(name="Asteroid2", mass=4.0e24,
              pos=np.array([0.0, -4.27e7]),
              vel=np.array([-5.0e2, 0.0]),
              datapoints=datapoints),
    
]

if imp==True:
    with open('Threebody1.json', 'r') as fin:
        importlst=json.load(fin)
    planets=importjson(importlst,datapoints)
imp=False




if export==True:
    out_lst = json.dumps([p.__dict__() for p in planets], indent=4)
    with open("Threebody3.json", "w") as fout:
        fout.write(out_lst)


lineheads = [ax.plot([], [], 'o', markersize=6)[0] for _ in planets]
lines = [ax.plot([], [], '-')[0] for _ in planets]

for i, marker in enumerate(lineheads):
    marker.set_label(planets[i].name)

#initialize_energy(planets,G)

storeline=0
f=0
maxposx= [0,0]
maxposy= [0,0]
#print(sum(i.initial_energy for i in planets))
'''
    actual_energy(planets,G)
    if f%5000==0:
        print(sum(i.actual_energy for i in planets))
'''
while True:
    for l, p1 in enumerate(planets):
        for p2 in planets[l+1:]:
            acceleration(p1,p2,G,dt)
        [maxposx,maxposy]=new_frame(p1,maxposx,maxposy)
    for p in planets:
        p.move(dt)

     
    if f%storefrequency==0:
        storeline+=1
        if storeline==datapoints:
            storeline=0
        for p in planets:
            p.store(storeline)


    if f%showfrequency==0:
        for i,p in enumerate(planets):
            data = p.getHistory(storeline)
            lineheads[i].set_data([p.position[0]], [p.position[1]])
            lines[i].set_data(data[:, 0], data[:, 1])
            ax.set_xlim(maxposx[0]*1.2, maxposx[1]*1.2)
            ax.set_ylim(maxposy[0]*1.2, maxposy[1]*1.2)
            plt.pause(1.0e-11)
    f+=1 


plt.ioff()
plt.show()