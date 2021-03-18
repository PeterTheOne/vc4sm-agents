import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import base64
import json

# todo: don't do insecure requests
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# inspired by https://github.com/krakenh2020/EduPilotDeployment1/blob/main/demoA.py
agent_url = 'https://localhost:8092'  # aka. agent 2

print('Check connection...')
r = requests.get(agent_url + '/connections', verify=False)
if r.status_code != 200:
    print('Connection down :(')
    exit()
print('Connection works!')

invitationBase64 = input('Paste invite here: ')
invitationBytes = base64.b64decode(invitationBase64)
invitationStr = invitationBytes.decode('utf-8')
invitation = json.loads(invitationStr)
print(invitation)


print('Receive invite')
connection = requests.post(
    agent_url +
    '/connections/receive-invitation',
    json=invitation['invitation'],
    verify=False).json()

print(connection)
connectionId = connection['connection_id']
print(connectionId)

print('List connections')
details = requests.get(
    agent_url +
    '/connections/' +
    connectionId,
    verify=False)
print('Details last invite: ' + details.text)


print('Accept invite')
details = requests.post(
    agent_url +
    '/connections/' +
    connectionId +
    '/accept-invitation',
    verify=False)
print('Details accept invite: ' + details.text)

print('List accepted connection')

details = requests.get(
    agent_url +
    '/connections/' +
    connectionId,
    verify=False)
print('connection: ' + str(details.json()['result']))
print('MyDID:    ' + str(details.json()['result']['MyDID']))
print('TheirDID: ' + str(details.json()['result']['TheirDID']))
