import json
import requests
import argparse
import ndjson
import sys


headers = {'Content-Type': 'application/json', 'kbn-xsrf': 'true'}

parser = argparse.ArgumentParser()
parser.add_argument("-name",   help="name of index to refresh", default=None)
parser.add_argument("-check",  help="only show", action="store_true")
args = parser.parse_args()

def update_index(id, name, fields):
  url = f'http://localhost:5601/api/saved_objects/index-pattern/{id}'
  print(url)
  data = f'{{"attributes":{{"title":"{name}","fields":"{fields}"}}}}'
  print(data)
  resp = requests.put(url=url, headers = headers, data = data)
  data = resp.json()
  return data
  
def get_fields(name):
  url = 'http://localhost:5601/api/index_patterns/_fields_for_wildcard'
  params = dict(
    pattern = name,
    meta_fields = '["_source","_id","_type","_index","_score"]'
  )
  resp = requests.get(url=url, params=params)
  data = resp.json()
  print(json.dumps(data['fields']))
  sys.exit(0)
  return data['fields']

def find_id_for_name(name):
  url = f'http://localhost:5601/api/saved_objects/_find'
  params = dict(
    type='index-pattern'
  )
  resp = requests.get(url=url, params=params)
  data = resp.json()
  for obj in data['saved_objects']:
    if (obj['attributes']['title'] == name):
      return obj['id']
  return None


id = None
if args.name:
  id = find_id_for_name(args.name)

if id is None:
  print("Index pattern not found")
  sys.exit()

fields = get_fields(args.name)

if args.check:
  print(json.dumps(fields, indent=2))
  sys.exit(0)

update_index(id, args.name, fields)

