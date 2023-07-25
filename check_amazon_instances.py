import boto3

# create an EC2 client
ec2 = boto3.client('ec2')

# get information about instances associated with your account
response = ec2.describe_instances()

# check if there are any instances
if not response['Reservations']:
    print("There are no instances associated with your account.")
else:
    # print the instance information
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            print(instance['InstanceId'], instance['InstanceType'], instance['State']['Name'])