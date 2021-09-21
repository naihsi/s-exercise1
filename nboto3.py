import boto3
import botocore.exceptions
import time


def fetch_instances():
    ec2 = boto3.resource('ec2')
    # select the running instances only
    # use tag: recycle_policy = auto to fetch the instances to check and terminate
    _filters = [
      {'Name': 'instance-state-name', 'Values': ['running']},
      {'Name': 'tag:branch_name', 'Values': ['dev_*']},
    ]
    for row in ec2.instances.filter(Filters=_filters):
        _branch_name = ""
        for one in row.tags:
            if one['Key'] == 'branch_name':
                _branch_name = one['Value']
        yield {
          'instance_id': row.instance_id,
          'branch_name': _branch_name,
        }


def terminate_instances(instance_ids):
    _client = boto3.client('ec2')
    # DryRun to claify if the permission is good to go
    try:
        _client.terminate_instances(InstanceIds=instance_ids, DryRun=True)
    except botocore.exceptions.ClientError as err:
        if err.response['Error']['Code'] == 'UnauthorizedOperation':
            print("failed to DryRun terminate instances")
            return None
        elif err.response['Error']['Code'] == 'DryRunOperation':
            print("DryRun for terminating instances passed")

    # do the termination
    _response = _client.terminate_instances(InstanceIds=instance_ids, DryRun=False)
    if _response["ResponseMetadata"]["HTTPStatusCode"] != 200:
        print("response is not 200: {}".format (_response["ResponseMetadata"]["HTTPStatusCode"]))
        return None

    # wait for all instances are terminated correctly
    wait_for_terminated(instance_ids)


def wait_for_terminated(instance_ids):
    wait_for_state(instance_ids, "terminated")


def wait_for_running(instance_ids):
    wait_for_state(instance_ids, "running")


def wait_for_state(instance_ids, wanted_state):
    ec2 = boto3.resource('ec2')
    _filters = [
      {'Name': 'instance-state-name', 'Values': [wanted_state]},
      {'Name': 'tag:branch_name', 'Values': ['dev_*']},
    ]

    # checking until all instances are terminated
    _ids = instance_ids.copy()
    while len(_ids) != 0:
        time.sleep(5)
        print("checking state for {}: {}".format(wanted_state, _ids))
        for row in ec2.instances.filter(Filters=_filters):
            if row.instance_id in _ids:
                print("{} {}".format(row.instance_id, wanted_state))
                _ids.remove(row.instance_id)


def create_instance(branch_name):
    _ami_image_id = "ami-087c17d1fe0178315"
    _instance_type = "t2.micro"
    _tags = [
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': "env: {}".format(branch_name)
                },
                {
                    'Key': 'branch_name',
                    'Value': branch_name
                },
            ]
        },
    ],
    _client = boto3.client('ec2')
    try:
        _response = _client.run_instances(ImageId=_ami_image_id, MinCount=1, MaxCount=1,
                                          InstanceType=_instance_type,
                                          TagSpecifications=_tags[0], 
                                          DryRun=True)
    except botocore.exceptions.ClientError as err:
        if err.response['Error']['Code'] == 'UnauthorizedOperation':
            print("failed to DryRun terminate instances")
            return None
        elif err.response['Error']['Code'] == 'DryRunOperation':
            print("DryRun for creating instances passed")
    
    _response = _client.run_instances(ImageId=_ami_image_id, MinCount=1, MaxCount=1,
                                      InstanceType=_instance_type,
                                      TagSpecifications=_tags[0])
    _instance_id = _response["Instances"][0]["InstanceId"]
    print("the instace to launch for {}: {}".format(branch_name, _instance_id))
    wait_for_running([_instance_id])


##### ##### ##### #####
# for testing

def test():
    _branch_name = "dev_1"
    create_instance(_branch_name)
    return 0
    terminate_instances(['i-0681deb87361053dc', 'i-0d61305a8adc0593c'])
    return 0
    for row in fetch_instances():
        print(row["instance_id"])
        print(row["branch_name"])


if __name__ == "__main__":
    test()
