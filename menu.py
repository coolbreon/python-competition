import tkinter as tk
import os
root=tk.Tk()
#DEFAULT VALUES
running = False
preset='SolarSystem'

#CREATE MAIN MENU
def create_menu():
    global running
    global preset
    message = tk.Label(root,text="Welcome to OSNI\n(Orbit Simulation with Numerical Integration)")
    message.pack()
    root.title("OSNI Menu")
    root.geometry('600x400')
    
    #Buttons
    tk.Button(root, text='Start Simulation', command=start).pack()
    tk.Button(root,text='Presets',command=presets).pack()
    tk.Button(root,text='Custom Orbit').pack()
    tk.Button(root,text='User Manual',command=help).pack()
    tk.Button(root,text='Exit',command=exit).pack()
    
    root.mainloop()
    return running, preset

#START BUTTON
def start():
    global running
    running = True
    root.destroy()

#USER MANUAL BUTTON
def help():
    root.withdraw() #Hide main menu
    hpage=tk.Tk()
    hpage.title("OSNI Help")
    hpage.geometry('600x800')

    text_box = tk.Text(hpage, wrap='word')  #Enables word-wrapping
    text_box.insert(tk.END, 
        "This is OSNI, a Python program created to simulate orbits using matplotlib and simple two-dimensional numerical integration.\n\n"
        "It is very important to know how a satellite or rocket will behave before actually sending them to space, and this program can help visualize that.\n"
        "Using the 'Presets' button, the user can access several presets of planets and satellites orbiting each other. After selecting a preset, the simulation begins automatically. Presets with many bodies may not run well on less powerful computers.\n"
        #Writing own presets Y/N?
        "The user may also make their own simulation by either writing their own .json file in the presets folder, taking a look at how all the other presets are written, or using the 'Custom Orbit' button.\n"
        "When creating a custom preset, it is recommended to use reasonable values, else the simulation may provide strange results. Please refer to the presets to find ideal orders of magnitude (based off Earth).\n"
        "Once the simulation is running, the following keybinds may be used:\n"
        "- SPACE - Pause\n"
        "- SHIFT - Increase mass of body to be created\n"
        "- CTRL - Decrease mass of body to be created\n"
        "- W - Increase dt of the numerical integration\n"
        "- S - Decrease dt of the numerical integration\n"
        "\tOnce paused:\n"
        "\t- Hover over planet - Highlights trajectory of one body\n"
        "\t- Middle Mouse Click - Creates a new body of previously given mass\n"
        "\t- Left Click - Drag body"
        "\t- Right Click - Select body\n"
        "\t\tOnce selected:\n"
        "\t\t- Left Click - Make velocity vector point to click location\n"
        "\t\t- Arrow Buttons - Move velocity vector in x-y coordinates\n"
        "\t- press V to hide/show velocity vectors\n"
        "\t- press E to export the current layout as a preset\n"
        )
    text_box.config(state='disabled')
    text_box.pack(expand=True, fill='both') #Make text fill the window
    tk.Button(hpage, text="Back to Menu", command=lambda: (hpage.destroy(), root.deiconify())).pack(pady=10)
    hpage.update() #unhide main menu

#PRESETS
def presets():
    global preset
    root.withdraw() #Hide main menu
    presets=tk.Tk()
    presets.title("OSNI Presets")
    presets.geometry('600x800') 

    for prest in os.listdir('presets'):
        prest=prest[0:-5]
        tk.Button(presets, text=prest, command=lambda p=prest: (set_preset(p), set_running(), presets.destroy(), root.destroy())).pack()
    
    tk.Button(presets, text="Back to Menu", command=lambda: (presets.destroy(), root.deiconify())).pack(pady=10)
    presets.update()

#EXIT
def exit():
    global running
    running = False #Exits without starting sim
    root.destroy()

#PRESET CHANGE FN
def set_preset(string):
    global preset
    preset=string

def set_running():
    global running
    running=True