import requests

with open('server_config.txt') as config:
    line = config.readline().split(':')

address = line[1]
port = line[3]

# Valid request
print('')
print('Valid request')
url = 'http://' + address + ':' + port + '/dostep/'
url += '1&parameter1,input1,input2&55,6,7&result1,result2'
print(url)
response = requests.get(url)
print(response.content)
print('')

# Wrong request: time is a string
print('')
print('Wrong request: time is a string')
url = 'http://' + address + ':' + port + '/dostep/'
url += 'cyder&parameter1,input1,input2&55,6,7&result1,result2'
print(url)
response = requests.get(url)
print(response.content)
print('')
