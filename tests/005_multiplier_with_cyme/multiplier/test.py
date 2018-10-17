import multiplier_wrapper

time = int(1.0)
input_names = 'x'
input_values = 1.0
output_names = 'y'
memory = None

print('Test function: ')
value, memory = multiplier_wrapper.exchange(
    '', time, input_names,
    input_values, output_names, False, memory)
print('Success: ' + str(value))

input_values = 2.0
value, memory = multiplier_wrapper.exchange(
    '', time, input_names,
    input_values, output_names, False, memory)
print('Success: ' + str(value))