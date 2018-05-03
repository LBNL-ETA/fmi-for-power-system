from flask import Flask
import os
import json
import socket

app = Flask(__name__)

@app.route('/dostep/<time>&<inputnames>&<inputvalues>&<outputnames>')
def step(time, inputnames, inputvalues, outputnames):
    data = _parse_url(time, inputnames, inputvalues, outputnames)
    outputs = [data['input1'] * data['time']
               for i in range(0, len(data['outputnames']))]
    return ','.join([str(output) for output in outputs])

def _parse_url(time, inputnames, inputvalues, outputnames):
    """
    Ensure that inputs has the right type
    """
    data = {str(key):float(value)
            for key, value in
            zip(inputnames.split(','), inputvalues.split(','))}
    data['time'] = float(time)
    data['outputnames'] = outputnames.split(',')
    return data

@app.errorhandler(Exception)
def handle_error(e):
    """
    Handle error message back to the FMU
    """
    return 'ERROR: ' + str(e)

if __name__ == '__main__':
    # Open the right port
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 0))  # Get a free port at random with '0'
    address, port = sock.getsockname()  # Retrieve the port and address
    sock.close()  # Close the socket and use the port with Flask

    # Write a file with port and address
    path_to_server = os.path.dirname(__file__)
    with open(path_to_server + "server_config.txt", "w") as config:
        config.write(address + ',' + str(port))

    # Start the server
    app.run(port=port, debug=True, use_reloader=False)
