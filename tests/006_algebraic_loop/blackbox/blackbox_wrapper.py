
def exchange(configuration_filename, time, input_names,
              input_values, output_names, save_to_file=False,
              memory=None):
    """
    """
    memory = None

    # Process inputs
    inputs = {}
    for name, value in zip(input_names, input_values):
        inputs[name] = value

    # Multiply value by 2
    value = float(inputs['x']) + float(inputs['u'])
    return [value, memory]


