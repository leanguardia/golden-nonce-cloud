import boto3
import logging
from botocore.exceptions import ClientError

class VirtualMachine(object):

  @classmethod
  def run_machines(klass, number):
    ec2 = boto3.client('ec2')
    response = ec2.run_instances(
      LaunchTemplate = {'LaunchTemplateId': 'lt-0244253c92f5a11c0'},
      MinCount = number,
      MaxCount = number,
      # Placement = {'AvailabilityZone': 'US East (N. Virginia)'}
    )
    print(response)
    return response

  # def stop_ec2_instance(ec2, instance_id):
  #   try:
  #     response = ec2.stop_instances(InstanceIds=[instance_id], DryRun=True)
  #     print(response)
  #   except ClientError as e:
  #     if 'DryRunOperation' not in str(e):
  #       raise
  #   # Dry run succeeded, call stop_instances without dryrun
  #   try:
  #     response = ec2.stop_instances(InstanceIds=[instance_id], DryRun=False)
  #     print(response)
  #   except ClientError as e:
  #     print(e)

if __name__ == '__main__':
  # ec2 = boto3.client('ec2')

  response = VirtualMachine().run_machines(1)

  # response = ec2.describe_instances()
  # print(response)

  # logging.basicConfig(level=logging.DEBUG,
  #                     format='%(levelname)s: %(asctime)s: %(message)s')
  
  # Starting and instance
  # image_id = 'ami-0b9d1c9679a45115c'

  # instance_info = create_ec2_instance(ec2, image_id, instance_type, keypair_name)
  # instance_id = instance_info["InstanceId"]
  # if instance_info is not None:
  #     logging.info(f'Launched EC2 Instance {instance_info["InstanceId"]}')
  #     logging.info(f'    VPC ID: {instance_info["VpcId"]}')
  #     logging.info(f'    Private IP Address: {instance_info["PrivateIpAddress"]}')
  #     logging.info(f'    Current State: {instance_info["State"]["Name"]}')

  # stop_ec2_instance(ec2, "i-0b8dc6583cd7eb0c9")
  # restart_ec2_instance(ec2, "i-00de005777c21e700")

  ## aws = AwsClient()
  ## start_broker()
  ## start_workers()

  ## Enter loop of crazines
