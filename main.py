from myfunctions import *
from eventhandler import Modes
from Satelliteobject import Satellite
from menu import create_menu

#tkinter menu and the preset from it
running, preset = create_menu()
print(f'Starting {preset}')
if running:
    plt.ion()
    
    #Setup plot
    fig, ax = plt.subplots()
    ax.set_aspect('equal', adjustable='box')
    ax.set_title("Simulation (Testing Movement)")

    #Constants
    
    datapoints=5000
    store_interval=10
    show_interval=100
    
    #imports the preset given by preset string
    planets=importjson(preset,datapoints)

    #Initialize lines and point masses to be plotted
    lines = [ax.plot([], [], '-')[0] for _ in planets]
    lineheads = [ax.plot([], [], 'o', markersize=6)[0] for _ in planets]

    #Set up the legend
    for i, marker in enumerate(lineheads):
        marker.set_label(planets[i].name)
    plt.legend(bbox_to_anchor=(-0.3, 1), loc='upper right', borderaxespad=0.)

    #Initialize the energy and time text to be plotted
    textbox = ax.text(1.05,0.2, '', fontsize=12, transform=ax.transAxes)

    modes=Modes(plt.gcf().canvas) #initialize event handler
    
    #Initialize constants/variables
    G=6.67430e-11           # [m3/kgs2]
    T=0                     #[s] time ellapsed
    storeline=0             #number of line to store data in
    f=0                     #number of cycles ellapsed
    maxposx= [-1e7,1e7]     #maximum values for the axis limits
    maxposy= [-1e7,1e7] 
    arrows=[]               #list of shown velocity arrows


    #Energy at t=0
    e_0 = get_system_energy(planets,G)
    
    modes.running=running
    #Simulation:
    while modes.running:
        #If the simulation is running
        if not modes.paused:
            #increase the ellapsed time by dt
            T+=modes.dt
            
            #Itarates the planet pares and calculates their new velocities
            for l, p1 in enumerate(planets):
                for p2 in planets[l+1:]:
                    v1,v2=acceleration(p1,p2,G,modes.dt)
                    p1.velocity=v1
                    p2.velocity=v2
            
            #move planets with the given velocity
            for p in planets:
                p.move(modes.dt)
            
            #if f is divisible by the store_interval the position of the planets is stored
            if f%store_interval==0:
                #handles the line in which the new data is stored
                storeline+=1
                if storeline==datapoints:
                    storeline=0
                #stores the data of planets
                for p in planets:
                    p.store(storeline)
            
            #if f is divisible by the show_interval visualization happens
            if f%show_interval==0:
                for i,p in enumerate(planets):
                    #arranges the data to visualize
                    data = p.getHistory(storeline)
                    #updates the data of the lines
                    lineheads[i].set_data([p.position[0]], [p.position[1]])
                    lines[i].set_data(data[:, 0], data[:, 1])
                    #updates the axes
                    p.maxpos=max(maxposx[1],maxposy[1])
                    maxposx,maxposy = new_frame(p,maxposx,maxposy)
                    ax.set_xlim(maxposx[0]*1.2, maxposx[1]*1.2)
                    ax.set_ylim(maxposy[0]*1.2, maxposy[1]*1.2)
                    #updates the text next to the figure
                    textbox.set_text(f'Energy change(% of t=0):\n'+
                                     f'{-100*get_system_energy(planets,G)/e_0+100:0.3f}%\n\n' +
                                     f'Time ellapsed:\n {convert_time(T)}\n\n'+
                                     f'dt={modes.dt}[s]\n\n'+
                                     f'Created mass:\n1e{log10(modes.mass_to_create):0.0f}[kg]')
                    #pause to save processor capacity
                    plt.pause(0.0001)

            f+=1
        
        #if paused:
        else:
            #if we need to export in this cycle export
            if modes.exporting:
                exporting(planets,export_naming())
                modes.exporting=False
            
            #if we need to connect here than connect
            if modes.connecting:
                modes.connect()
                for p in planets:
                    p.connect()
                modes.connecting=False
            
            #if we need to disconnect here than disconnect (to speed up the calculations)
            if modes.disconnecting:
                modes.disconnect()
                for p in planets:
                    p.disconnect()
                    p.selected=False
                modes.disconnecting=False

            #New satellite creation event and connects it.
            if modes.creating: 
                planets.append(
                    Satellite(name=f"Asteroid{len(planets)+1}", 
                              mass=modes.mass_to_create,
                              pos=modes.create,
                              vel=np.array([0.0, 0.0]),
                              datapoints=datapoints)
                )
                planets[-1].connect()
                #creates the new visualization
                lineheads.append(ax.plot([], [], 'o', markersize=6)[0])
                lines.append(ax.plot([], [], '-')[0])
                modes.creating=False
                #resets energy calculations (as new mass was created)
                e_0=get_system_energy(planets,G)

            #Displaying velocity vectors
            if modes.arrows: 
                for p in planets:
                    arrows.append(plt.arrow(p.position[0],p.position[1],
                                            p.velocity[0]*p.maxpos/5e3,p.velocity[1]*p.maxpos/5e3, 
                                            width= 0.2, head_width=p.maxpos/5e1))
                    
            for i,p in enumerate(planets):
                lineheads[i].set_data([p.position[0]], [p.position[1]])
                #Right-click selection
                if p.selected:
                    lineheads[i].set_marker('D')
                    lineheads[i].set_markersize(15)
                #Mouse hover (makes the planet hovered over pop)
                if p.hovered:
                    for n,pl in enumerate(planets):
                        #Set trajectory and velocity vector opacities of all other bodies to 20%
                        if n!=i:
                            lines[n].set_alpha(0.2)
                            if modes.arrows:
                                arrows[n].set_alpha(0.2)
                #If the data of a planet was changed, reset the energy calculations
                if p.changed:
                    e_0=get_system_energy(planets,G)
                    p.changed=False
            plt.pause(0.1) #pause to show modifications
            
            #removes arrows to avoid them staying on during simulation
            for a in arrows:
                a.remove()
            arrows.clear()
            #Resets planet visualizations to avoid them staying transparent during simulation
            for n,pl in enumerate(planets):    
                lines[n].set_alpha(1)
                lineheads[n].set_marker('o')
                lineheads[n].set_markersize(6)

            #Write data next to graph
            textbox.set_text(f'Energy change(% of t=0):\n'+
                                     f'{-100*get_system_energy(planets,G)/e_0+100:0.3f}%\n\n' +
                                     f'Time ellapsed:\n {convert_time(T)}\n\n'+
                                     f'dt={modes.dt}[s]\n\n'
                                    f'Created mass:\n1e{log10(modes.mass_to_create):0.0f}[kg]')
    #End of simulation
    plt.ioff()
    plt.show()
    print('exiting...')