# Import modules
import numpy as np
import matplotlib.pyplot as plt
from func import integrateGraph
from tkinter import *
from tkinter.ttk import *
from tktooltip import ToolTip
import random # Import the random module
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter.ttk import Style # Import the Style class

# Create a GUI window
window = Tk()
window.title("Rocket Simulation")

# Set dark theme colors
background_color = "#333333"
foreground_color = "#FFFFFF"

window.configure(bg=background_color)
window.option_add("*background", background_color)
window.option_add("*foreground", foreground_color)

# Create a figure for the plot
fig = plt.figure(figsize=(8, 6))
fig.patch.set_facecolor(background_color)

# Create a canvas to display the figure
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.draw()
canvas.get_tk_widget().grid(row=0, column=0, columnspan=3, rowspan=5, padx=10, pady=10)

# Create a function to update the plot
def update_plot():
    # Get the values from the entries
    totalMass = float(totalMass_entry.get())
    dryMass = float(dryMass_entry.get())
    burnTime = float(burnTime_entry.get())
    totalImpulse = float(totalImpulse_entry.get())
    propellantMass = float(propellantMass_entry.get())

    # Calculate the average thrust, mass flow rate, thrust, mass, acceleration, velocity, and displacement
    averageThrust = totalImpulse / burnTime
    massFlowRate = propellantMass / burnTime

    time = np.linspace(0, 10, 100, False)

    index = np.argmax(time == burnTime) + 1
    thrust = np.append(np.repeat(averageThrust, index), np.repeat(0, len(time) - index))
    mass = np.append(np.repeat(totalMass, index) - time[0:index] * massFlowRate,
                     np.repeat(dryMass, len(time) - index))
    acceleration = thrust / mass - 9.81
    velocity = integrateGraph(time, acceleration)
    displacement = integrateGraph(time, velocity)

    # Clear the previous plot
    fig.clear()

    # Plot the new data
    plt.plot(time, displacement)
    plt.plot(time, velocity)
    legend = plt.legend(["Displacement (m)", "Velocity (m/s)"], facecolor=background_color, edgecolor=foreground_color)
    for text in legend.get_texts():
        text.set_color(foreground_color)
    plt.xlabel("Time", color=foreground_color)
    plt.tick_params(colors=foreground_color)
    plt.gca().set_facecolor(background_color)

    # Draw the canvas
    canvas.draw()

# Create a function to create a label, an entry and a text box for each parameter
def create_input(label_text, entry_text, tooltip_text, row, column):
    # Create a label with the given text and font
    label = Label(window,
                  text=label_text,
                  font=("Arial", 16)) # Use Arial font with size 16 for the label
    label.grid(row=row,
               column=column+3,
               padx=10,
               pady=5,
               sticky="E")
    # Create an entry with the given text and font
    entry = Entry(window,
                  font=("Arial", 16)) # Use Arial font with size 16 for the entry
    entry.insert(0,
                 entry_text)
    entry.grid(row=row,
               column=column+4,
               padx=10,
               pady=5)
    # Create a text box with the given text and font
    text = Text(window,
                width=40,
                height=2,
                font=("Arial", 16)) # Use Arial font with size 16 for the text box
    text.insert(END,
                tooltip_text)
    text.config(state=DISABLED)
    text.grid(row=row,
              column=column+5,
              padx=10,
              pady=5)
    # Create a tooltip for the text box
    ToolTip(text,
            msg=tooltip_text)
    # Return the entry object for later use
    return entry

# Create labels and entries for the parameters using the create_input function
totalMass_entry = create_input("Total Mass (kg):",
                               "1",
                               "The mass of the rocket at liftoff.",
                               0,
                               0)
dryMass_entry = create_input("Dry Mass (kg):",
                             "0.906",
                             "The mass of the rocket without propellant.",
                             1,
                             0)
burnTime_entry = create_input("Burn Time (s):",
                              "3.4",
                              "The duration of the rocket's thrust.",
                              2,
                              0)
totalImpulse_entry = create_input("Total Impulse (N*s):",
                                  "49.6",
                                  "The total change in momentum of the rocket.",
                                  3,
                                  0)
propellantMass_entry = create_input("Propellant Mass (kg):",
                                    "0.064",
                                    "The mass of the propellant consumed by the rocket.",
                                    4,
                                    0)

# Create a style object
style = Style()

# Configure a custom style for the buttons
style.configure("Large.TButton",
                font=("Arial", 16), # Use Arial font with size 16 for the buttons
                padding=10)

# Create a button to update the plot
update_button = Button(window,
                       text="Update Plot",
                       command=update_plot,
                       style="Large.TButton") # Apply the custom style to the button
update_button.grid(row=5,
                   column=3,
                   columnspan=3,
                   padx=10,
                   pady=5)

# Create a function to generate random inputs
def generate_random_inputs():
    # Generate random values for the parameters
    totalMass = random.uniform(0.1, 10) # in kg
    dryMass = random.uniform(0.10, 10) * totalMass # in kg
    burnTime = random.uniform(2, 20) # in s
    totalImpulse = random.uniform(40, 150) # in N*s
    propellantMass = totalMass - dryMass # in kg

    # Delete the previous values from the entries
    totalMass_entry.delete(0, "end")
    dryMass_entry.delete(0, "end")
    burnTime_entry.delete(0, "end")
    totalImpulse_entry.delete(0, "end")
    propellantMass_entry.delete(0, "end")

    # Insert the new values into the entries
    totalMass_entry.insert(0, f"{totalMass:.3f}")
    dryMass_entry.insert(0, f"{dryMass:.3f}")
    burnTime_entry.insert(0, f"{burnTime:.3f}")
    totalImpulse_entry.insert(0, f"{totalImpulse:.3f}")
    propellantMass_entry.insert(0, f"{propellantMass:.3f}")

# Create a button to generate random inputs
random_button = Button(window,
                       text="Generate Random Inputs",
                       command=generate_random_inputs,
                       style="Large.TButton") # Apply the custom style to the button
random_button.grid(row=6,
                   column= 3,
                   columnspan= 3,
                   padx= 10,
                   pady=5)

# Run the main loop of the window
window.mainloop()
