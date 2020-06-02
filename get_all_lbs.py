import boto3

region_name = [
    'us-east-1',
    'us-west-2',
    'ca-central-1',
    'ap-southeast-2',
    'eu-west-1',
    'us-west-1',
    'eu-central-1'
]

for region in region_name:

    print('\n')
    print('######### The region is: ' + region + ' ##########')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

    ec2 = boto3.client('elbv2', region_name=region)
    ec2v2 = boto3.client('elbv2', region_name=region)

    def find_elb(client):

        resp = client.describe_load_balancers()
        # print(resp)

        for elb in resp['LoadBalancers']:
            print(elb['LoadBalancerName'], elb['DNSName'])


    find_elb(ec2)
    find_elb(ec2v2)
