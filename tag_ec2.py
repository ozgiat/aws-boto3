#!/usr/bin/python3
import boto3
import os
region_list = ['us-east-2','us-east-1', 'us-east-2', 'us-west-1', 'ap-south-1', 'eu-west-3', 'eu-north-1', 'eu-west-2', 'eu-west-1', 'ap-northeast-2', 'ap-northeast-1', 'sa-east-1', 'ca-central-1', 'ap-southeast-1', 'ap-southeast-2', 'eu-central-1', 'us-west-2']


for region in region_list:
    print(region)
    client = boto3.client('ec2', region_name=region)
    response = client.describe_instances()
    
    for i in response['Reservations']:
        for instance in i['Instances']:
            if instance['State']['Name'] == 'stopped':
                print(instance['InstanceId'])


            

