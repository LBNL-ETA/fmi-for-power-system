import json
import pandas as pd


class Result(object):
    """
    Save simulation results
    """
    def __init__(self, add_pvs, add_pvqs, add_evs, source_node, result_options):
        self.results = {'add_pvs': add_pvs,
                        'add_pvqs': add_pvqs,
                        'add_evs': add_evs,
                        'scada': [],
                        'pv_generations': [],
                        'pvq_generations': [],
                        'ev_demands': [],
                        'pv_node_voltages': [],
                        'pvq_node_voltages': [],
                        'ev_node_voltages': [],
                        'total_p_measured': [],
                        'total_q_measured': [],
                        'high_voltages': [],
                        'low_voltages': [],
                        'times': []}
        self.source_node = source_node

    def save(self, time, substation, scada, pv_generations,
             pvq_generations, ev_demands):
        # Get time and SCADA
        self.results['times'].append(time.strftime("%Y-%m-%d %H:%M:%S"))
        self.results['scada'].append(scada)

        # Get voltage at each node where we have connected a device
        if pv_generations:
            self.results['pv_node_voltages'].append(
                substation.get_voltage_from_node_ids(
                    self.results['add_pvs']['node_ids']))
        if pvq_generations:
            self.results['pvq_node_voltages'].append(
                substation.get_voltage_from_node_ids(
                    self.results['add_pvqs']['node_ids']))
        if ev_demands:
            self.results['ev_node_voltages'].append(
                substation.get_voltage_from_node_ids(
                    self.results['add_evs']['node_ids']))

        # Get active and reactive power at each device
        self.results['pv_generations'].append(pv_generations)
        self.results['pvq_generations'].append(pvq_generations)
        self.results['ev_demands'].append(ev_demands)

        # Get Worst voltage conditions through CYME
        source_node = self.source_node  # TODO: add substation.get_source_node() 'SOURCE_2405BK1'
        high = ({info: substation.get_info_node(source_node, info)
          for info in ['DwHighVoltWorstA', 'DwHighVoltWorstB', 'DwHighVoltWorstC']})
        low = ({info: substation.get_info_node(source_node, info)
          for info in ['DwLowVoltWorstA', 'DwLowVoltWorstB', 'DwLowVoltWorstC']})
        self.results['high_voltages'].append(high)
        self.results['low_voltages'].append(low)

        # Get P and Q at the source node
        self.results['total_p_measured'].append(substation.get_info_node(source_node, 'KWTOT'))
        self.results['total_q_measured'].append(substation.get_info_node(source_node, 'KVARTOT'))

    def to_json(self, filename='results.json'):
        with open(filename, 'w') as outfile:
            json.dump(self.results, outfile)


