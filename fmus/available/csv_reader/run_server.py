from flask import Flask, request
import os
import socket
import pandas

app = Flask(__name__)

@app.route('/dostep/<time>&<inputnames>&<inputvalues>&<outputnames>')
def step(time, inputnames, inputvalues, outputnames):
    data = _parse_url(time, inputnames, inputvalues, outputnames)
    outputs = []
    outputs.append(df.loc[int(data['time']), df.columns[int(data['column'])]])
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

@app.route('/shutdown')
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'

@app.errorhandler(Exception)
def handle_error(e):
    """
    Handle error message back to the FMU
    """
    return 'ERROR: ' + str(e)

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

    # Create a variable to hold the CSV file
    absolute_path = ('/Users/mygreencar/v2_git/fmi-for-power-system/' +
                     'fmus/available/csv_reader/')
    df = pandas.read_csv(absolute_path + 'data.csv', index_col=0)

    # Start the server
    app.run(port=port, debug=True, use_reloader=False)
