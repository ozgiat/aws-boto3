#!/usr/bin/python3
import boto3
region_list = ['us-east-1', 'us-east-2', 'us-west-1', 'ap-south-1', 'eu-west-3', 'eu-north-1', 'eu-west-2', 'eu-west-1', 'ap-northeast-2', 'ap-northeast-1', 'sa-east-1', 'ca-central-1', 'ap-southeast-1', 'ap-southeast-2', 'eu-central-1', 'us-west-2']



for region in region_list:

    client = boto3.client('rds', region_name=region)
    response = client.describe_db_instances()
    RDS=[]

    for db in response['DBInstances']:        
        if db['DBInstanceStatus'] == 'not available':
            RDS.append(db['DBInstanceIdentifier'])
            db = client.create_tags(
                Resources=[
                    db['DBInstanceIdentifier']
                ],
                Tags=[
                    {
                        'Key':'Usage',
                        'Value':'Not In Use'
                    }
                ]
            )
            