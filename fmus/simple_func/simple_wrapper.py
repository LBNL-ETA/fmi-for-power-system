
def exchange(configuration_filename, time, input_names,
              input_values, output_names, save_to_file=False,
              memory=None):
    """
    """

    # Process inputs
    result = 1
    for name, value in zip(input_names, input_values):
        result *= value
    outputs = [result]

    # [Optional debug]
    with open("debug.csv", "a") as f:
        row = (str(time) + ',' +
               str(dt.datetime.now()) + ',' +
               ','.join(map(str, input_values)) + ',' +
               ','.join(map(str, outputs)) + '\n')
        f.write(row)
    return [outputs, memory]
