
# coding: utf-8

# In[1]:


from pyfmi import load_fmu
from pyfmi.master import Master


# In[ ]:


# Load CSV reader FMU
print('line 15')
csv_reader = load_fmu('csv_reader/simulator.fmu', log_level=7)
print('line 16')
csv_reader.setup_experiment(start_time=0, stop_time=20)
print('line 17')

# In[ ]:


# Create the Master algorithm
master = Master([csv_reader], [])
options = master.simulate_options()
options['step_size'] = 1.0

# Launch the simulation
results = master.simulate(options=options, final_time=23.0)
csv_reader.terminate()


# In[ ]:


# Plot the results
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 3))
plt.plot(results[csv_reader]["time"], results[csv_reader]["y"])
plt.ylabel("Data from the CSV file")
plt.xlabel("Time")
plt.show()

