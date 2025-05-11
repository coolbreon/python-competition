from myfunctions import *


#Contants
G=6.67430*10**(-11) # [m3/kgs2]
datapoints=100
planets = [Satellite(datapoints),Satellite(datapoints)]
planets[0].mass=5.97*10**24
planets[0].position[0,0]=0
planets[0].position[0,1]=0
planets[0].velocity[0,0]=0
planets[0].velocity[0,1]=0

planets[1].mass=100
planets[1].position[0][1]=0
planets[1].position[0][0]=42164000
planets[1].velocity[0][0]=0
planets[1].velocity[0][1]=7611


i=1
while True:
    for k in range(len(planets)):
        a=np.array([0,0])
        for j in (*range(0,k),*range(k+1,len(planets))):
            a= a+planets[k].acceleration(planets[j].position[i-1],planets[j].mass,G,i)
        plt.plot(planets[k].position[:,0],planets[k].position[:,1],)
        planets[k].iterate(a,100,i)

    i+=1
    if i==datapoints:
        i=0
    plt.draw()
    plt.pause(0.00001)
plt.ion
plt.show()

#BLITTING