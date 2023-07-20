import json
import requests
import os

from dotenv import load_dotenv
load_dotenv()

BIN = os.environ['BIN']
MASTERKEY = os.environ['MASTERKEY']
ACCESSKEY = os.environ['ACCESSKEY']

def read():
    url = f'https://api.jsonbin.io/v3/b/{BIN}/latest'
    headers = {
        'X-Master-Key': MASTERKEY,
        'X-Access-Key': ACCESSKEY
    }
    return json.loads(requests.get(url, headers=headers).content)['record']

def write(data):
    url = f'https://api.jsonbin.io/v3/b/{BIN}'
    headers = {
        'Content-Type': 'application/json',
        'X-Master-Key': MASTERKEY,
    }
    requests.put(url,headers=headers, json=data)