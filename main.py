# Import libraries
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # for embedding plot in tkinter
import tkinter as tk # for creating GUI
from matplotlib.animation import FuncAnimation # for creating animation

# Define variables
g = 9.8 # gravity in m/s^2

# Define functions for ODEs
def deriv(t, u):
    x, xdot, z, zdot = u # unpack variables
    speed = np.hypot(xdot, zdot) # calculate speed
    xdotdot = -k/m * speed * xdot # calculate acceleration along x-axis
    zdotdot = -k/m * speed * zdot - g # calculate acceleration along y-axis
    return xdot, xdotdot, zdot, zdotdot # return derivatives

# Define events to stop integration when hitting target or reaching max height
def hit_target(t,u):
    # We've hit the target if the z-coordinate is zero.
    return u[2]
# Stop integration when we hit target
hit_target.terminal = True
# We must be moving downwards (don't stop before we begin moving upwards!)
hit_target.direction = -1

def max_height(t,u):
    # The maximum height is obtained when the z-velocity is zero.
    return u[3]

# Define function to plot the trajectory
def plot_trajectory():
    global k, m # access global variables
    # Get the input values from the entry widgets
    theta = float(angle_entry.get()) # angle in degrees
    v0 = float(speed_entry.get()) # initial speed in m/s
    c = float(drag_entry.get()) # drag coefficient
    r = float(radius_entry.get()) # radius of projectile in m
    m = float(mass_entry.get()) # mass of projectile in kg
    rho_air = float(density_entry.get()) # air density in kg/m^3
    
    # Calculate initial velocities along x and y axes
    v0x = v0 * np.cos(np.radians(theta)) # initial speed along x-axis in m/s
    v0y = v0 * np.sin(np.radians(theta)) # initial speed along y-axis in m/s
    
    # Calculate cross-sectional area and constant for convenience
    A = np.pi * r**2 # cross-sectional area of projectile in m^2
    k = 0.5 * c * rho_air * A # constant for convenience
    
    # Define initial conditions: x0, v0_x, z0, v0_z.
    u0 = [0, v0x, 0., v0y]

    # Integrate up to tf unless we hit the target sooner.
    t0, tf = [0,50]

    # Solve the ODEs with initial conditions and events
    soln = solve_ivp(deriv, (t0, tf), u0, dense_output=True, events=(hit_target, max_height))

    # Print some results on the console widget
    console_text.delete(1.0, tk.END) # clear previous text
    console_text.insert(tk.END, soln) 
    console_text.insert(tk.END, '\nTime to target = {:.2f} s\n'.format(soln.t_events[0][0]))
    console_text.insert(tk.END, 'Time to highest point = {:.2f} s\n'.format(soln.t_events[1][0]))

    # Create a fine grid of time points from 0 until impact time.
    t = np.linspace(0, soln.t_events[0][0], 100)

    # Retrieve the solution for the time grid and plot the trajectory.
    sol = soln.sol(t)
    
    console_text.insert(tk.END,'Range to target, xmax = {:.2f} m\n'.format(sol[0][-1]))
    console_text.insert(tk.END,'Maximum height, zmax = {:.2f} m\n'.format(max(sol[2])))
    
    fig.clear() # clear previous plot
    
    ax = fig.add_subplot(111) 
   
   
    ax.set_xlabel('Distance (m)')
    ax.set_ylabel('Height (m)')
    ax.set_title('Projectile motion with drag')
   
   # Define a function to update the plot for each frame
    def animate(i):
       # Plot the trajectory up to the i-th time point
       ax.plot(sol[0][:i], sol[2][:i], color='blue')
       # Plot the current position of the projectile as a red dot
       ax.plot(sol[0][i], sol[2][i], 'ro')
   
   # Create an animation object with 100 frames, no repeat and 50 ms interval
    anim = FuncAnimation(fig, animate, frames=100, repeat=False, interval=50)
   
    canvas.draw() # update the plot on the canvas widget

# Create a tkinter window
window = tk.Tk()
window.title('Projectile motion with drag GUI')
window.geometry('800x600') # set window size

# Create a frame for the input widgets
input_frame = tk.Frame(window)
input_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

# Create labels and entry widgets for the input parameters
angle_label = tk.Label(input_frame, text='Enter the angle in degrees:')
angle_label.grid(row=0, column=0, sticky=tk.W)
angle_entry = tk.Entry(input_frame)
angle_entry.grid(row=0, column=1, sticky=tk.E)

speed_label = tk.Label(input_frame, text='Enter the initial speed in m/s:')
speed_label.grid(row=1, column=0, sticky=tk.W)
speed_entry = tk.Entry(input_frame)
speed_entry.grid(row=1, column=1, sticky=tk.E)

drag_label = tk.Label(input_frame, text='Enter the drag coefficient:')
drag_label.grid(row=2, column=0, sticky=tk.W)
drag_entry = tk.Entry(input_frame)
drag_entry.grid(row=2, column=1, sticky=tk.E)

radius_label = tk.Label(input_frame, text='Enter the radius of projectile in m:')
radius_label.grid(row=3, column=0, sticky=tk.W)
radius_entry = tk.Entry(input_frame)
radius_entry.grid(row=3, column=1, sticky=tk.E)

mass_label = tk.Label(input_frame, text='Enter the mass of projectile in kg:')
mass_label.grid(row=4, column=0, sticky=tk.W)
mass_entry = tk.Entry(input_frame)
mass_entry.grid(row=4, column=1, sticky=tk.E)

density_label = tk.Label(input_frame, text='Enter the air density in kg/m^3:')
density_label.grid(row=5, column=0, sticky=tk.W)
density_entry = tk.Entry(input_frame)
density_entry.grid(row=5, column=1, sticky=tk.E)

# Create a button to plot the trajectory
plot_button = tk.Button(input_frame, text='Plot trajectory', command=plot_trajectory)
plot_button.grid(row=6, columnspan=2)

# Create a frame for the output widgets
output_frame = tk.Frame(window)
output_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

# Create a figure and a canvas widget to display the plot
fig = plt.figure(figsize=(6,4))
canvas = FigureCanvasTkAgg(fig, master=output_frame) 
canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create a text widget to display the console output
console_text = tk.Text(output_frame)
console_text.pack(side=tk.RIGHT, fill=tk.BOTH)

# Start the main loop of the window
window.mainloop()
