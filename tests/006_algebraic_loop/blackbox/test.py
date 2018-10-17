import blackbox_wrapper

time = 1.0
input_names = ['x', 'u']
input_values = [1.0, 0.0]
output_names = 'y'
memory = None

print('Test function: ')
value, memory = blackbox_wrapper.exchange(
    '', time, input_names,
    input_values, output_names, False, memory)
print('Success: ' + str(value))

input_values = [1.0, 2.0]
value, memory = blackbox_wrapper.exchange(
    '', time, input_names,
    input_values, output_names, False, memory)
print('Success: ' + str(value))