# coding: utf-8
from pyfmi import load_fmu
from pyfmi.fmi_coupled import CoupledFMUModelME2

# Load CSV reader FMU
print('Loading the csv reader (server ME FMU) ...')
csv_reader = load_fmu('csv_reader/simulator.fmu', log_level=7)
csv_reader.setup_experiment(start_time=0, stop_time=20)

print('Loading the multiplier (function ME FMU) ...')
multiplier = load_fmu('multiplier/multiplier.fmu', log_level=7)
multiplier.setup_experiment(start_time=0, stop_time=20)
print('Done loading FMUs')

# Create the Master algorithm and launch the simulation
print('Create master')
models = [("csv_reader", csv_reader), ("multiplier", multiplier)]
connections = [(csv_reader, "y", multiplier, "x")]
master = CoupledFMUModelME2(models, connections)
options = master.simulate_options()
options['ncp'] = 23
print('Run simulation')
results = master.simulate(options=options, final_time=23.0)

# Terminate FMUs
print('Done terminate FMUs')
csv_reader.terminate()
multiplier.terminate()

# Plot the results
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 3))
plt.plot(results["time"], results["csv_reader.y"],
    label='CSV data')
plt.plot(results["time"], results["multiplier.y"],
    label='Multiply by 2')
plt.ylabel("Results")
plt.xlabel("Time")
plt.legend(loc=0)
plt.show()
