#!/usr/bin/env -S python3
import requests
import json
from prettytable import PrettyTable

# Your Cloudflare API credentials
API_TOKEN = "YOUR_TOKEN_HERE"
ACCOUNT_ID = "YOUR_ACCOUNT_ID_HERE"

# API endpoint
url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/gateway/rules"

# Request headers
headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}


# GET request to get all rules
try:
   response = requests.get(url, headers=headers)
except requests.exceptions.HTTPError as errh: 
    print("HTTP Error") 
    print(errh.args[0]) 


# Check the response
if response.status_code == 200:
    print('API Response OK')
else:
    print(f"Error: {response.status_code}")
    print(response.text)


# Print rules in pretty table
rules_table = PrettyTable(['Num', 'ID', 'Type', 'Name'])
i = 1

for x in response.json().get('result'):
   rules_table.add_row([i, x.get('id'), x.get('filters')[0], x.get('name')])
   i += 1

print('Current Rules:')
print(rules_table)


# Get rule to clone
val = input("Enter Rule Number to Clone: ")
   
cloned_rule = response.json()['result'][int(val)-1]
cloned_rule['precedence'] = cloned_rule['precedence'] + 1
cloned_rule['name'] = "Clone - " + cloned_rule['name']
cloned_rule['enabled'] = False


# Post request to create clone rule
try:
   response = requests.post(url, headers=headers, json=cloned_rule)
except requests.exceptions.HTTPError as errh: 
    print("HTTP Error") 
    print(errh.args[0]) 


# Print cloned rule in pretty table
if response.status_code == 200:
    x = response.json().get('result')
    cloned_table = PrettyTable(['Num', 'ID', 'Type', 'Name'])
    cloned_table.add_row([int(val)+1, x.get('id'), x.get('filters')[0], x.get('name')])
    print('')
    print('Cloned Rule Created:')
    print(cloned_table)
else:
    print(f"Error: {response.status_code}")
    print(response.text)
