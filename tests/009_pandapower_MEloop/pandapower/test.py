import pandapower_wrapper as ppw
import datetime as dt

input_names = ['8_KW', '7_KW', '9_KW', '8_KVAR', '7_KVAR', '9_KVAR']
input_values = [-50, -50, -50, 10, 10, 10]
output_names = ['8_Vpu', '7_Vpu', '9_Vpu']

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