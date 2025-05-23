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
datapoints=6000
dt=3
storefrequency=50
showfrequency=100
imp=True
export=False

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
    with open('presets/Fourbody3.json', 'r') as fin:
        importlst=json.load(fin)
    planets=importjson(importlst,datapoints)
imp=False




if export==True:
    out_lst = json.dumps([p.__dict__() for p in planets], indent=4)
    with open("presets/Sat2.json", "w") as fout:
        fout.write(out_lst)


lineheads = [ax.plot([], [], 'o', markersize=6)[0] for _ in planets]
lines = [ax.plot([], [], '-')[0] for _ in planets]

for i, marker in enumerate(lineheads):
    marker.set_label(planets[i].name)

#initialize_energy(planets,G)


#initialzize variables
modes=Modes(plt.gcf().canvas)

storeline=0
f=0
maxposx= [0,0]
maxposy= [0,0]
arrows=[]

#connects the click event to the canvas and gives it an ID
closeid = plt.gcf().canvas.mpl_connect('close_event',modes.closeing)
keyid = plt.gcf().canvas.mpl_connect('key_press_event',modes.key)


#print(sum(i.initial_energy for i in planets))
'''
    actual_energy(planets,G)
    if f%5000==0:
        print(sum(i.actual_energy for i in planets))
'''

while modes.running:
    if not modes.paused:
        for l, p1 in enumerate(planets):
            for p2 in planets[l+1:]:
                acceleration(p1,p2,G,dt)
            [maxposx,maxposy] = new_frame(p1,maxposx,maxposy)
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
                plt.pause(0.0001)
                

        f+=1
    else:     
        if modes.arrows: 
            for p in planets:
                arrows.append(plt.arrow(p.position[0],p.position[1],
                                        p.velocity[0]*5e3,p.velocity[1]*5e3, 
                                        width= 0.2, head_width=1000000))

        #makes the planet hovered over pop
        for a,p in enumerate(planets):
            lines[a].set_alpha(1)
            
            try:
                isactive=closeto(modes.hovered,p.position,maxposx,maxposy)
            except:
                isactive=False
            if isactive:
                for k,traj in enumerate(lines):
                    if k!=a:
                        traj.set_alpha(0.2) 
                break
        plt.pause(0.1)
        for traj in lines:
            traj.set_alpha(1)
        for a in arrows:
            a.remove()
        arrows.clear()
plt.ioff()
plt.show()
print('exiting...')