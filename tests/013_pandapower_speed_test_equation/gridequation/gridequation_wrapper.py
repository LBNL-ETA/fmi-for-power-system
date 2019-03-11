import datetime as dt

def exchange(configuration_filename, time, input_names,
              input_values, output_names, save_to_file=False,
              memory=None):
    """
    """
    # Process inputs
    result = 0
    P = 0
    Pmax = 2000
    Q = 0
    Qmax = 2000 * 1.05 * 0.44
    for name, value in zip(input_names, input_values):
        if 'KW' in name:
            P = float(value)
        if 'KVAR' in name:
            Q = float(value)
    result = 1.0 + 0.1 * P / float(Pmax) + 0.1 * Q / float(Qmax)
    outputs = [result]

    if memory is None:
        memory = 1
        header = ('sim_time,clock,' +
                  ','.join(input_names) + ',' +
                  ','.join(output_names) + '\n')
        with open("debug.csv", "w") as f:
            f.write(header)

    # [Optional debug]
    with open("debug.csv", "a") as f:
        row = (str(time) + ',' +
               str(dt.datetime.now()) + ',' +
               ','.join(map(str, input_values)) + ',' +
               ','.join(map(str, outputs)) + '\n')
        f.write(row)
    print(row)
    return [result, memory]
