import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import base64
import json

# todo: don't do insecure requests
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# inspired by https://github.com/krakenh2020/EduPilotDeployment1/blob/main/demoA.py
agent_url = 'https://localhost:8082'  # aka. agent 1

print('Check connection...')
r = requests.get(agent_url + '/connections', verify=False)
if r.status_code != 200:
    print('Connection down :(')
    exit()
print('Connection works!')


print('List own invite again')

connections = requests.get(agent_url + '/connections', verify=False).json()
for connection in connections['results']:
    print('connection: ' + str(connection))
    connectionId = connection['ConnectionID']

    print('MyDID:    ' + str(connection['MyDID']))
    print('TheirDID: ' + str(connection['TheirDID']))


print('Get connection states')

details = requests.get(
    agent_url +
    '/connections/' +
    connectionId,
    verify=False)
print('connection: state = ' + str(details.json()['result']['State']))


print('Accept request')

details = requests.post(
    agent_url +
    '/connections/' +
    connectionId +
    '/accept-request',
    verify=False)
print('details accept invite: ' + details.text)