class DetailedResult(object):
    """
    Save simulation results
    """
    def __init__(self, add_pvs, add_pvqs, add_evs, source_node, result_options):
        self.results = {'add_pvs': add_pvs,
                        'add_pvqs': add_pvqs,
                        'add_evs': add_evs,
                        'scada': [],
                        'pv_generations': [],
                        'pvq_generations': [],
                        'ev_demands': [],
                        'pv_node_voltages': [],
                        'pvq_node_voltages': [],
                        'ev_node_voltages': [],
                        'total_p_measured': [],
                        'total_q_measured': [],
                        'high_voltages': [],
                        'low_voltages': [],
                        'worst_loading':[],
                        'times': [],
                        'nodes': False,
                        'sections': False,
                        'devices': False}
        self.source_node = source_node
        self.save_time = result_options['save_time']

    def save(self, time, substation, scada, pv_generations,
             pvq_generations, ev_demands):
        # Get time and SCADA
        self.results['times'].append(time.strftime("%Y-%m-%d %H:%M:%S"))
        self.results['scada'].append(scada)

        # Get voltage at each node where we have connected a device
        if pv_generations:
            self.results['pv_node_voltages'].append(
                substation.get_voltage_from_node_ids(
                    self.results['add_pvs']['node_ids']))
        if pvq_generations:
            self.results['pvq_node_voltages'].append(
                substation.get_voltage_from_node_ids(
                    self.results['add_pvqs']['node_ids']))
        if ev_demands:
            self.results['ev_node_voltages'].append(
                substation.get_voltage_from_node_ids(
                    self.results['add_evs']['node_ids']))

        # Get active and reactive power at each device
        self.results['pv_generations'].append(pv_generations)
        self.results['pvq_generations'].append(pvq_generations)
        self.results['ev_demands'].append(ev_demands)

        # Get Worst voltage conditions through CYME
        source_node = self.source_node  # TODO: add substation.get_source_node() 'SOURCE_2405BK1'
        high = ({info: substation.get_info_node(source_node, info)
          for info in ['DwHighVoltWorstA', 'DwHighVoltWorstB', 'DwHighVoltWorstC']})
        low = ({info: substation.get_info_node(source_node, info)
          for info in ['DwLowVoltWorstA', 'DwLowVoltWorstB', 'DwLowVoltWorstC']})
        self.results['high_voltages'].append(high)
        self.results['low_voltages'].append(low)
        self.results['worst_loading'].append(
            {info: substation.get_info_node(source_node, info)
          for info in ['DwOverloadWorstA', 'DwOverloadWorstB', 'DwOverloadWorstC']})

        # Get P and Q at the source node
        self.results['total_p_measured'].append(substation.get_info_node(source_node, 'KWTOT'))
        self.results['total_q_measured'].append(substation.get_info_node(source_node, 'KVARTOT'))

        # Save detailed info
        if time == self.save_time:
            feeder_id = list(scada.keys())[0]
            # Save node info id, lat, long, distance, Vpu, kW, kVAR
            nodes = substation.list_nodes()
            nodes.drop('node_object', inplace=True, axis=1)
            nodes = nodes[nodes['network_id'] == feeder_id]
            keywords = ['Vpu', 'VpuA', 'VpuB', 'VpuC', 'KWTOT', 'KVARTOT']
            for keyword in keywords:
                nodes[keyword] = [0] * len(nodes)
            for node in nodes.itertuples():
                for keyword in keywords:
                    nodes.loc[node.Index, keyword] = substation.get_info_node(
                        node.node_id, keyword)
            for keyword in keywords:
                nodes[keyword] = nodes[keyword].apply(lambda x: None if x is '' else float(x))
            self.results['nodes'] = nodes.to_dict()

            # Save devices info id, section, type, distance, overloading
            devices = substation.list_devices()
            devices.drop('device', inplace=True, axis=1)
            devices = devices[devices['network_id'] == feeder_id]
            devices.columns = ['device_type', 'device_id', 'device_section', 'device_network']
            keywords = ['Distance', 'LOADINGA', 'LOADINGB', 'LOADINGC']
            for keyword in keywords:
                devices[keyword] = [0] * len(devices)
            for device in devices.itertuples():
                for keyword in keywords:
                    devices.loc[device.Index, keyword] = substation.get_info_device(
                        device.device_id, keyword, device.device_type)
            for keyword in keywords:
                devices[keyword] = devices[keyword].apply(lambda x: None if x is '' else float(x))
            self.results['devices'] = devices.to_dict()

            # Save sections info id, to and from nodes, length, kW, kVAR
            sections = substation.list_sections()
            sections.drop('section_object', inplace=True, axis=1)
            sections = sections[sections['network_id'] == feeder_id]
            self.results['sections'] = sections.to_dict()


