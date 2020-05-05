#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# scripts needs the restAPI to run live

import requests
import json

# initiates and loads flowshet
url = "http://127.0.0.1:5000/api/items/str"
payload = '{"fname":"ExampleAbsorber999","lname":"-"}'
headers = {'content-type': 'application/json'}
res = requests.put(url, data=payload, headers=headers)
# runs a simulation

url = "http://127.0.0.1:5000/api/items"
payload = '{"fname":"ExampleAbsorber999","lname":"-"}'
headers = {'content-type': 'application/json'}
res = requests.post(url, data=payload, headers=headers)

r = requests.get('http://127.0.0.1:5000/api/results/%7B%22pipe%22%3A%22P02%22%2C%22prop%22%3A%22press%22%7D')

dict_obj = json.loads(r.content.decode())
# pipe = dict_obj['pipe']
property = dict_obj['lname']  # property
value = dict_obj['fname']  # value
