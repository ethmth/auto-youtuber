import sys
import json

varFile = open("/opt/src/current_values.var", "r")
lines = varFile.readlines()
varFile.close()

for line in lines:
    if line[0:line.index("=")] == "CLIENT_ID":
        client_id = line[(line.index("=") + 2):(line.index("\n") - 1)]
    if line[0:line.index("=")] == "CLIENT_SECRET":
        client_secret = line[(line.index("=") + 2):(line.index("\n") - 1)]


jsonFile = open("/opt/src/client_secrets.json", "r")
data = json.load(jsonFile)
jsonFile


localdata = data["web"]
localdata["client_id"] = client_id
localdata["client_secret"] = client_secret
data["web"] = localdata


jsonFile = open("/opt/src/client_secrets.json", "w")
json.dump(data, jsonFile)
jsonFile.close()