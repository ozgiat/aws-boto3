#!/usr/bin/python3
import boto3
region_list = ['ap-southeast-1', 'ap-southeast-2', 'eu-central-1', 'us-west-2']

for region in region_list:

    client = boto3.client('ec2', region_name=region)
    response = client.describe_snapshots(OwnerIds=[owner_id])
    snapshots={}
    for snapshot in response['Snapshots']:
        snapshots_size = 0
        if 'ami' not in snapshot['Description']:
            snapshots[snapshot['SnapshotId']] = str(snapshot['VolumeSize'])
            snapshots_size = snapshots_size + snapshot['VolumeSize']

            snapshot = client.create_tags(
                Resources=[
                    snapshot['SnapshotId']
                ],
                Tags=[
                    {
                        'Key':'Usage',
                        'Value':'Not In Use'
                    }
                ]
            )
