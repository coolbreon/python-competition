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

planets[0].init(100,[42700000,0],[0,2000])
planets[1].init(5.67*10**24,[0,0],[0,0])

geo1=Trajectory()
geo1.calculate([42700000,0],[0,2000],planets[1],G)
print(geo1)
geo1.visualise()

lines = []
for p in planets:
    line, = ax.plot([], [], '-')
    lines.append(line)

lineheads = []
for p in planets:
    line, = ax.plot([], [], 'o')
    lineheads.append(line)

running=True
i=1
print(planets[1].acceleration(planets[0].position[0],planets[0].mass,G,1))
while running:
    for k in range(len(planets)):
        a=np.array([0,0])
        for j in (*range(0,k),*range(k+1,len(planets))):
            a= a+planets[k].acceleration(planets[j].position[i-1],planets[j].mass,G,i)
        planets[k].iterate(a,dt,i)
        x = np.concatenate((planets[k].position[i+1:, 0], planets[k].position[:i+1, 0]))
        y = np.concatenate((planets[k].position[i+1:, 1], planets[k].position[:i+1, 1]))
        lines[k].set_data(x, y)
        lineheads[k].set_data([x[-1]], [y[-1]])
        

    i+=1
    if i==datapoints:
        i=0
    plt.pause(0.0000001)
    plt.draw()




#BLITTING