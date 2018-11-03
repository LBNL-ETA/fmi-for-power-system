from __future__ import print_function
from flask import Flask, request
import os
import socket
import sys

app = Flask(__name__)

@app.route('/initialize/<parameter_names>&<parameter_values>')
def initialize(parameter_names, parameter_values):
    # Create a variable to hold the CSV file
    return 'Server initialized'

@app.route('/dostep/<time>&<inputnames>&<inputvalues>&<outputnames>')
def step(time, inputnames, inputvalues, outputnames):
    inputs = _parse_url(time, inputnames, inputvalues, outputnames)
    outputs = []
    outputs.append(float(inputs['x']) + float(inputs['u']))
    outputs = [1.051]
    print('Output values: ' + str(outputs), file=sys.stderr)
    return ','.join([str(output) for output in outputs])

# Utility functions
#################################################################
def _parse_url(time, inputnames, inputvalues, outputnames):
    #Ensure that inputs has the right type
    data = {str(key):float(value)
            for key, value in
            zip(inputnames.split(','), inputvalues.split(','))}
    data['time'] = float(time)
    data['outputnames'] = outputnames.split(',')
    return data

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

@app.errorhandler(Exception)
def handle_error(e):
    #Handle error message back to the FMU
    return 'ERROR: ' + str(e)
#################################################################

if __name__ == '__main__':
    # Open the right port
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = 'localhost'
    sock.bind((address, 0))  # Get a free port at random with '0'
    port = sock.getsockname()[1]  # Retrieve the port and address
    sock.close()  # Close the socket and use the port with Flask

    # Write a file with port and address
    path_to_server = os.path.dirname(__file__)
    ping_server_code = """def main():
    import urllib2
    try:
        response = urllib2.urlopen("http://localhost:""" + str(port) + """/ping").read()
        response = response.decode('utf-8')
    except:
        response = 'bad request'
    if response in 'pinged':
        print('The Server is up')
        return 0
    else:
        print('The server is not up yet')
        return 1

if __name__ == '__main__':
    import sys
    sys.exit(main())
    """

    # Write a file which allows checking if the server is up
    with open(os.path.join(path_to_server, "check_server.py"), "w") as py_ping:
        py_ping.write(ping_server_code)

    # Write te configuration file for connecting to the server
    with open(os.path.join(path_to_server, "server_config.txt"), "w") as config:
        config.write('address:' + address + ':port:' + str(port) + ':')

    # Start the server
    app.run(port=port, debug=True, use_reloader=False)
