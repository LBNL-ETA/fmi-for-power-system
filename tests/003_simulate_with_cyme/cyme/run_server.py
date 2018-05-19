from flask import Flask, request
import os
import socket
import json
import pandas
import cympy

app = Flask(__name__)
version = 'test cyme'

class Substation(object):
    def __init__(self):
        self.configuration = None
        self.first_iteration = None
        self.scada = None
        self.results = None

    # INITIALIZATION
    #################################################################
    def initialize_cyme(self, inputs):
        """
        Initialize the CYME FMU
        """
        # Open the configuration file and read the configurations
        with open(inputs['_configurationFileName'], 'r') as configuration_file:
            self.configuration = json.load(configuration_file)
        assert 'model_filename' in self.configuration, 'missing model_filename'
        assert 'total_load_filename' in self.configuration, ('missing ' +
            'total_load_filename')
        assert 'substation_network' in self.configuration, ('missing ' +
            'substation_network')

        # Open load allocation data [MW]
        self.scada = pandas.read_csv(
            self.configuration['total_load_filename'], index_col=0)

        # Create a list of all the feeder names
        self.feeders = list(set(
            [value.split('_')[0] for value in self.scada.columns]))
        if self.configuration['substation_network'] in self.feeders:
            self.substation_and_feeders = list(self.feeders)
        else:
            self.substation_and_feeders = list(self.feeders)
            self.substation_and_feeders.append(
                self.configuration['substation_network'])

        # Reset iteration count and results
        self.first_iteration = True
        self.results = []

        # Open model
        cympy.study.Open(self.configuration['model_filename'])
        return 'Initialization complete'

    # DOSTEP
    #################################################################
    def simulate_cyme(self, inputs):
        """
        Simulate the CYME FMU
        """
        # Parse inputs into categories
        voltages = {}
        loads = {}
        for name, value in inputs.items():
            if 'VMAG' in name:
                voltages[name] =  value
            elif 'KW' in name or 'KVAR' in name:
                loads[name] = value
            elif 'time' not in name and 'outputnames' not in name:
                raise Exception("Wrong input " + str(name))

        # If first iteration add load to the feeder model
        if self.first_iteration:
            self._add_load(
                node_ids=[name.split('!')[1] for name in loads.keys()],
                network_ids=[name.split('!')[0] for name in loads.keys()],
                device_ids=[name for name in loads.keys()])
            self.first_iteration = False

        # Set voltage at the feeder/substation head [V]
        if voltages:
            self._set_voltages(voltages, self.configuration['substation_network'])

        # Retrieve current feeder load
        # Load are expected in MW and converted to kW
        feeder_loads = {}
        index = self.scada.index[self.scada.index.get_loc(
                                    int(inputs['time']),
                                    method='nearest')]
        for feeder in self.feeders:
            feeder_loads[feeder] = (
                {'MW': self.scada.loc[index, feeder + '_MW'],
                 'MVAR': self.scada.loc[index, feeder + '_MVAR']})
        self._baseload_allocation(feeder_loads)

        # Set new values for the loads [kW or kVAR]
        self._set_load_power(device_ids=[name for name in loads.keys()],
                             values=[loads[name] for name in loads.keys()])

        # Run the power flow
        self._run_powerflow(self.substation_and_feeders)

        # Return the right outputs [units from CYME]
        return self._output_values(inputs['outputnames'])

    def _baseload_allocation(self, feeder_loads):
        # Allocate load with respect to the total demand recorded
        # Create Load Allocation object
        la = cympy.sim.LoadAllocation()

        for feeder in feeder_loads.keys():
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

    def _add_load(self, node_ids, network_ids, device_ids):
        # Add section with spot loads
        for node, network, device in zip(node_ids, network_ids, device_ids):
            new_section = cympy.study.AddSection(
                'SECTION' + device,  # Section ID
                network,  # Network ID
                device,  # Load ID
                cympy.enums.DeviceType.SpotLoad,
                node,  # Node ID
                'NEW_NODE_from' + node)

    def _set_voltages(self, inputs, network):
        # Set the voltage at the source node from transmission grid
        # Set up the right voltage in [kV] (input must be [V])
        cympy.study.SetValueTopo(voltages['VMAG_A'] / 1000,
            "Sources[0].EquivalentSourceModels[0]" +
            ".EquivalentSource.OperatingVoltage1", network)
        cympy.study.SetValueTopo(voltages['VMAG_B'] / 1000,
            "Sources[0].EquivalentSourceModels[0]" +
            ".EquivalentSource.OperatingVoltage2", network)
        cympy.study.SetValueTopo(voltages['VMAG_C'] / 1000,
            "Sources[0].EquivalentSourceModels[0]" +
            ".EquivalentSource.OperatingVoltage3", network)

    def _set_load_power(self, device_ids, values):
        # Get active load model
        activeLoadModel = cympy.study.GetActiveLoadModel()

        for device_id, value in zip(device_ids, values):
            # Get device
            device = cympy.study.GetDevice(
                device_id,
                cympy.enums.DeviceType.SpotLoad)

            # Get the number of phases for the device
            section = cympy.study.GetSection(device.SectionID)
            nb_phases = int(len(section.GetValue("Phase")))

            # Get load parameter to set
            if 'KW' in device_id:
                parameter = 'KW'
            elif 'KVAR' in device_id:
                parameter = 'KVAR'
            else:
                raise Exception('Device parameter is not supported: ' +
                                str(device_id))

            # Add load value divided by the number of phases
            for phase in range(0, nb_phases):
                cympy.study.SetValueDevice(
                    float(value) / nb_phases,  # Load value
                    'CustomerLoads[0].CustomerLoadModels.Get(' +
                    str(activeLoadModel.ID) + ').' +  # Active load model
                    'CustomerLoadValues[' + str(phase) +  # Phase
                    '].LoadValue.' + parameter,  # Parameter to set
                    device_id,  # Load ID
                    cympy.enums.DeviceType.SpotLoad)  # Load type

    def _run_powerflow(self, feeders):
        # Run the power flow
        lf = cympy.sim.LoadFlow()
        lf.Run(list(feeders))

    def _output_values(self, output_names):
        # Query the right output name at the source node
        output = []
        for name in output_names:
            node = name.split('!')[0]
            category = name.split('!')[1]
            temp = cympy.study.QueryInfoNode(category, node)
            output.append(float(temp))
        return output

