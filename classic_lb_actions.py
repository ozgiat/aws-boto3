import boto3
import time
import sys

elbName = input("ELB-Name?")

client = boto3.client('elbv2', 'us-east-1')
attachedInstances = []
response = client.describe_load_balancers(
    LoadBalancerNames=[
        elbName
    ]
)
#print(response)
def getELBstatus():
    print("Checking ELB Status..")
    for inst in response['LoadBalancerDescriptions']:
        print(inst)
        print("ALB : " + inst['DNSName'])
        for ec2Id in inst['Instances']:
            print(ec2Id)
            attachedinst = ec2Id['InstanceId']
            attachedInstances.append(attachedinst)
            print("Attached Instances : " + attachedinst)
            healthy = client.describe_instance_health(
                LoadBalancerName=elbName
            )
            print(healthy)
            for status in healthy['InstanceStates']:
                print("InstanceId : " + status['InstanceId'] + " " + "State : " + status['State'])
                while(status['State'] != 'InService'):
                    print("waiting for instance")


def detachInstancefromELB(instance):
    try:
        print("Detaching Instance: " + attachedInstances[0] + "from ELB")
        detach = client.deregister_instances_from_load_balancer(
            LoadBalancerName=elbName,
            Instances=[
                {
                'InstanceId':instance
                },
            ]
        )
    except ValueError as err:
        print(err.args)
        sys(exit(1))
    print(detach)

def attachInstancetoELB(instance):
    time.sleep(5)
    print("Attaching Instance: " + attachedInstances[0] + "to ELB")
    try:
        attach = client.register_instances_with_load_balancer(
            LoadBalancerName=elbName,
            Instances=[
                {
                    'InstanceId':instance
                },
            ]
        )
    except ValueError as err:
        print(err.args)
        sys(exit(1))
    healthy = client.describe_instance_health(
        LoadBalancerName=elbName,
    )
    # print(healthy)
    for status in healthy['InstanceStates']:
        print("InstanceId : " + status['InstanceId'] + " " + "State : " + status['State'])
        while (status['State'] != 'InService'):
            print("waiting for instance")

    print(attach)

getELBstatus()
#detachInstancefromELB(attachedInstances[0])
#attachInstancetoELB(attachedInstances[0])
#getELBstatus()