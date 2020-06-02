#!/usr/bin/python3
import boto3
import datetime

region_list = ['us-east-1', 'us-east-2', 'us-west-1', 'ap-south-1', 'eu-west-3', 'eu-north-1', 'eu-west-2', 'eu-west-1', 'ap-northeast-2', 'ap-northeast-1', 'sa-east-1', 'ca-central-1', 'ap-southeast-1', 'ap-southeast-2', 'eu-central-1', 'us-west-2']



for region in region_list:
    print()
    print("For region " + region + " the following are active reserved instances that are about to expire:")
    print('==========================================================================================')
    client = boto3.client('ec2', region_name=region)
    response = client.describe_reserved_instances()
    # print(response)
    ec2=[]
    for y in response['ReservedInstances']:
        if y['State'] == 'active':
            print("Reservation Id is: " + y['ReservedInstancesId'] )    
    



    
