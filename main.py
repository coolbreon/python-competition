from myfunctions import *
plt.ion()
ax.set_xlim(-10e7, 10e7)
ax.set_ylim(-10e7, 10e7)

#Contants
G=6.67430e-11 # [m3/kgs2]
datapoints=300
dt=10
cycles=10000
storefrequency=40
showfrequency=40


planets = [
    Satellite(name="Earth", mass=5.972e24,
              pos=np.array([0.0, 0.0]),
              vel=np.array([0.0, 0.0]),
              datapoints=datapoints),

    Satellite(name="Geo", mass=10e2,
              pos=np.array([0.0, 4.27e7]),
              vel=np.array([3.0e3, 0.0]),
              datapoints=datapoints),

]


lineheads = [ax.plot([], [], 'o', markersize=6)[0] for _ in planets]
lines = [ax.plot([], [], '-')[0] for _ in planets]

for i, marker in enumerate(lineheads):
    marker.set_label(planets[i].name)


storeline=0
for f in range(cycles):
    for l, p1 in enumerate(planets):
        for p2 in planets[l+1:]:
            acceleration(p1,p2,G,dt)
    for p in planets:
        p.move(dt)
     
    if f%storefrequency==0:
        for p in planets:
            p.store(storeline)

        storeline+=1
        if storeline==datapoints:
            storeline=0
    
    if f%showfrequency==0:
        for i,p in enumerate(planets):
            data = p.getHistory(storeline)
            lineheads[i].set_data([p.position[0]], [p.position[1]])
            lines[i].set_data(data[:, 0], data[:, 1])
            plt.pause(1.0e-11)
        print(f"Step {f}/{cycles} completed.\n")   


print("Simulation finished.")
plt.ioff()
plt.show()