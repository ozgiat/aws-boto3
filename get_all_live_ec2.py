#!/usr/bin/python3
import boto3
import requests
import json
import sys
import csv

region_list = ['us-east-1', 'us-east-2', 'us-west-1', 'ap-south-1', 'eu-west-3', 'eu-north-1', 'eu-west-2', 'eu-west-1',
               'ap-northeast-2', 'ap-northeast-1', 'sa-east-1', 'ca-central-1', 'ap-southeast-1', 'ap-southeast-2',
               'eu-central-1', 'us-west-2']

accessible_dict = {}
inaccesible_dict = {}
strange_instances = []

for region in region_list:
    client = boto3.client('ec2', region_name=region)
    response = client.describe_instances()

    for r in response['Reservations']:
        for i in r['Instances']:
            inaccesible_private = True
            inaccesible_public = True
            try:
                for x in i['Tags']:
                    if x['Key'] == "Name":
                        instance_name = x['Value']
            except KeyError:
                print("--Cant find instance name")
                instance_name = i['PrivateIpAddress']

            if i['State']['Name'] == "running":
                if 'PrivateIpAddress' in i:
                    print(i['PrivateIpAddress'], instance_name)
                    try:
                        response = requests.get('http://' + i['PrivateIpAddress'] + ':9090/system/health', timeout=3)
                        if response.json()['status'] == "UP" or "DOWN":
                            print('success for instance name: ' + instance_name + ' with private')
                            accessible_dict[(i['PrivateIpAddress'])] = [instance_name]
                            break
                    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError, requests.exceptions.HTTPError, ValueError) as e:
                        print('connection timed out or connection error')
                        inaccesible_private = False
                        # inaccesible_dict[(i['PrivateIpAddress'])] = [instance_name]

                if 'PublicIpAddress' in i:
                    print(i['PublicIpAddress'], instance_name)
                    try:
                        response = requests.get('http://' + i['PublicIpAddress'] + ':9090/system/health', timeout=3)
                        if response.json()['status'] == "UP" or "DOWN":
                            print('success for instance name: ' + instance_name + ' with public')
                            accessible_dict[(i['PublicIpAddress'])] = [instance_name]
                            break
                    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError, requests.exceptions.HTTPError, ValueError) as e:
                        print('connection timed out or connection error')
                        inaccesible_public = False
                else:
                    print(instance_name)
                    strange_instances.append(instance_name)
                    break
                if not inaccesible_private and not inaccesible_public:
                    inaccesible_dict[(i['PrivateIpAddress'])] = [instance_name]

with open('accessible_services.csv', 'w') as f:
    for key in accessible_dict.keys():
        f.write("%s %s\n" % (key, accessible_dict[key]))

with open('inaccessible_services.csv', 'w') as f:
    for key in inaccesible_dict.keys():
        f.write("%s %s\n" % (key, inaccesible_dict[key]))

with open('strange_instances.txt', 'w') as f:
    for item in strange_instances:
        f.write("%s\n" % item)
