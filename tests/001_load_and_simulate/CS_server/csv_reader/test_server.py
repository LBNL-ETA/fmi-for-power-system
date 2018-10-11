import requests
from datetime import datetime

with open('server_config.txt') as config:
    line = config.readline().split(':')

address = line[1]
port = line[3]

# Valid request on ping/
print('')
print('Valid request')
url = 'http://' + address + ':' + port + '/ping'
url += ''
print(url)
start_time = datetime.now()
response = requests.get(url)
time_elapsed = datetime.now() - start_time
print(response.content)
print('Time elapsed (hh:mm:ss.ms) {}'.format(time_elapsed))
print('')

# Valid request on initialize/
print('')
print('Valid request')
url = 'http://' + address + ':' + port + '/initialize/'
url += '_configurationFileName&'
path = ('C:\\Users\\DRRC\\Desktop\\fmi-for-power-system\\tests'+
        '\\001_load_and_simulate\\csv_reader\\data.csv').replace("\\", '%')
url += path
print(url)
start_time = datetime.now()
response = requests.get(url)
time_elapsed = datetime.now() - start_time
print(response.content)
print('Time elapsed (hh:mm:ss.ms) {}'.format(time_elapsed))
print('')

# Valid request dostep/
print('')
print('Valid request')
url = 'http://' + address + ':' + port + '/dostep/'
url += '1&column&0&output'
print(url)
start_time = datetime.now()
response = requests.get(url)
time_elapsed = datetime.now() - start_time
print(response.content)
print('Time elapsed (hh:mm:ss.ms) {}'.format(time_elapsed))
print('')


# Wrong request: time is a string
print('')
print('Wrong request: index is out of bound')
url = 'http://' + address + ':' + port + '/dostep/'
url += '1&column&100&output'
print(url)
response = requests.get(url)
print(response.content)
print('')
