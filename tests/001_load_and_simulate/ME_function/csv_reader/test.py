import csv_reader

configuration_filename = 'data.csv'
time = int(1.0)
input_names = ['column']
input_values = [int(0.0)]
output_names = ['y']
memory = None

print('Test function: ')
value, memory = csv_reader.step(
    configuration_filename, time, input_names,
    input_values, output_names, memory)
print('Success: ' + str(value))

time = int(2.0)
value, memory = csv_reader.step(
    configuration_filename, time, input_names,
    input_values, output_names, memory)
print('Success: ' + str(value))