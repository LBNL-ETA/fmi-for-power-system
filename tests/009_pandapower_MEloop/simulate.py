# coding: utf-8
from pyfmi import load_fmu
from pyfmi.fmi_coupled import CoupledFMUModelME2
import datetime as dt

start = dt.datetime(2018, 6, 17, 3, 0, 0)
end = dt.datetime(2018, 6, 17, 22, 5, 0)
begin = dt.datetime(2018, 1, 1, 0, 0, 0)
start_s = int((start - begin).total_seconds())
end_s = int((end - begin).total_seconds())
print('Start: ' + str(start_s) + ' seconds')
print('End: ' + str(end_s) + ' seconds')

# Load bbq FMU
print('Loading pandapower (function ME FMU) ...')
pp = load_fmu('pandapower/pandapower.fmu', log_level=7)
pp.setup_experiment(start_time=start_s, stop_time=end_s)

# Load PV
print('Loading the PV (Modelica FMU) ...')
P_A = 750 * 14  # m2
pv = load_fmu('pv/pv.fmu', log_level=7)
ref = pv.get_variable_valueref("filNam")
pv.set_string([ref],
              [bytes('pv/' + 'USA_CA_San.Francisco.Intl.AP.724940_TMY3.mos')])
pv.setup_experiment(start_time=start_s, stop_time=end_s)
pv.set("A_PV", P_A)  # m2
pv.set("azi", 180)


# Load inverter
print('Loading the inverter (Modelica FMU) ...')
P_max = P_A * 1000 * 0.12 / 1000
S_max = P_max + 0.05 * P_max
print('Smax: ' + str(S_max) + 'kVAR')
controls = []
for index in range(0, 3):
    controls.append(load_fmu(
        'inverter/CyDER_HIL_Controls_voltVar_0param_0firstorder.fmu',
        log_level=7))
    controls[-1].setup_experiment(start_time=start_s, stop_time=end_s)
    controls[-1].set("QMaxCap", 0.3 * S_max)
    controls[-1].set("QMaxInd", 0.3 * S_max)
    controls[-1].set("thr", 0.07)
    controls[-1].set("hys", 0.033)
print('Done loading FMUs')

# Connect FMUs and create Master
print('Create master')
models = [("pp", pp), ("pv", pv),
          ("control_0", controls[0]),
          ("control_1", controls[1]),
          ("control_2", controls[2])]
connections = [(pv, "PV_generation", pp, "KW_7"),
               (pv, "PV_generation", pp, "KW_8"),
               (pv, "PV_generation", pp, "KW_9"),
               (controls[0], "QCon", pp, "KVAR_7"),
               (controls[1], "QCon", pp, "KVAR_8"),
               (controls[2], "QCon", pp, "KVAR_9"),
               (pp, "Vpu_7", controls[0], "v"),
               (pp, "Vpu_8", controls[1], "v"),
               (pp, "Vpu_9", controls[2], "v")]
master = CoupledFMUModelME2(models, connections)
options = master.simulate_options()
options['ncp'] = 200
print('Run simulation')
results = master.simulate(options=options,
    start_time=start_s, final_time=end_s)

print('Done terminate FMUs')
pp.terminate()
pv.terminate()
for control in controls:
    control.terminate()

# Plot the results
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 3))
plt.plot(results["time"],
         results["pv.PV_generation"])
plt.ylabel("PV generation [W]")
plt.xlabel("Time")

plt.figure(figsize=(10, 3))
plt.plot(results["time"],
         results["control_0.QCon"],
         label='control_0')
plt.plot(results["time"],
         results["control_1.QCon"],
         label='control_1')
plt.plot(results["time"],
         results["control_2.QCon"],
         label='control_2')
plt.ylabel("Reactive power [kVAR]")
plt.xlabel("Time")
plt.legend(loc=0)

plt.figure(figsize=(10, 3))
plt.plot(results["time"],
         results["pp.Vpu_7"],
         label='Vpu_7')
plt.plot(results["time"],
         results["pp.Vpu_8"],
         label='Vpu_8')
plt.plot(results["time"],
         results["pp.Vpu_9"],
         label='Vpu_9')
plt.plot(results["time"],
         results["pp.Vpu_17"],
         label='Vpu_17')
plt.ylabel("Voltage [p.u.]")
plt.xlabel("Time")
plt.legend(loc=0)
plt.show()

