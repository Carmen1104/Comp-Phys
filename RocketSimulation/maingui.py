import numpy as np
import matplotlib.pyplot as plt
from func import integrateGraph
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Create a GUI window
window = Tk()
window.title("Rocket Simulation")
window.geometry("800x600")

# Create a figure for the plot
fig = plt.figure(figsize=(6, 4))

# Create a canvas to display the figure
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

# Create a function to update the plot
def update_plot():
    # Get the values from the entries
    totalMass = float(totalMass_entry.get())
    dryMass = float(dryMass_entry.get())
    burnTime = float(burnTime_entry.get())
    totalImpulse = float(totalImpulse_entry.get())
    propellantMass = float(propellantMass_entry.get())

    # Calculate the average thrust, mass flow rate, thrust, mass, acceleration, velocity and displacement
    averageThrust = totalImpulse/burnTime
    massFlowRate = propellantMass/burnTime

    time = np.linspace(0, 10, 100, False)

    index = np.argmax(time==burnTime) + 1
    thrust = np.append(np.repeat(averageThrust, index), np.repeat(0, len(time) - index))
    mass = np.append(np.repeat(totalMass, index) - time[0:index] * massFlowRate, np.repeat(dryMass, len(time) - index))
    acceleration = thrust/mass - 9.81
    velocity = integrateGraph(time, acceleration)
    displacement = integrateGraph(time, velocity)

    # Clear the previous plot
    fig.clear()

    # Plot the new data
    plt.plot(time, displacement)
    plt.plot(time, velocity)
    plt.legend(["Displacement", "Velocity"])
    plt.xlabel("Time")

    # Draw the canvas
    canvas.draw()

# Create labels and entries for the parameters
totalMass_label = Label(window, text="Total Mass (kg):")
totalMass_label.pack(side=LEFT)
totalMass_entry = Entry(window)
totalMass_entry.insert(0, "1")
totalMass_entry.pack(side=LEFT)

dryMass_label = Label(window, text="Dry Mass (kg):")
dryMass_label.pack(side=LEFT)
dryMass_entry = Entry(window)
dryMass_entry.insert(0, "0.906")
dryMass_entry.pack(side=LEFT)

burnTime_label = Label(window, text="Burn Time (s):")
burnTime_label.pack(side=LEFT)
burnTime_entry = Entry(window)
burnTime_entry.insert(0, "3.4")
burnTime_entry.pack(side=LEFT)

totalImpulse_label = Label(window, text="Total Impulse (N*s):")
totalImpulse_label.pack(side=LEFT)
totalImpulse_entry = Entry(window)
totalImpulse_entry.insert(0, "49.6")
totalImpulse_entry.pack(side=LEFT)

propellantMass_label = Label(window, text="Propellant Mass (kg):")
propellantMass_label.pack(side=LEFT)
propellantMass_entry = Entry(window)
propellantMass_entry.insert(0, "0.064")
propellantMass_entry.pack(side=LEFT)

# Create a button to update the plot
update_button = Button(window, text="Update Plot", command=update_plot)
update_button.pack(side=LEFT)

# Run the main loop of the window
window.mainloop()
