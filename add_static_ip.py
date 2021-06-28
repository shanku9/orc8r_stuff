#!/usr/bin/env python3
import requests
import json


# Subscriber IP Template

json_str = """
{
  "id": "IMSI001011234561000",
  "lte": {
    "auth_algo": "MILENAGE",
    "auth_key": "i69HPy+P0JSHzMvXCXxoYg==",
    "auth_opc": "jie2rw5pLnUPMmZ6OxRgXQ==",
    "state": "ACTIVE",
    "sub_profile": "default"
  },
  "name": "user_61000", 
  "static_ips": {
    "fbinternal": "10.22.145.0" 
  },
  "active_apns": [
    "fbinternal"
  ]
}
"""

headers = {"accept": "application/json", "content-type": "application/json"}

# API End Point
base_url = f"https://api.ens.fbmagma.ninja/magma/v1/lte/multi_apn/subscribers/"

# Place Holders for cert and keys
# Generate from pfx
cert = "ninja_new.crt"
key = "ninja_new_nopwd.key"

res = {}
dict = json.loads(json_str)
# IP IMSI Gen
for i in range(501):  # Number of Users
    if i < 256:
        ip = "10.22.145." + str(i)
    elif i > 255:
        ip = "10.22.146." + str(i - 256)

    # Prepend zeros
    sub = str(i).zfill(3)

    new_id = "IMSI001011234561" + sub
    new_name = "user_61" + sub

    dict["id"] = new_id
    dict["name"] = new_name
    dict["static_ips"]["fbinternal"] = ip
    new_js = json.dumps(dict)

    payload = new_js

    new_url = base_url + new_id
    # Debug
    # print(new_url, new_js)

    # Send Request
    response = requests.request(
        "PUT", new_url, headers=headers, data=payload, verify=False, cert=(cert, key)
    )
    if response:
        res[new_id] = "Added"
    else:
        res[new_id] = "Check"

# Capture output in file
list_of_string = [f"{key} : {res[key]}" for key in res]
with open("res_static.txt", "a") as f:
    [f.write(f"{st}\n") for st in list_of_string]
