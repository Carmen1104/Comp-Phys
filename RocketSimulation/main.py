import numpy as np
import matplotlib.pyplot as plt
from func import integrateGraph

totalMass = 1
dryMass = 0.906
burnTime = 3.4
totalImpulse = 49.6
propellantMass = 0.064
averageThrust = totalImpulse/burnTime
massFlowRate = propellantMass/burnTime

time = np.linspace(0, 10, 100, False)

index = np.argmax(time==burnTime) + 1
thrust = np.append(np.repeat(averageThrust, index), np.repeat(0, len(time) - index))
mass = np.append(np.repeat(totalMass, index) - time[0:index] * massFlowRate, np.repeat(dryMass, len(time) - index))
acceleration = thrust/mass - 9.81
velocity = integrateGraph(time, acceleration)
displacement = integrateGraph(time, velocity)

plt.plot(time, displacement)
plt.plot(time, velocity)
plt.legend(["Displacement", "Velocity"])
plt.xlabel("Time")
plt.show()