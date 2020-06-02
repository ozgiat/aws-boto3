#!/usr/bin/python3
import boto3
region_list = ['us-east-1', 'us-east-2', 'us-west-1', 'ap-south-1', 'eu-west-3', 'eu-north-1', 'eu-west-2', 'eu-west-1', 'ap-northeast-2', 'ap-northeast-1', 'sa-east-1', 'ca-central-1', 'ap-southeast-1', 'ap-southeast-2', 'eu-central-1', 'us-west-2']



for region in region_list:

    client = boto3.client('ec2', region_name=region)
    response = client.describe_addresses()
    eips=[]
    for address in response['Addresses']:
        if 'InstanceId' not in address:
            eips.append(address['PublicIp'])
            #print (eips[-1])
            address = client.create_tags(
                Resources=[
                    address['AllocationId']
                ],
                Tags=[
                    {
                        'Key':'Usage',
                        'Value':'Not In Use'
                    }
                ]
            )
