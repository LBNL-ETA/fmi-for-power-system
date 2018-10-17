# coding: utf-8
from pyfmi import load_fmu
from pyfmi.fmi_coupled import CoupledFMUModelME2

# Load CYME FMU
print('Loading CYME (server ME FMU) ...')
cyme = load_fmu('cyme/simulator.fmu', log_level=7)
cyme.setup_experiment(start_time=0, stop_time=10)

# Load PV
print('Loading the PV (Modelica FMU) ...')
P_A = 750 * 4  # m2
pv = load_fmu('pv/pv.fmu', log_level=7)
ref = pv.get_variable_valueref("filNam")
pv.set_string([ref],
              [bytes('pv/' + 'USA_CA_San.Francisco.Intl.AP.724940_TMY3.mos')])
pv.setup_experiment(start_time=0, stop_time=10)
pv.set("A_PV", P_A)  # m2
pv.set("azi", 180)
print('Done loading FMUs')

# Connect FMUs and create Master
print('Create master')
models = [("cyme", cyme), ("pv", pv)]
connections = [(pv, "PV_generation", cyme, "IEEE34NODES_836_KW")]
master = CoupledFMUModelME2(models, connections)
options = master.simulate_options()
options['ncp'] = 10
print('Run simulation')
results = master.simulate(options=options, final_time=10.0)

print('Done terminate FMUs')
cyme.terminate()
pv.terminate()

# Plot the results
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 3))
plt.plot(results["time"], results["cyme.voltage_836_Vpu"])
plt.ylabel("Voltage [p.u.]")
plt.xlabel("Time")
plt.show()