class Node_Result(object):
    """
    Save simulation results
    """
    def __init__(self, add_pvs, add_pvqs, add_evs, source_node, result_options):

        self.arguments = { 'nodes_arguments' : {
                                                'Distance': 'Distance',
                                                'Section Id':'SectionId',
                                                'Feeder Id' : 'FeederId',
                                                'Total through Kvar' : 'KVARTOT',
                                                'Total through KW' : 'KWTOT',
                                                'Balanced KVLN Voltage' : 'VLN',
                                                'KVLN voltage on phase A' : 'VLNA',
                                                'KVLN voltage on phase B' : 'VLNB',
                                                'KVLN voltage on phase C' : 'VLNC',
                                                'Balanced Pu line-to-neutral Voltage' : 'Vpu',
                                                'Pu line-to-neutral voltage on phase A' : 'VpuA',
                                                'Pu line-to-neutral voltage on phase B' : 'VpuB',
                                                'Pu line-to-neutral voltage on phase C' : 'VpuC',
                                                'Worst downstream under-voltage' : 'DwLowVoltWorst3PH',
                                                'Worst downstream over-voltage' : 'DwHighVoltWorst3PH',
                                                'Worst downstream over-voltage phase A' : 'DwHighVoltWorstA',
                                                'Worst downstream over-voltage phase B' : 'DwHighVoltWorstB',
                                                'Worst downstream over-voltage phase C' : 'DwHighVoltWorstC',
                                                'Worst downstream under-voltage phase A' : 'DwLowVoltWorstA',
                                                'Worst downstream under-voltage phase B' : 'DwLowVoltWorstB',
                                                'Worst downstream under-voltage phase C' : 'DwLowVoltWorstC',
                                                'Node Equipment Type' : 'NodeEqType',
                                                'Network Type' : 'NetworkType',
                                                'Latitude' : 'Latitude',
                                                'Longitude' : 'Longitude',
                                            },

        }

        self.results = {    'node_results' : pd.DataFrame(columns=['Distance', 
                                'Section Id', 
                                'Feeder Id', 
                                'Total through Kvar', 
                                'Total through KW', 
                                'Balanced KVLN Voltage', 
                                'KVLN voltage on phase A', 
                                'KVLN voltage on phase B', 
                                'KVLN voltage on phase C', 
                                'Balanced Pu line-to-neutral Voltage', 
                                'Pu line-to-neutral voltage on phase A', 
                                'Pu line-to-neutral voltage on phase B', 
                                'Pu line-to-neutral voltage on phase C', 
                                'Worst downstream under-voltage', 
                                'Worst downstream over-voltage', 
                                'Worst downstream over-voltage phase A', 
                                'Worst downstream over-voltage phase B', 
                                'Worst downstream over-voltage phase C', 
                                'Worst downstream under-voltage phase A', 
                                'Worst downstream under-voltage phase B', 
                                'Worst downstream under-voltage phase C', 
                                'Node Equipment Type', 
                                'Network Type', 
                                'Latitude', 
                                'Longitude']),
                            'other_results' : {'add_pvs': add_pvs,
                                'add_pvqs': add_pvqs,
                                'add_evs': add_evs,
                                'scada': [],
                                'pv_generations': [],
                                'pvq_generations': [],
                                'ev_demands': [],
                                'pv_node_voltages': [],
                                'pvq_node_voltages': [],
                                'ev_node_voltages': [],
                                'total_p_measured': [],
                                'total_q_measured': [],
                                'high_voltages': [],
                                'low_voltages': [],
                                'times': []}
                        }       

        self.source_node = source_node

    def save(self, timestamp, substation, scada, pv_generations,
             pvq_generations, ev_demands):
        # Get time and SCADA
        self.results['other_results']['times'].append(timestamp.strftime("%Y-%m-%d %H:%M:%S"))
        self.results['other_results']['scada'].append(scada)

        # Get voltage at each node where we have connected a device
        if pv_generations:
            self.results['other_results']['pv_node_voltages'].append(
                substation.get_voltage_from_node_ids(
                    self.results['other_results']['add_pvs']['node_ids']))
        if pvq_generations:
            self.results['other_results']['pvq_node_voltages'].append(
                substation.get_voltage_from_node_ids(
                    self.results['other_results']['add_pvqs']['node_ids']))
        if ev_demands:
            self.results['other_results']['ev_node_voltages'].append(
                substation.get_voltage_from_node_ids(
                    self.results['other_results']['add_evs']['node_ids']))

        # Get active and reactive power at each device
        self.results['other_results']['pv_generations'].append(pv_generations)
        self.results['other_results']['pvq_generations'].append(pvq_generations)
        self.results['other_results']['ev_demands'].append(ev_demands)

        # Get Worst voltage conditions through CYME
        source_node = self.source_node  # TODO: add substation.get_source_node() 'SOURCE_2405BK1'
        high = ({info: substation.get_info_node(source_node, info)
          for info in ['DwHighVoltWorstA', 'DwHighVoltWorstB', 'DwHighVoltWorstC']})
        low = ({info: substation.get_info_node(source_node, info)
          for info in ['DwLowVoltWorstA', 'DwLowVoltWorstB', 'DwLowVoltWorstC']})
        self.results['other_results']['high_voltages'].append(high)
        self.results['other_results']['low_voltages'].append(low)

        # Get P and Q at the source node
        self.results['other_results']['total_p_measured'].append(substation.get_info_node(source_node, 'KWTOT'))
        self.results['other_results']['total_q_measured'].append(substation.get_info_node(source_node, 'KVARTOT'))


        # Get all node results
        nodes = substation.list_nodes_extensive(properties=self.arguments['nodes_arguments'])
        timestamp_list = [timestamp] * len(nodes)
        nodes['timestamp'] = pd.Series(timestamp_list)

        self.results['node_results'] = self.results['node_results'].append(nodes, ignore_index=True)


