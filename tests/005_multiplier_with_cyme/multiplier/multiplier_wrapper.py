import pandas

def exchange(configuration_filename, time, input_names,
              input_values, output_names, save_to_file=False,
              memory=None):
    """
    TODO: 
    - change configuration_filename for (parameter_names, parameter_values)
    """
    # If input is not a list because it's a single input
    # (should be fix in SimulatorToFMU to have consistent behavior)
    input_names = [input_names]
    input_values = [input_values]
    memory = None

    # Process inputs
    inputs = {}
    for name, value in zip(input_names, input_values):
        inputs[name] = value

    # Multiply value by 2
    value = float(inputs['x']) * 2.0
    return [value, memory]