# END POINTS
#################################################################
@app.route('/initialize/<parameter_names>&<parameter_values>')
def initialize(parameter_names, parameter_values):
    # Create a variable to hold the CSV file
    inputs = {str(key):str(value)
              for key, value in
              zip(parameter_names.split(','), parameter_values.split(','))}
    inputs['_configurationFileName'] = (
        inputs['_configurationFileName'].replace('!', '\\'))
    substation.initialize_cyme(inputs)
    return 'Server initialized'

@app.route('/dostep/<time>&<inputnames>&<inputvalues>&<outputnames>')
def step(time, inputnames, inputvalues, outputnames):
    #Ensure that inputs has the right type
    inputs = {str(key):float(value)
              for key, value in
              zip(inputnames.split(','), inputvalues.split(','))}
    inputs['time'] = float(time)
    inputs['outputnames'] = outputnames.split(',')
    outputs = substation.simulate_cyme(inputs)
    return ','.join([str(output) for output in outputs])

@app.route('/shutdown')
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'

@app.route('/ping')
def ping():
    return 'pinged'

# @app.errorhandler(Exception)
# def handle_error(e):
#     #Handle error message back to the FMU
#     return 'ERROR: ' + str(e)

# LAUNCH SERVER
#################################################################
if __name__ == '__main__':
    # Open the right port
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = 'localhost'
    sock.bind(('localhost', 0))  # Get a free port at random with '0'
    port = sock.getsockname()[1]  # Retrieve the port and address
    sock.close()  # Close the socket and use the port with Flask

    # Write a file with port and address
    path_to_server = os.path.dirname(__file__)
    with open(os.path.join(path_to_server, "server_config.txt"), "w") as config:
        config.write('address:' + address + ':port:' + str(port) + ':')

    # Create state variables
    substation = Substation()

    # Start the server
    app.run(port=port, debug=True, use_reloader=False)
