import boto3, time, os

class ParallelWorker(object):
  def __init__(self, num_of_workers):
    self.num_of_workers = num_of_workers
    self.ec2 = boto3.client('ec2')
    self.key_name = os.environ.get('CND_KEY_NAME')
    self.security_group = os.environ.get('CND_SECURITY_GROUP')
    self.iam_profile = os.environ.get('CND_IAM_PROFILE')
    self.instance_ids = []

  def run(self):
    print(f"Initializing {self.num_of_workers} worker(s)")
    print("KeyName:", self.key_name, " - SecurityGroup:", self.security_group, " - IAM Profile:", self.iam_profile)
    response = self.ec2.run_instances(
      ImageId = 'ami-015dd0c2828bf03ff',
      InstanceType = 't2.micro',
      MinCount = self.num_of_workers,
      MaxCount = self.num_of_workers,
      UserData = open("remote/worker-boot.txt").read(),
      KeyName = self.key_name,
      SecurityGroups = [self.security_group],
      IamInstanceProfile = { 'Name': self.iam_profile },
    )
    for machine_info in response["Instances"]:
      self.instance_ids.append(machine_info['InstanceId'])
    print(self.instance_ids)
    return self.instance_ids

  def status(self):
    reservations = self.ec2.describe_instances(
      InstanceIds=self.instance_ids,
    )['Reservations']
    if reservations[0]: statuses = self.__parse_statuses(reservations)
    return statuses if statuses else []

  def wait_initialization(self, min_instances_running=1, timeout=600):
    print(f"Waiting until at least {min_instances_running} worker(s) starts running.")
    waiting = True; seconds = 0
    while(waiting and seconds < timeout):
      time.sleep(1); seconds +=1
      if seconds > 12 and all(state == 'running' for state in self.status()):
        waiting = False
      print('.', end='', flush=True)
    print('')
    if seconds == timeout: print('Initialization timeout!')

  def shutdown(self):
    print(f"Shutting-down instances {self.instance_ids}")
    return self.ec2.terminate_instances(InstanceIds=self.instance_ids)

  def __parse_statuses(self, reservations):
    statuses = []
    if reservations[0]:
      for instance_info in reservations[0]['Instances']:
        statuses.append(instance_info['State']['Name'])
    return statuses

if __name__ == '__main__':

  parallel_worker = ParallelWorker(num_of_workers=1)
  parallel_worker.run()
  # parallel_worker.wait_initialization()
  # parallel_worker.shutdown()
