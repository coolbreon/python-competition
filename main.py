from myfunctions import *
import json

def key(event):
    if event.key==' ':
        modes.spaceclick()


plt.ion()

ax.set_aspect('equal', adjustable='box')
ax.set_title("Simulation (Testing Movement)")
ax.set_xlim(-10e7, 10e7)
ax.set_ylim(-10e7, 10e7)


#Contants
G=6.67430e-11 # [m3/kgs2]
datapoints=500
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
    with open('presets/Fourbody2.json', 'r') as fin:
        importlst=json.load(fin)
    planets=importjson(importlst,datapoints)
imp=False


#Initialize lines and point masses to be plotted
lineheads = [ax.plot([], [], 'o', markersize=6)[0] for _ in planets]
lines = [ax.plot([], [], '-')[0] for _ in planets]

#Initialize the energy and time text to be plotted
energy_text = ax.text(1.05,0.3, '', fontsize=12, transform=ax.transAxes)
time_text =ax.text(1.05,0.5, '', fontsize=12, transform=ax.transAxes)

for i, marker in enumerate(lineheads):
    marker.set_label(planets[i].name)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)

#initialzize variables
modes=Modes(plt.gcf().canvas)

storeline=0
f=0
maxposx= [0,0]
maxposy= [0,0]
arrows=[]

for p in planets:
            p.connect()

#Energy at t=0
e_0 = get_system_energy(planets,G)

while modes.running:
    if not modes.paused:
        for l, p1 in enumerate(planets):
            for p2 in planets[l+1:]:
                acceleration(p1,p2,G,dt)
            
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
               
                maxposx,maxposy = new_frame(p,maxposx,maxposy)
                #p.maxpos=max(maxposx[1],maxposy[1])
                ax.set_xlim(maxposx[0]*1.2, maxposx[1]*1.2)
                ax.set_ylim(maxposy[0]*1.2, maxposy[1]*1.2)
                energy_text.set_text(f"Energy change(% of t=0):\n{-100*get_system_energy(planets,G)/e_0+100:0.3f}%")
                time_text.set_text("Time ellapsed:\n"+ convert_time(f*dt))
                plt.pause(0.0001)

        f+=1
    else:
        if modes.exporting:
            exporting(planets,f'Preset')
            modes.exporting=False

        if modes.arrows: 
            for p in planets:
                arrows.append(plt.arrow(p.position[0],p.position[1],
                                        p.velocity[0]*5e3,p.velocity[1]*5e3, 
                                        width= 0.2, head_width=1000000))
                
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