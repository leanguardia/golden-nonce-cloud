import boto3

class Sqs(object):
  def __init__(self):
    self.tasks_queue_url = 'https://sqs.us-east-1.amazonaws.com/398055134224/nonce-search-tasks.fifo'
    self.stop_search_queue_url  = 'https://sqs.us-east-1.amazonaws.com/398055134224/stop-search.fifo'
    self.client = boto3.client('sqs')

  def create_task(self, data, difficulty, search_range):
    search_from, search_to = search_range
    response = self.client.send_message(
    QueueUrl=self.tasks_queue_url,
    MessageBody=(f"Diff {difficulty}: {search_from} - {search_to}"),
    MessageAttributes={
        'Data': {
            'DataType': 'String',
            'StringValue': data
        },
        'Difficulty': {
            'DataType': 'Number',
            'StringValue': str(difficulty)
        },
        'SearchFrom': {
            'DataType': 'Number',
            'StringValue': str(search_from)
        },
        'SearchTo': {
            'DataType': 'Number',
            'StringValue': str(search_to)
        }
    },
    MessageGroupId=("UniqueID")
  )

  def next_task(self, max_retries=9):
    message = None
    attempt_num = 1
    while(not message and attempt_num <= max_retries):
      if attempt_num > 1: print("Receive Message Attempt:", attempt_num)
      response = self.client.receive_message(
        QueueUrl=self.tasks_queue_url,
        AttributeNames=['All'],
        MaxNumberOfMessages=1,
        MessageAttributeNames=['All'],
        WaitTimeSeconds=1,
      )
      if 'Messages' in response: message = response['Messages'][0]
      attempt_num += 1
    return self.__build_task(response['Messages'][0]) if message else False

  def complete_task(self, task):
    response = self.client.delete_message(
      QueueUrl=self.tasks_queue_url,
      ReceiptHandle=task['ReceiptHandle']
    )

  def purge_all(self):
    print("--> Purging Queues")
    self.client.purge_queue(QueueUrl=self.tasks_queue_url)
    self.client.purge_queue(QueueUrl=self.stop_search_queue_url)

  def stop_search(self, max_retries=3):
    message = None
    attempt_num = 1
    while(not message and attempt_num <= max_retries):
      if attempt_num > 1: print("Receive Message Attempt:", attempt_num)
      response = self.client.receive_message(
        QueueUrl=self.stop_search_queue_url,
        AttributeNames=['All'],
        MaxNumberOfMessages=1,
        MessageAttributeNames=['All'],
        WaitTimeSeconds=1,
      )
      if 'Messages' in response: message = response['Messages'][0]
      attempt_num += 1
    return message

  def publish_golden_nonce(self, nonce, binary_sequence):
    response = self.client.send_message(
      QueueUrl=self.stop_search_queue_url,
      MessageBody=(f"Golden {nonce}: {binary_sequence}|({len(binary_sequence)})"),
      MessageAttributes={
          'Nonce': {
              'DataType': 'Number',
              'StringValue': str(nonce)
          },
          'BinarySequence': {
              'DataType': 'String',
              'StringValue': str(binary_sequence)
          },
      },
      MessageGroupId=("UniqueID")
    )

  def __build_task(self, message):
    attributes = message['MessageAttributes']
    return {
      'Body': message['Body'],
      'SearchFrom': int(attributes['SearchFrom']['StringValue']),
      'SearchTo': int(attributes['SearchTo']['StringValue']),
      'Difficulty': int(attributes['Difficulty']['StringValue']),
      'Data': attributes['Data']['StringValue'],
      'ReceiptHandle': message['ReceiptHandle'],
    }

if __name__ == "__main__":
  # data = "CLOUDSMSlalala"
  # difficulty = 3
  sqs = Sqs()

  # batch_size = 100
  # num_of_tasks = 100

  # for task_index in range(num_of_tasks):
  #   search_from = task_index * batch_size
  #   search_to = search_from + batch_size - 1
  #   sqs.create_task(data, difficulty, (search_from, search_to))

  # task = sqs.next_task()
  # print(task)
  
  # sqs.complete_task(task)

  # sqs.nonce_found(39, "00010101010")
  
  # sqs.stop_search()
  sqs.purge_all()