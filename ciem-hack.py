import boto3

from datetime import datetime, timedelta, timezone
from pprint import pprint

from laceworksdk import LaceworkClient

lw = LaceworkClient()
aws = boto3.Session()


def get_start_end_times(hour_delta=1):
    current_time = datetime.now(timezone.utc)
    start_time = current_time - timedelta(hours=hour_delta)
    start_time = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_time = current_time.strftime("%Y-%m-%dT%H:%M:%SZ")

    return start_time, end_time


def get_raw_cloud_trail():

    start_time, end_time = get_start_end_times()

    result = lw.queries.execute(
        query_text="""{
            source {
                CloudTrailRawEvents
            }
            return distinct {
                INSERT_ID,
                INSERT_TIME,
                EVENT_TIME,
                EVENT
            }
        }""",
        arguments={
            "StartTimeRange": start_time,
            "EndTimeRange": end_time,
        }
    )

    return result


def get_services_by_role(json_data):

    roles = {}

    for event in json_data['data']:
        identity_arn = event['EVENT'].get('userIdentity', {}).get('arn', None)
        if identity_arn:
            if identity_arn not in roles.keys():
                roles[identity_arn] = set([event['EVENT']['eventSource']])
            else:
                roles[identity_arn].add(event['EVENT']['eventSource'])

    pprint(roles)

    return roles


def list_all_roles():
    iam = aws.client('iam')
    paginator = iam.get_paginator('list_roles')
    responses = paginator.paginate()

    for response in responses:
        for role in response['Roles']:
            print(role['RoleName'])


if __name__ == '__main__':

    json_data = get_raw_cloud_trail()
    get_services_by_role(json_data)
    list_all_roles()

    # TODO scope what data fields we want/need from raw data
    # TODO get all AWS services via CLI/API
    # TODO create a "diff" on used roles
