import json
import requests
import argparse
import ndjson
import sys

# -list -type <type>    dashboard, visualization
# -export -type <type> [-id <id>]
# -import 

headers = {'Content-Type': 'application/json', 'kbn-xsrf': 'true'}

def print_aligned(data):
  widths = [max(map(len, col)) for col in zip(*data)]
  for row in data:
    print ("  ".join((val.ljust(width) for val, width in zip(row, widths))))

def print_pretty(data):
  if args.json:
    print(json.dumps(data, indent=2))
  else:
    print(ndjson.dumps(data))

def append_unique(data, obj):
  for el in data:
    if el['id'] == obj['id']:
      return
  data.append(obj)

parser = argparse.ArgumentParser()
parser.add_argument("-list",   help="list objects", action="store_true")
parser.add_argument("-i",      help="import objects", action="store_true")
parser.add_argument("-export", help="export objects", action="store_true")
parser.add_argument("-type",   help="type for export or list", default=None)
parser.add_argument("-id",     help="id for export or list", default=None)
parser.add_argument("-all",    help="export all referenced objects as well", action="store_true")
parser.add_argument("-json",   help="output pretty json instead of ndjson", action="store_true")

args = parser.parse_args()

def export_objects_recurse(data, type, id=None):
  url = f'http://localhost:5601/api/saved_objects/_export'
  if id is None:
    params = {
      'type' : type
    }
  else:
    params = { 
      'objects' : [ 
        { 'type' : type, 'id': id }
      ]
    }
  resp = requests.post(
    url=url, 
    json=json.dumps(params),
    headers=headers
  )
  objs = ndjson.loads(resp.text)
  for obj in objs:
    if args.all:
      for ref in obj['references']:
        export_objects_recurse(data, ref['type'], ref['id'])
    append_unique(data, obj)
  return


if args.list:
  url = f'http://localhost:5601/api/saved_objects/_find'
  params = dict(
    type=args.type
  )
  resp = requests.get(url=url, params=params)
  data = resp.json()
  
  output = [['ID', 'Type', 'Title']]
  for obj in data['saved_objects']:
    output.append([ obj['id'], obj['type'], obj['attributes']['title']])
  print_aligned(output)

if args.export:
  if args.type is None:
    print("You must specify a type using -type")
    sys.exit()
  data = []
  if args.id:
    export_objects_recurse(data,args.type, args.id)
  else:
    export_objects_recurse(data,args.type)

  print_pretty(data)

if args.i:
  print("Import")


