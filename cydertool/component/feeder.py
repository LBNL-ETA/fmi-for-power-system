try:
    import cympy
except:
    pass
import pandas
import uuid
import time


class Cyme(object):
    """"""
    def __init__(self, model_filename):
        """"""
        # Open the model
        self.model_filename = model_filename
        cympy.study.Open(self.model_filename)

    def baseload_allocation(self, feeder_loads):
        """Allocate load with respect to the total demand recorded"""
        # Create Load Allocation object
        la = cympy.sim.LoadAllocation()

        for feeder in list(feeder_loads.keys()):
            # Create the Demand object
            demand = cympy.sim.Meter()
            demand.LoadValueType = cympy.enums.LoadValueType.KW_KVAR

            # Fill in the demand values
            demand.IsTotalDemand = False
            demand.DemandA = cympy.sim.LoadValue()
            demand.DemandA.Value1 = feeder_loads[feeder]['MW'] * 1000 / 3.0
            demand.DemandA.Value2 = feeder_loads[feeder]['MVAR'] * 1000 / 3.0
            demand.DemandB = cympy.sim.LoadValue()
            demand.DemandB.Value1 = feeder_loads[feeder]['MW'] * 1000 / 3.0
            demand.DemandB.Value2 = feeder_loads[feeder]['MVAR'] * 1000 / 3.0
            demand.DemandC = cympy.sim.LoadValue()
            demand.DemandC.Value1 = feeder_loads[feeder]['MW'] * 1000 / 3.0
            demand.DemandC.Value2 = feeder_loads[feeder]['MVAR'] * 1000 / 3.0

            # Set the first feeders demand
            la.SetDemand(feeder, demand)

        # Run the load allocation
        la.Run(list(feeder_loads.keys()))

    def add_power_devices(self, node_ids, network_ids, device_ids):
        """"""
        # Add section with spot loads
        for node, network, device in zip(node_ids, network_ids, device_ids):
            new_section = cympy.study.AddSection('MYSECTION' + device,  # Section ID
                                                 network,  # Network ID
                                                 device,  # Load ID
                                                 cympy.enums.DeviceType.SpotLoad,
                                                 node,  # Node ID
                                                 str(uuid.uuid4()))


    def set_power_devices(self, device_ids, values, reactive=False):
        """"""
        # Get active load model
        activeLoadModel = cympy.study.GetActiveLoadModel()

        # Set active or reactive values
        if reactive:
            parameter = 'KVAR'
        else:
            parameter = 'KW'

        for device_id, value in zip(device_ids, values):
            # Get device
            device = cympy.study.GetDevice(device_id, cympy.enums.DeviceType.SpotLoad)

            # Get the number of phases for the device
            section = cympy.study.GetSection(device.SectionID)
            nb_phases = int(len(section.GetValue("Phase")))

            # Add load value divided by the number of phases
            for phase in range(0, nb_phases):
                cympy.study.SetValueDevice(float(value) / nb_phases,  # Load value
                    'CustomerLoads[0].CustomerLoadModels.Get(' +
                    str(activeLoadModel.ID) + ').' +  # Active load model (August)
                    'CustomerLoadValues[' + str(phase) +  # Phase
                    '].LoadValue.' + parameter,  # Parameter to set
                    device_id,  # Load ID
                    cympy.enums.DeviceType.SpotLoad)  # Load type

    def run_powerflow(self, feeders=None, run_all=False):
        """"""
        # Run the power flow
        lf = cympy.sim.LoadFlow()
        if run_all:
            lf.Run()
        else:
            lf.Run(list(feeders))

    def list_networks(self):
        """"""
        networks = cympy.study.ListNetworks()
        return networks

    def list_nodes(self):
        """List all the nodes
        Return:
            a DataFrame with section_id, node_id, latitude and longitude
        """

        # Get all nodes
        nodes = cympy.study.ListNodes()

        # Create a frame
        nodes = pandas.DataFrame(nodes, columns=['node_object'])
        nodes['node_id'] = nodes['node_object'].apply(lambda x: x.ID)

        nodes['section_id'] = [0] * len(nodes)
        nodes['network_id'] = [0] * len(nodes)
        nodes['latitude'] = [0] * len(nodes)
        nodes['longitude'] = [0] * len(nodes)
        nodes['distance'] = [0] * len(nodes)

        for node in nodes.itertuples():
            nodes.loc[node.Index, 'section_id'] = cympy.study.QueryInfoNode("SectionId", node.node_id)
            nodes.loc[node.Index, 'latitude'] = cympy.study.QueryInfoNode("CoordY", node.node_id)
            nodes.loc[node.Index, 'longitude'] = cympy.study.QueryInfoNode("CoordX", node.node_id)
            nodes.loc[node.Index, 'distance'] = cympy.study.QueryInfoNode("Distance", node.node_id)
            nodes.loc[node.Index, 'network_id'] = cympy.study.QueryInfoNode("NetworkId", node.node_id)

        # Cast the right type
        for column in ['latitude']:
            nodes[column] = nodes[column].apply(lambda x: None if x is '' else float(x) / (1.26 * 100000))

        # Cast the right type
        for column in ['longitude']:
            nodes[column] = nodes[column].apply(lambda x: None if x is '' else float(x) / (100000))

        # Cast the right type
        for column in ['distance']:
            nodes[column] = nodes[column].apply(lambda x: None if x is '' else float(x))
        return nodes


    def get_voltage(self, frame):
        """
        Args:
            devices (DataFrame): list of all the devices or nodes to include
        Return:
            devices_voltage (DataFrame): devices and their corresponding voltage for
                each phase
        """
        # Create a new frame to hold the results
        voltage = frame.copy()

        # Reset or create new columns to hold the result
        voltage['voltage_A'] = [0] * len(voltage)
        voltage['voltage_B'] = [0] * len(voltage)
        voltage['voltage_C'] = [0] * len(voltage)

        for value in frame.itertuples():
            # Get the according voltage per phase in a pandas dataframe
            voltage.loc[value.Index, 'voltage_A'] = cympy.study.QueryInfoNode("VpuA", value.node_id)
            voltage.loc[value.Index, 'voltage_B'] = cympy.study.QueryInfoNode("VpuB", value.node_id)
            voltage.loc[value.Index, 'voltage_C'] = cympy.study.QueryInfoNode("VpuC", value.node_id)

        # Cast the right type
        for column in ['voltage_A', 'voltage_B', 'voltage_C']:
            voltage[column] = voltage[column].apply(lambda x: None if x is '' else float(x))
        return voltage


    def get_voltage_from_node_ids(self, node_ids):
        """
        Args:
            node_ids (List): node ids
        Return:
            node_voltage (List)

        TODO: use a comprhension list!!
        """
        voltages = []
        for node_id in node_ids:
            voltages.append(cympy.study.QueryInfoNode("Vpu", node_id))
        return voltages


    def get_info_node(self, node, info):
        """"""
        return cympy.study.QueryInfoNode(info, node)

    def get_info_device(self, device, info, device_type):
        """"""
        return cympy.study.QueryInfoDevice(info, device, int(device_type))

    def get_info_section(self, section, info):
        return cympy.study.GetValueSection(info, section)

    def list_networks(self, properties={}):
        """
            List all the feeders

            Args:
                properties (list): list of properties to retrieve for each feeder
                values(list): list of values to retrieve for each feeder
            Returns:
                a DataFrame
        """

        # Get all networks
        networks = cympy.study.ListNetworks()
        networks.sort(key = lambda v:len(v))
        substation = networks.pop(0)
        # Create a frame
        networks = pandas.DataFrame(networks, columns=['feeder_id'])

        if properties:
            networks = get_networks_properties(networks, properties)

        networks['Substation Id'] = [substation] * len(networks)

        return networks


    def list_nodes_extensive(self, properties={}):
        """
            List all the nodes

            Args:
                properties (list): list of properties to retrieve for each node
                values(list): list of values to retrieve for each node
            Returns:
                a DataFrame with section_id, node_id and any other picked properties
        """

        # Get all nodes
        nodes = cympy.study.ListNodes()

        # Create a frame
        nodes = pandas.DataFrame(nodes, columns=['node_object'])

        nodes['node_id'] = nodes['node_object'].apply(lambda x: x.ID)

        if properties:
            nodes = self.get_nodes_properties(nodes, properties)

        return nodes


    def list_devices(self, device_type=False, properties={}, values={}):
        """
            List all devices and return a break down of their type

            Args:
                device_type (Device): if passed then list of device with the same type
                verbose (Boolean): if True print result (default True)

            Return:
                DataFrame <device, device_type, device_number, device_type_id>
        """

        # Get the list of devices
        if device_type:
            devices = cympy.study.ListDevices(device_type)
        else:
            # Get all devices
            devices = cympy.study.ListDevices()

        # Create a dataframe
        devices = pandas.DataFrame(devices, columns=['device'])
        devices['device_type_id'] = devices['device'].apply(lambda x: x.DeviceType)
        devices['device_number'] = devices['device'].apply(lambda x: x.DeviceNumber)
        devices['device_sectionid'] = devices['device'].apply(lambda x: x.SectionID)
        devices['network_id'] = devices['device'].apply(lambda x: x.NetworkID)
        # devices['device_type'] = cympy.enums.DeviceType[cympy.enums.DeviceType == devices['device_type_id']].Name

        if properties:
            devices = self.get_devices_properties(devices, properties)

        if values:
            devices = self.get_devices_values(devices, values)

        return devices


    def list_sections(self, properties={}):
        """
            List all the sections

            Args:
                properties (list): list of properties to retrieve for each section
                values(list): list of values to retrieve for each section
            Returns:
                a DataFrame
        """

        # Get all sections
        sections = cympy.study.ListSections()

        # Create a frame
        sections = pandas.DataFrame(sections, columns=['section_object'])
        sections['section_id'] = sections['section_object'].apply(lambda x: x.ID)
        sections['length'] = sections['section_object'].apply(lambda x: x.Length)
        sections['from_node'] = sections['section_object'].apply(lambda x: x.FromNode.ID)
        sections['to_node'] = sections['section_object'].apply(lambda x: x.ToNode.ID)
        sections['network_id'] = [0] * len(sections)

        for section in sections.itertuples():
            sections.loc[section.Index, 'network_id'] = cympy.study.QueryInfoNode(
                "NetworkId", section.from_node)

        if properties:
            sections = self.get_sections_properties(sections, properties)

        return sections



    def get_nodes_properties(self, nodes, properties_names):
        """
        """
        nodes_ids_list = nodes['node_id'].tolist()
        for property_name, cymdist_keyword in properties_names.items():
            list_property = [0] * len(nodes_ids_list)
            for index in range(len(nodes_ids_list)):
                node_id = nodes_ids_list[index]
                list_property[index] = cympy.study.QueryInfoNode(
                    cymdist_keyword, node_id)
            nodes[property_name] = pandas.Series(list_property)
        return nodes


    def get_devices_properties(self, devices, properties_names):
        """
        """
        devices_ids_list = devices['device_number'].tolist()
        devices_type_ids_list = devices['device_type_id'].tolist()
        for property_name, cymdist_name in properties_names.items():
            list_property = [0] * len(devices_ids_list)
            for index in range(len(devices_ids_list)):
                device_id = devices_ids_list[index]
                device_type_id = devices_type_ids_list[index]
                list_property[index] = cympy.study.QueryInfoDevice(
                    cymdist_name, device_id, int(device_type_id))
            devices[property_name] = pd.Series(list_property)
        return devices


    def get_devices_values(self, devices, values_names):
        """
        """
        temp_devices = devices.copy()
        for value_name, cymdist_name in values_names.items():
            temp_device[value_name] = [0] * len(temp_devices)
            for device in devices.itertuples():
                try:
                    temp_devices.loc[device.Index, value_name] = cympy.study.GetValueDevice(
                        cymdist_name, device.device_number, int(device.device_type_id))
                except:
                    temp_devices.loc[device.Index, value_name] = False
        temp_devices = self.cast_info_type(temp_devices)
        return temp_devices


    def get_sections_properties(self, sections, properties_names):
        """
        """
        sections_ids_list = sections['section_id'].tolist()
        for property_name, cymdist_keyword in properties_names.items():
            list_property = [0] * len(sections_ids_list)
            for index in range(len(sections_ids_list)):
                section_id = sections_ids_list[index]
                list_property[index] = cympy.study.GetValueSection(
                    cymdist_keyword, section_id)
            sections[property_name] = pd.Series(list_property)
        return sections


    def cast_info_type(self, properties):
        """
        """
        for column in properties:
            if column in ['latitude']:
                properties[column] = properties[column].apply(lambda x: None if x is '' else float(x) / (1.26 * 100000))
            elif column in ['longitude']:
                properties[column] = properties[column].apply(lambda x: None if x is '' else float(x) / (100000))
        return properties

    def export_mode_file(self, filepath):

                cympy.study.Save(filepath)
