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
        print(row.state["Name"])
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

    # do the termination
    _response = _client.terminate_instances(InstanceIds=instance_ids, DryRun=False)
    if _response["ResponseMetadata"]["HTTPStatusCode"] != 200:
        print("response is not 200: {}".format (_response["ResponseMetadata"]["HTTPStatusCode"]))
        return None

    # wait for all instances are terminated correctly
    wait_for_terminated(instance_ids)


def wait_for_terminated(instance_ids):
    ec2 = boto3.resource('ec2')
    _filters = [
      {'Name': 'instance-state-name', 'Values': ['terminated']},
      {'Name': 'tag:branch_name', 'Values': ['dev_*']},
    ]

    # checking until all instances are terminated
    _ids = instance_ids.copy()
    while len(_ids) != 0:
        print("checking termination: {}".format(_ids))
        for row in ec2.instances.filter(Filters=_filters):
            if row.instance_id in _ids:
                print("{} terminated".format(row.instance_id))
                _ids.remove(row.instance_id)
        time.sleep(2)


##### ##### ##### #####
# for testing

def test():
    terminate_instances(['i-0681deb87361053dc', 'i-0d61305a8adc0593c'])
    return 0
    for row in fetch_instances():
        print(row["instance_id"])
        print(row["branch_name"])


if __name__ == "__main__":
    test()
