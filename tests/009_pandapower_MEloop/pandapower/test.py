import pandapower_wrapper as ppw
import datetime as dt

input_names = ['KW_8', 'KW_7', 'KW_9', 'KVAR_8', 'KVAR_7', 'KVAR_9']
input_values = [-50, -50, -50, 10, 10, 10]
output_names = ['Vpu_8', 'Vpu_7', 'Vpu_9']

time1 = dt.datetime.now()
results = ppw.exchange('configuration_filename', 0, input_names,
                   input_values, output_names, memory=None)
time2 = dt.datetime.now()
print('Test')
print((time2 - time1).total_seconds())
print(results[:-1])
print('')

input_values = [-100, -100, -100, 10, 10, 10]
time1 = dt.datetime.now()
results = ppw.exchange('configuration_filename', 0, input_names,
                   input_values, output_names, memory=results[-1])
time2 = dt.datetime.now()
print('Test')
print((time2 - time1).total_seconds())
print(results[:-1])
print('')

input_values = [100, 100, 100, 10, 10, 10]
time1 = dt.datetime.now()
results = ppw.exchange('configuration_filename', 0, input_names,
                   input_values, output_names, memory=results[-1])
time2 = dt.datetime.now()
print('Test')
print((time2 - time1).total_seconds())
print(results[:-1])
print('')