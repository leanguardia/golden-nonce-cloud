import boto3
import logging
from botocore.exceptions import ClientError

class ParallelWorker(object):

  def __init__(self, num_of_workers):
    self.num_of_workers = num_of_workers
    self.ec2 = boto3.client('ec2')
    self.instance_ids = []

  def run(self):
    print(f"Initializing {self.num_of_workers} workers")
    response = self.ec2.run_instances(
      LaunchTemplate = {'LaunchTemplateId': 'lt-0244253c92f5a11c0'},
      MinCount = self.num_of_workers,
      MaxCount = self.num_of_workers,
    )
    for machine_info in response["Instances"]:
      self.instance_ids.append(machine_info['InstanceId'])
    return self.instance_ids

  def status(self):
    reservations = self.ec2.describe_instances(
      Filters = [
        { 'Name': 'tag:Purpose', 'Values': ['Worker'] },
        { 'Name': 'instance-state-name', 'Values': ['running'] },
      ],
    )['Reservations']
    return reservations[0]['Instances'] if reservations else []

  def shutdown(self):
    print(f"Shutting-down instances {self.instance_ids}")
    return self.ec2.terminate_instances(InstanceIds=self.instance_ids)

if __name__ == '__main__':

  parallel_worker = ParallelWorker(num_of_workers=3)
  parallel_worker.run()
  statuses = parallel_worker.status()
  print(statuses)
  # parallel_worker.shutdown()
