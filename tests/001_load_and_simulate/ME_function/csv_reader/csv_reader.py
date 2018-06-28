import pandas

def step(configuration_filename, time, input_names,
         input_values, output_names, memory=None):
    """
    TODO: 
    - change configuration_filename for (parameter_names, parameter_values)
    """
    if memory is None:
        memory = pandas.read_csv(configuration_filename, index_col=0)

    # Process inputs
    inputs = {}
    for name, value in zip(input_names, input_values):
        inputs[name] = value

    # Read value
    value = memory.loc[int(time), memory.columns[int(inputs['column'])]]
    return [value, memory]


