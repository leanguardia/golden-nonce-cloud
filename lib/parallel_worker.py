import boto3
import logging
from botocore.exceptions import ClientError

class ParallelWorker(object):

  def __init__(self, num_of_workers):
    self.num_of_workers = num_of_workers
    self.ec2 = boto3.client('ec2')
    self.identifiers = []

  def run(self):
    print(f"Initializing {self.num_of_workers} workers")
    response = self.ec2.run_instances(
      LaunchTemplate = {'LaunchTemplateId': 'lt-0244253c92f5a11c0'},
      MinCount = self.num_of_workers,
      MaxCount = self.num_of_workers,
    )
    for machine_info in response["Instances"]:
      self.identifiers.append(machine_info['InstanceId'])

  def status(self):
    response = self.ec2.describe_instances(
      Filters=[
        { 'Name': 'tag:Purpose', 'Values': ['Worker'] },
        { 'Name': 'instance-state-name', 'Values': ['running'] },
      ],
      # InstanceIds=self.identifiers,
      # IncludeAllInstances=Filters,
    )
    return response['Reservations'][0]['Instances']

  def shutdown(self):
    response = self.ec2.terminate_instances(InstanceIds=self.identifiers)

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

  parallel_worker = ParallelWorker(num_of_workers=2)
  # parallel_worker.run()
  statuses = parallel_worker.status()
  # parallel_worker.shutdown_workers()




