import pandapower as pp
import pandapower.networks as pn

def exchange(configuration_filename, time, input_names,
              input_values, output_names, save_to_file=False,
              memory=None):
    """
    """
    if memory is None:
        memory = pn.case33bw()
        memory['ext_grid'].loc[0, 'vm_pu'] = 1.05

    # Process inputs
    inputs = {}
    for name, value in zip(input_names, input_values):
        inputs[name] = value

    # Change loading
    for name in input_names:
        if 'KW' in name:
            bus_index = int(name.split('_')[1])
            memory['load'].loc[bus_index, 'p_kw'] += inputs[name] / -1000
        if 'KVAR' in name:
            bus_index = int(name.split('_')[1])
            memory['load'].loc[bus_index, 'q_kvar'] += inputs[name]

    # Run powerflow
    pp.runpp(memory)

    # Revert loading changes
    for name in input_names:
        if 'KW' in name:
            bus_index = int(name.split('_')[1])
            memory['load'].loc[bus_index, 'p_kw'] -= inputs[name] / -1000
        if 'KVAR' in name:
            bus_index = int(name.split('_')[1])
            memory['load'].loc[bus_index, 'q_kvar'] -= inputs[name]

    # Get outputs
    outputs = []
    for name in output_names:
        if 'Vpu' in name:
            bus_index = int(name.split('_')[1])
            outputs.append(
                memory['res_bus'].loc[bus_index, 'vm_pu'])
    return [outputs, memory]
