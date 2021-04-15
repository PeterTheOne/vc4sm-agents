import time
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

invitation = input('Paste invite here: ')
invitation = json.loads(invitation)
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


while True:

    print('Accept credential offer with request')

    offer_accepted = False

    while not offer_accepted:
        print('fetch offers...')

        r = requests.get(agent_url + '/issuecredential/actions', verify=False).json()

        for offer in r['actions']:
            print('credential offer: ' + str(offer))
            piid = offer['PIID']

            r_credofferaccept = requests.post(
                agent_url +
                '/issuecredential/' +
                piid +
                '/accept-offer',
                verify=False).json()
            print(r_credofferaccept)
            offer_accepted = True

        time.sleep(2)



    print('accept credential')

    cred_accepted = False

    while not cred_accepted:
        print('fetch creds...')

        r = requests.get(agent_url + '/issuecredential/actions', verify=False).json()

        label = "demo-credentials18"
        credlabel = {
            "names": [
                label
            ]
        }

        for offer in r['actions']:
            print('credential offer: ' + str(offer))
            piid = offer['PIID']

            r_credaccept = requests.post(
                agent_url + '/issuecredential/' + piid + '/accept-credential',
                json=credlabel,
                verify=False).json()
            print(r_credaccept)

            cred_accepted = True

        time.sleep(2)

    offer_accepted = False
    cred_accepted = False
