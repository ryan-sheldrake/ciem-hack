import json
import requests
from pprint import pprint as pprint

import typing_extensions


def get_bearer_token():
    with open("/Users/ryansheldrake/.lacework-creds", "r") as f:
        content = f.readlines()
        lw_acc = (content[8]).strip()
        access_key = (content[9]).strip()
        secret = (content[10]).strip()
        the_url = 'https://' + str(lw_acc) + '.lacework.net/api/v1/access/tokens'

        #print(the_url)
        data = {
            "keyId": access_key,
            "expiryTime": 3600
        }
        headers = {
            "X-LW-UAKS": secret,
            "Content-Type": "application/json"
        }
        res = requests.post(the_url, json=data, headers=headers)
        json_data = json.loads(res.text)
        for i in (json_data['data']):
            token = (i['token'])
        return token, lw_acc


def get_raw_cloud_trail(token):
    ct_url = 'https://' + str(
        lw_acc) + ".lacework.net/api/v2/Queries/execute"
    headers = {"Authorization": "Bearer " + str(token).strip()
               }
    data = {
    "query": {
        "queryText": "ryan_ct_extract {source {CloudTrailRawEvents} return distinct {INSERT_ID,INSERT_TIME,EVENT_TIME,EVENT}}"
    },
    "arguments": [
        {
            "name": "StartTimeRange",
            "value": "2022-07-27T10:00:00.000Z"
        },
        {
            "name": "EndTimeRange",
            "value": "2022-07-27T11:00:00.000Z"
        }
    ]
    }
    res_lql = requests.post(ct_url, json=data, headers=headers)
    json_data = json.loads(res_lql.text)
    # pprint(json_data)
    return json_data


def get_roles(json_data):
    for event in json_data['data']:
        user_id_parms = event['EVENT']['userIdentity']
        if "arn" in user_id_parms.keys():
            print(user_id_parms['arn'])



if __name__ == '__main__':
    token, lw_acc = get_bearer_token()
    json_data = get_raw_cloud_trail(token)
    get_roles(json_data)
    #TODO get rawcloudtrail data via LQL query
    #TODO scope what data fileds we want/need from raw data
    #TODO parse all principle/roles
    #TODO get all AWS services via CLI/API

