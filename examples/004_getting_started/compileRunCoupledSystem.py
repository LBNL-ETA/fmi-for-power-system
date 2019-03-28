from pymodelica import compile_fmu
from pyfmi import load_fmu
from pyfmi import Master
import matplotlib.pyplot as plt
import os

# This script compiles two Modelica models as FMUs for co-simulation.
# It then loads the models, connect them and run them using the master algorithm
# PyFMI. The implementation of the models can be seen in the Modelica code.
# The model "generator" creates a wave, whereas the model controller switches its
# output whenever its input crosses a threshold of 120.

start_time=0
final_time=10

if not(os.path.isfile('HELICS_CyDER_Generator.fmu')):
    compile_fmu('HELICS_CyDER.Generator', 'HELICS_CyDER.mo', version='2.0', target='cs');
if not(os.path.isfile('HELICS_CyDER_Controller.fmu')):
    compile_fmu('HELICS_CyDER.Controller', 'HELICS_CyDER.mo', version='2.0', target='cs');

# Load the compile FMUs
generator=load_fmu('HELICS_CyDER_Generator.fmu')
controller=load_fmu('HELICS_CyDER_Controller.fmu')

# Create the list of FMUs
models=[generator, controller]

# Connect the FMUs
connections=[(generator, 'y', controller, 'u')]

# Create an instance of the master
master=Master(models, connections)

# Get the options
opts=master.simulate_options()
opts['step_size']=0.01

# Simulate the master instance
res=master.simulate(options=opts, start_time=start_time, final_time=final_time)

# Get the results
con_tim=res[controller]["time"]
con_y=res[controller]["y"]
gen_tim=res[generator]["time"]
gen_y=res[generator]["y"]

# Plot the results
plt.figure(1)

plt.subplot(211)
plt.plot(gen_tim, gen_y)
plt.ylabel('Generator')

plt.subplot(212)
plt.plot(con_tim, con_y)
plt.ylabel('Controller')

plt.show()
