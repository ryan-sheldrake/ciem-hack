import json
import requests
from pprint import pprint as pprint


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


if __name__ == '__main__':
    token, lw_acc = get_bearer_token()
    #TODO get rawcloudtrail data via LQL query
    #TODO scope what data fileds we want/need from raw data
    #TODO parse all principle/roles
    #TODO get all AWS services via CLI/API

