import json
import os

folders = {}
with open('folders.json', 'r') as f:
    folders = json.load(f)

location = "programming"
if location in folders:
    command = '''open "%s"''' % (folders[location])
    os.system(command)
else:
    print("Doesn't seem to work")