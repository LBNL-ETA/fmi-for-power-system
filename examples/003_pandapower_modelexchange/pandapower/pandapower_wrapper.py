import pandapower as pp
import pandapower.networks as pn
import datetime as dt

def exchange(configuration_filename, time, input_names,
              input_values, output_names, save_to_file=False,
              memory=None):
    """
    """

    if memory is None:
        memory = pn.case33bw()
        memory['ext_grid'].loc[0, 'vm_pu'] = 1.05
        header = ('sim_time,clock,' +
                  ','.join(input_names) + ',' +
                  ','.join(output_names) + '\n')
        with open("debug.csv", "w") as f:
            f.write(header)

    # Process inputs
    inputs = {}
    for name, value in zip(input_names, input_values):
        inputs[name] = value

    # Change loading
    for name in input_names:
        if 'KW' in name:
            bus_index = int(name.split('_')[1])
            bus_index = memory['load'][memory['load']['bus'] == bus_index].index
            memory['load'].loc[bus_index, 'p_kw'] += inputs[name] / -1
        if 'KVAR' in name:
            bus_index = int(name.split('_')[1])
            bus_index = memory['load'][memory['load']['bus'] == bus_index].index
            memory['load'].loc[bus_index, 'q_kvar'] += inputs[name] / -1

    # Run powerflow
    pp.runpp(memory)

    # Revert loading changes
    for name in input_names:
        if 'KW' in name:
            bus_index = int(name.split('_')[1])
            bus_index = memory['load'][memory['load']['bus'] == bus_index].index
            memory['load'].loc[bus_index, 'p_kw'] -= inputs[name] / -1
        if 'KVAR' in name:
            bus_index = int(name.split('_')[1])
            bus_index = memory['load'][memory['load']['bus'] == bus_index].index
            memory['load'].loc[bus_index, 'q_kvar'] -= inputs[name] / -1

    # Get outputs
    outputs = []
    for name in output_names:
        if 'Vpu' in name:
            bus_index = int(name.split('_')[1])
            outputs.append(
                memory['res_bus'].loc[bus_index, 'vm_pu'])

    # [Optional debug]
    with open("debug.csv", "a") as f:
        row = (str(time) + ',' +
               str(dt.datetime.now()) + ',' +
               ','.join(map(str, input_values)) + ',' +
               ','.join(map(str, outputs)) + '\n')
        f.write(row)
    print(row)
    return [outputs, memory]
