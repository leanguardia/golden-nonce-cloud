import boto3
import logging
from botocore.exceptions import ClientError

def create_ec2_instance(ec2, image_id, instance_type, keypair_name):
  try:
    response = ec2.run_instances(ImageId=image_id,
                                 InstanceType=instance_type,
                                 KeyName=keypair_name,
                                 SecurityGroups=['launch-wizard-1'],
                                 MinCount=1,
                                 MaxCount=1)
  except ClientError as e:
    logging.error(e)
    return None
  return response['Instances'][0]

def stop_ec2_instance(ec2, instance_id):
  try:
    response = ec2.stop_instances(InstanceIds=[instance_id], DryRun=True)
    print(response)
  except ClientError as e:
    if 'DryRunOperation' not in str(e):
      raise
  # Dry run succeeded, call stop_instances without dryrun
  try:
    response = ec2.stop_instances(InstanceIds=[instance_id], DryRun=False)
    print(response)
  except ClientError as e:
    print(e)

def restart_ec2_instance(ec2, instance_id):
  try: ec2.start_instances(InstanceIds=[instance_id], DryRun=True)
  except ClientError as e:
    if 'DryRunOperation' not in str(e):
      raise

  # Dry run succeeded, run start_instances without dryrun
  try:
    response = ec2.start_instances(InstanceIds=[instance_id], DryRun=False)
    print(response)
  except ClientError as e:
    print(e)

# def terminate_ec2_instance(ec2, instance_id): # TODO

if __name__ == '__main__':
  ec2 = boto3.client('ec2')

  # response = ec2.describe_instances()
  # print(response)

  logging.basicConfig(level=logging.DEBUG,
                      format='%(levelname)s: %(asctime)s: %(message)s')
  
  # Starting and instance
  # image_id = 'ami-00dc79254d0461090' # Amazon Linux 2 AMI
  # instance_type = 't2.micro'
  # keypair_name = 'aws-macbook13'

  # instance_info = create_ec2_instance(ec2, image_id, instance_type, keypair_name)
  # instance_id = instance_info["InstanceId"]
  # if instance_info is not None:
  #     logging.info(f'Launched EC2 Instance {instance_info["InstanceId"]}')
  #     logging.info(f'    VPC ID: {instance_info["VpcId"]}')
  #     logging.info(f'    Private IP Address: {instance_info["PrivateIpAddress"]}')
  #     logging.info(f'    Current State: {instance_info["State"]["Name"]}')

  stop_ec2_instance(ec2, "i-0b8dc6583cd7eb0c9")
  # restart_ec2_instance(ec2, "i-00de005777c21e700")
```