from myfunctions import *
plt.ion()
fig, ax = plt.subplots()
ax.set_xlim(-10e7, 10e7)
ax.set_ylim(-10e7, 10e7)

#Contants
G=6.67430*10**(-11) # [m3/kgs2]
datapoints=6000
dt=30
planets = [Satellite(datapoints),Satellite(datapoints)]

planets[1].init(5.67*10**24,[0,0],[0,0])
planets[0].init(100,[42700000,0],[0,3704])


lines = []
for p in planets:
    line, = ax.plot([], [], '-')
    lines.append(line)

lineheads = []
for p in planets:
    line, = ax.plot([], [], 'o')
    lineheads.append(line)


i=1
print(planets[1].acceleration(planets[0].position[0],planets[0].mass,G,1))
while True:
    for k in range(len(planets)):
        a=np.array([0,0])
        for j in (*range(0,k),*range(k+1,len(planets))):
            a= a+planets[k].acceleration(planets[j].position[i-1],planets[j].mass,G,i)
        planets[k].iterate(a,dt,i)
        lines[k].set_data([planets[k].position[:, 0]], [planets[k].position[:, 1]])
        lineheads[k].set_data([planets[k].position[i, 0]], [planets[k].position[i, 1]])

    i+=1
    if i==datapoints:
        i=0

    plt.pause(0.00000001)
    plt.draw()




#BLITTING