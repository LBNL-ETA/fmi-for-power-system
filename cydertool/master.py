import pandas
import datetime
try:
    import cympy
except:
    pass
import json
import os

def sim(datetimes, substation_filename, scada_filename, source_node,
        add_pvs=False, add_pvqs=False, add_evs=False, result_factory=Result,
        substation_powerflow=True, feeder_powerflow=False, result_options={}):
    # Open and set the substation
    substation = Substation(substation_filename)
    scada = Scada(scada_filename, feeder_powerflow)

    # Create PV simulators
    if add_pvs:
        pv_ids = ['PV' + str(index) for index in range(0, len(add_pvs['node_ids']))]
        substation.add_power_devices(node_ids=add_pvs['node_ids'],
                                     network_ids=add_pvs['network_ids'],
                                     device_ids=pv_ids)
        pvfactory = PVFactory(add_pvs['ghi_filename'])
        pvs = pvfactory.create(add_pvs['pv_capacities'], pv_ids)

    # Create Inverter simulators
    if add_pvqs:
        pvq_ids = ['Q' + str(index) for index in range(0, len(add_pvqs['node_ids']))]
        substation.add_power_devices(node_ids=add_pvqs['node_ids'],
                                     network_ids=add_pvqs['network_ids'],
                                     device_ids=pvq_ids)
        pvqfactory = PVQFactory()
        if 'setpoints' not in add_pvqs:
          add_pvqs['setpoints'] = 'default'
        pvqs = pvqfactory.create(add_pvqs['apparent_powers'], add_pvqs['setpoints'],
                                 pvq_ids)

    # Create EV simulators
    if add_evs:
        ev_ids = ['EV' + str(index) for index in range(0, len(add_evs['node_ids']))]
        substation.add_power_devices(node_ids=add_evs['node_ids'],
                                     network_ids=add_evs['network_ids'],
                                     device_ids=ev_ids)
        if 'nrdc' in add_evs:
            evfactory = EVFactory_nrdc(add_evs['residential_filename'],
                                       add_evs['commercial_filename'],
                                       add_evs['industrial_filename'])
            evs = evfactory.create(add_evs['nb_evs_residential'],
                                   add_evs['nb_evs_commercial'],
                                   add_evs['nb_evs_industrial'],
                                   ev_ids)
        else:
            evfactory = EVFactory(add_evs['home_filename'],
                                  add_evs['work_filename'],
                                  datetimes[0])
            evs = evfactory.create(add_evs['nb_evs'],
                                   add_evs['location_categories'],
                                   ev_ids)

    # Run simulation
    pv_generations = False
    pvq_generations = False
    ev_demands = False
    result = result_factory(add_pvs, add_pvqs, add_evs, source_node, result_options)
    print('Run substation from ' +
          datetimes[0].strftime("%Y-%m-%d %H:%M:%S") + ' to ' +
          datetimes[-1].strftime("%Y-%m-%d %H:%M:%S"))
    for t in datetimes:
        # Set the base load
        feeder_baseloads = scada.get(t)
        substation.baseload_allocation(feeder_loads=feeder_baseloads)

        # Add PVs
        if add_pvs:
            pv_generations = [pv.get(t) for pv in pvs]
            substation.set_power_devices(device_ids=[pv.id for pv in pvs],
                                         values=pv_generations)


        if add_evs:
            ev_node_voltages = []
            ev_demands = [ev.get(t) for ev in evs]
            substation.set_power_devices(device_ids=[ev.id for ev in evs],
                                         values=ev_demands)

        # Export model file for PY
        # export_model_file_path = os.getcwd() + '\\pv_simulation_results\\' + datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S_")  + '.sxst'
        # print(export_model_file_path)
        # cympy.study.Save(export_model_file_path)

        # Run powerflow
        if substation_powerflow:
            substation.run_powerflow(run_all=True)
        else:
            substation.run_powerflow(feeders=feeder_baseloads.keys())

        # Add controlable devices (they need voltage at the current time)
        if add_pvqs:
            pvq_node_voltages = substation.get_voltage_from_node_ids(
                                    add_pvqs['node_ids'])
            pvq_generations = [pvq.get(t, cast_to_float(v)) for pvq, v
                              in zip(pvqs, pvq_node_voltages)]
            substation.set_power_devices(device_ids=[pvq.id for pvq in pvqs],
                                         values=pvq_generations, reactive=True)

        # Run powerflow after controlable device are set
        if add_pvqs: # or add_evs:
            if substation_powerflow:
                substation.run_powerflow(run_all=True)
            else:
                substation.run_powerflow(feeders=feeder_baseloads.keys())

        # Save the results
        result.save(t, substation, feeder_baseloads, pv_generations,
                    pvq_generations, ev_demands)

    return result.results

def cast_to_float(value):
    try:
        return float(value)
    except:
        return 1.0

if __name__ == "__main__":
    # # Get all the nodes in a CSV file
    # substation = Substation('substations/BU0006Feeders_v2Change.sxst')
    # nodes = substation.list_nodes()
    # nodes.to_csv('all_nodes.csv', encoding='utf-8')

    # Run simulation
    datetimes = []
    substation_filename = 'substations/BU0006Feeders_v2Change.sxst'
    scada_filename = 'scada/BU0006_processed.csv'
    add_pvs = {'network_ids': [],
               'node_ids': [],
               'pv_capacities': [],
               'ghi_filename': '../data/solar.csv'}
    add_pvqs = {}
    add_evs = {}

    results = sim(datetimes, substation_filename, scada_filename,
                  add_pvs=False, add_pvqs=False, add_evs=False)

    # Write results to file
    with open('result.json', 'w') as outfile:
        json.dump(results, outfile)
