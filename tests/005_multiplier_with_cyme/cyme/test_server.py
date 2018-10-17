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
        '\\003_simulate_with_cyme\\cyme\\configuration.json').replace("\\", '!')
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
url += '1&IEEE34NODES!828!KW,IEEE34NODES!836!KW&0,0&'
url += '828!Vpu,836!Vpu'
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
url += '3&IEEE34NODES!828!KW,IEEE34NODES!836!KW&0,0&'
url += '828!Vpu,836!Vpu'
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
url += '8&IEEE34NODES!828!KW,IEEE34NODES!836!KW&0,0&'
url += '828!Vpu,836!Vpu'
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
url += '8&IEEE34NODES!828!KW,IEEE34NODES!836!KW&100,100&'
url += '828!Vpu,836!Vpu'
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
url += '8&IEEE34NODES!828!KW,IEEE34NODES!836!KW&-100,-100&'
url += '828!Vpu,836!Vpu'
print(url)
start_time = datetime.now()
response = requests.get(url)
time_elapsed = datetime.now() - start_time
print(response.content)
print('Time elapsed (hh:mm:ss.ms) {}'.format(time_elapsed))
print('')

# Wrong request dostep/
print('')
print('Valid request')
url = 'http://' + address + ':' + port + '/dostep/'
url += '8&&&'
url += '828!Vpu,836!Vpu'
print(url)
start_time = datetime.now()
response = requests.get(url)
time_elapsed = datetime.now() - start_time
print(response.content)
print('Time elapsed (hh:mm:ss.ms) {}'.format(time_elapsed))
print('')