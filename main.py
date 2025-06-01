from myfunctions import *
import json
from eventhandler import*
from Satelliteobject import Satellite

plt.ion()

fig, ax = plt.subplots()
ax.set_aspect('equal', adjustable='box')
ax.set_title("Simulation (Testing Movement)")
ax.set_xlim(-10e7, 10e7)
ax.set_ylim(-10e7, 10e7)


#Contants
G=6.67430e-11 # [m3/kgs2]
datapoints=5000
dt=3
storefrequency=30
showfrequency=100
imp=True

planets = [
    Satellite(name="Earth", mass=5.972e+24,
              pos=np.array([0.0, 0.0]),
              vel=np.array([0.0, 0.0]),
              datapoints=datapoints),

    Satellite(name="Sat", mass=4.0e3,
              pos=np.array([0.0, 4.27e7]),
              vel=np.array([1.0e3, 0.0]),
              datapoints=datapoints),    
]

if imp==True:
    with open('presets/Threebody2.json', 'r') as fin:
        importlst=json.load(fin)
    planets=importjson(importlst,datapoints)
imp=False


#Initialize lines and point masses to be plotted
lineheads = [ax.plot([], [], 'o', markersize=6)[0] for _ in planets]
lines = [ax.plot([], [], '-')[0] for _ in planets]

#Initialize the energy and time text to be plotted
energy_text = ax.text(1.05,0.3, '', fontsize=12, transform=ax.transAxes)
time_text =ax.text(1.05,0.5, '', fontsize=12, transform=ax.transAxes)
mass_text =ax.text(1.05,0.9, '', fontsize=12, transform=ax.transAxes)

for i, marker in enumerate(lineheads):
    marker.set_label(planets[i].name)
plt.legend(bbox_to_anchor=(-0.3, 1), loc='upper right', borderaxespad=0.)

#initialzize variables
modes=Modes(plt.gcf().canvas)

storeline=0
f=0
maxposx= [-1e7,1e7]
maxposy= [-1e7,1e7]
arrows=[]


#Energy at t=0
e_0 = get_system_energy(planets,G)

while modes.running:
    if not modes.paused:
        for l, p1 in enumerate(planets):
            for p2 in planets[l+1:]:
                v1,v2=acceleration(p1,p2,G,dt)
                p1.velocity=v1
                p2.velocity=v2
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
                p.maxpos=max(maxposx[1],maxposy[1])
                maxposx,maxposy = new_frame(p,maxposx,maxposy)
                ax.set_xlim(maxposx[0]*1.2, maxposx[1]*1.2)
                ax.set_ylim(maxposy[0]*1.2, maxposy[1]*1.2)
                energy_text.set_text(f"Energy change(% of t=0):\n{-100*get_system_energy(planets,G)/e_0+100:0.3f}%")
                time_text.set_text("Time ellapsed:\n"+ convert_time(f*dt))
                mass_text.set_text(f"Created mass:\n{modes.mass_to_create:0.0f}[kg]")
                plt.pause(0.0001)

        f+=1
    else:
        if modes.exporting:
            exporting(planets,f'Preset{export_naming()}')
            modes.exporting=False

        if modes.connecting:
            modes.connect()
            for p in planets:
                p.connect()
            modes.connecting=False
        
        if modes.disconnecting:
            modes.disconnect()
            for p in planets:
                p.disconnect()
                p.selected=False
            modes.disconnecting=False

        if modes.creating:
            planets.append(
                Satellite(name=f"Asteroid{len(planets)+1}", mass=modes.mass_to_create,
              pos=modes.create,
              vel=np.array([0.0, 0.0]),
              datapoints=datapoints)
            )
            planets[-1].connect()
            lineheads.append(ax.plot([], [], 'o', markersize=6)[0])
            lines.append(ax.plot([], [], '-')[0])
            modes.creating=False


        if modes.arrows: 
            for p in planets:
                arrows.append(plt.arrow(p.position[0],p.position[1],
                                        p.velocity[0]*p.maxpos/5e3,p.velocity[1]*p.maxpos/5e3, 
                                        width= 0.2, head_width=p.maxpos/5e1))
                
        for i,p in enumerate(planets):
            lineheads[i].set_data([p.position[0]], [p.position[1]])
            if p.selected:
                lineheads[i].set_marker('D')
                lineheads[i].set_markersize(15)
            if p.hovered:
                for n,pl in enumerate(planets):
                    
                    if n!=i:
                        lines[n].set_alpha(0.2)
                        if modes.arrows:
                            arrows[n].set_alpha(0.2)

        #makes the planet hovered over pop
        plt.pause(0.1)
        
        for a in arrows:
            a.remove()
        arrows.clear()

        for n,pl in enumerate(planets):    
            lines[n].set_alpha(1)
            lineheads[n].set_marker('o')
            lineheads[n].set_markersize(6)
plt.ioff()
plt.show()
print('exiting...')