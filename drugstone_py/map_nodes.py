import requests
import json

def map_nodes():
    header= { 'Content-Type': 'application/json' }
    API = 'https://drugst.one/drugstone_api/'
    response = requests.post(API+'map_nodes/', headers=header, verify=False, data=json.dumps({'nodes': [{'id': "PTEN"}], 'identifier': "symbol"}))
    print(response.json())

map_nodes()