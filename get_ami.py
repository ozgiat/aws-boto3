import boto3

region_name = [
    'eu-west-1',
    'us-west-2',
    'ca-central-1',
    'ap-southeast-2'
]

for region in region_name:

    print('\n')
    print('######### The region is: ' + region + ' ##########')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

    ec2 = boto3.client('ec2', region_name=region)

    resp = ec2.describe_images(Filters=[
        {'Name': 'owner-id', 'Values': ['675948241492']}])

    ami_list = []

    for ami in resp['Images']:
        ami_list.append(ami['ImageId'])

        print(ami['ImageId'], ami['Name'], ami['CreationDate'])
        # print(ami_list)