class Extensive_Result(object):
    """
    Save simulation results
    """
    def __init__(self, add_pvs, add_pvqs, add_evs, source_node):

        self.arguments = { 'nodes_arguments' : {
                                                'Distance': 'Distance',
                                                'Section Id':'SectionId',
                                                'Feeder Id' : 'FeederId',
                                                'Total through Kvar' : 'KVARTOT',
                                                'Total through KW' : 'KWTOT',
                                                'Balanced KVLN Voltage' : 'VLN',
                                                'KVLN voltage on phase A' : 'VLNA',
                                                'KVLN voltage on phase B' : 'VLNB',
                                                'KVLN voltage on phase C' : 'VLNC',
                                                'Balanced Pu line-to-neutral Voltage' : 'Vpu',
                                                'Pu line-to-neutral voltage on phase A' : 'VpuA',
                                                'Pu line-to-neutral voltage on phase B' : 'VpuB',
                                                'Pu line-to-neutral voltage on phase C' : 'VpuC',
                                                'Worst downstream under-voltage' : 'DwLowVoltWorst3PH',
                                                'Worst downstream over-voltage' : 'DwHighVoltWorst3PH',
                                                'Worst downstream over-voltage phase A' : 'DwHighVoltWorstA',
                                                'Worst downstream over-voltage phase B' : 'DwHighVoltWorstB',
                                                'Worst downstream over-voltage phase C' : 'DwHighVoltWorstC',
                                                'Worst downstream under-voltage phase A' : 'DwLowVoltWorstA',
                                                'Worst downstream under-voltage phase B' : 'DwLowVoltWorstB',
                                                'Worst downstream under-voltage phase C' : 'DwLowVoltWorstC',
                                                'Node Equipment Type' : 'NodeEqType',
                                                'Network Type' : 'NetworkType',
                                                'Latitude' : 'Latitude',
                                                'Longitude' : 'Longitude',
                                            },
                            'devices_arguments' : {
                                                'Feeder Id' : 'FeederId',
                                                'Total through Kvar' : 'KVARTOT',
                                                'Total through KW' : 'KWTOT',
                                                'Total spot load kW' : 'SpotKWT',
                                                'Distance': 'Distance',
                                                'Secondary base voltage' : 'XfoVBaseTo',
                                                'PV Initial Active Generation kW' : 'PVActiveGeneration',
                                                'overload' : 'OverloadAmpsMax',
                                                'Network type' : 'NetworkType',
                                                'Number of parallel cells' : 'PVParallelCells',
                                                'Splot Load Location' : 'SpotLocat',
                                                'Phase type' : 'PhaseType',
                                                'Number of series cells' : 'PVSeriesCells',
                                                'Total spot load customers' : 'SpotConsT',
                                                'Spot load status' : 'SpotStatus',
                                                'Spot load type' : 'SpotType',
                                                'Total spot load consumption kWh' : 'SpotCKWHT',
                                                'Voltage at maximum power point' : 'PVVmpp',
                                                'Spot load year' : 'SpotYear',
                                                'PV Rated Power kW' : 'PVRatedPower',
                                                'Spot load type list' : 'SpotTypeList',
                                                'Total number of customers' : 'TotalCons' 
                                            },
                            'sections_arguments' : {
                                                'From Node Id' : 'FromNodeID',
                                                'To Node Id' : 'ToNodeID',
                                                'Phase': 'Phase'
                                            }

        }

        self.results = {    'node_results' : pd.DataFrame(columns=['Distance', 'Section Id', 'Feeder Id', 'Total through Kvar', 'Total through KW', 'Balanced KVLN Voltage', 'KVLN voltage on phase A', 'KVLN voltage on phase B', 'KVLN voltage on phase C', 'Balanced Pu line-to-neutral Voltage', 'Pu line-to-neutral voltage on phase A', 'Pu line-to-neutral voltage on phase B', 'Pu line-to-neutral voltage on phase C', 'Worst downstream under-voltage', 'Worst downstream over-voltage', 'Worst downstream over-voltage phase A', 'Worst downstream over-voltage phase B', 'Worst downstream over-voltage phase C', 'Worst downstream under-voltage phase A', 'Worst downstream under-voltage phase B', 'Worst downstream under-voltage phase C', 'Node Equipment Type', 'Network Type', 'Latitude', 'Longitude']),
                            'devices_results' : pd.DataFrame(columns=['Feeder Id', 'Total through Kvar', 'Total through KW', 'Total spot load kW', 'Distance', 'Secondary base voltage', 'PV Initial Active Generation kW', 'overload', 'Network type', 'Number of parallel cells', 'Splot Load Location', 'Phase type', 'Number of series cells', 'Total spot load customers', 'Spot load status', 'Spot load type', 'Total spot load consumption kWh', 'Voltage at maximum power point', 'Spot load year', 'PV Rated Power kW', 'Spot load type list', 'Total number of customers']),
                            'sections_results' : pd.DataFrame(columns= ['From Node Id', 'To Node Id', 'Phase']),
                            'feeders_results' : pd.DataFrame(columns= ['Feeder Id', 'Substation Id']),
                            'other_results' : {'add_pvs': add_pvs,
                                'add_pvqs': add_pvqs,
                                'add_evs': add_evs,
                                'scada': [],
                                'pv_generations': [],
                                'pvq_generations': [],
                                'ev_demands': [],
                                'pv_node_voltages': [],
                                'pvq_node_voltages': [],
                                'ev_node_voltages': [],
                                'total_p_measured': [],
                                'total_q_measured': [],
                                'high_voltages': [],
                                'low_voltages': [],
                                'times': []}
                        }       

        self.source_node = source_node

    def save(self, time, substation, scada, pv_generations,
             pvq_generations, ev_demands):
        # Get time and SCADA
        self.results['other_results']['times'].append(time.strftime("%Y-%m-%d %H:%M:%S"))
        self.results['other_results']['scada'].append(scada)

        # Get voltage at each node where we have connected a device
        if pv_generations:
            self.results['other_results']['pv_node_voltages'].append(
                substation.get_voltage_from_node_ids(
                    self.results['other_results']['add_pvs']['node_ids']))
        if pvq_generations:
            self.results['other_results']['pvq_node_voltages'].append(
                substation.get_voltage_from_node_ids(
                    self.results['other_results']['add_pvqs']['node_ids']))
        if ev_demands:
            self.results['other_results']['ev_node_voltages'].append(
                substation.get_voltage_from_node_ids(
                    self.results['other_results']['add_evs']['node_ids']))

        # Get active and reactive power at each device
        self.results['other_results']['pv_generations'].append(pv_generations)
        self.results['other_results']['pvq_generations'].append(pvq_generations)
        self.results['other_results']['ev_demands'].append(ev_demands)

        # Get Worst voltage conditions through CYME
        source_node = self.source_node  # TODO: add substation.get_source_node() 'SOURCE_2405BK1'
        high = ({info: substation.get_info_node(source_node, info)
          for info in ['DwHighVoltWorstA', 'DwHighVoltWorstB', 'DwHighVoltWorstC']})
        low = ({info: substation.get_info_node(source_node, info)
          for info in ['DwLowVoltWorstA', 'DwLowVoltWorstB', 'DwLowVoltWorstC']})
        self.results['other_results']['high_voltages'].append(high)
        self.results['other_results']['low_voltages'].append(low)

        # Get P and Q at the source node
        self.results['other_results']['total_p_measured'].append(substation.get_info_node(source_node, 'KWTOT'))
        self.results['other_results']['total_q_measured'].append(substation.get_info_node(source_node, 'KVARTOT'))


        # Get all node results
        nodes = substation.list_nodes_extensive(properties=self.arguments['nodes_arguments'])
        devices = substation.list_devices(properties=self.arguments['devices_arguments'])
        sections = substation.list_sections(properties=self.arguments['sections_arguments'])
        feeders = substation.list_networks()

        timestamp_list = [time] * len(nodes)
        nodes['timestamp'] = pd.Series(timestamp_list)
        timestamp_list = [time] * len(devices)
        devices['timestamp'] = pd.Series(timestamp_list)
        timestamp_list = [time] * len(sections)
        sections['timestamp'] = pd.Series(timestamp_list)
        timestamp_list = [time] * len(feeders)
        feeders['timestamp'] = pd.Series(timestamp_list)

        self.results['node_results'] = self.results['node_results'].append(nodes, ignore_index=True)
        self.results['devices_results'] = self.results['devices_results'].append(devices, ignore_index=True)
        self.results['sections_results'] = self.results['sections_results'].append(sections, ignore_index=True)
        self.results['feeders_results'] = self.results['feeders_results'].append(feeders, ignore_index=True)



