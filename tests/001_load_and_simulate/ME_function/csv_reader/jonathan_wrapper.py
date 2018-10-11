import pandas

def exchange(configuration_filename, time, input_names,
              input_values, output_names, save_to_file=False,
              memory=None):
    """
    TODO: 
    - change configuration_filename for (parameter_names, parameter_values)
    """
    input_names = [input_names]
    input_values = [input_values]
    if memory is None:
        memory = pandas.read_csv(configuration_filename, index_col=0)

    # Process inputs
    inputs = {}
    for name, value in zip(input_names, input_values):
        inputs[name] = value

    # Read value
    value = memory.loc[int(time), memory.columns[int(inputs['column'])]]
    print(value)
    return [value, memory]


