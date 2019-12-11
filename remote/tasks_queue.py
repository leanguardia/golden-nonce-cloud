import boto3

class TasksQueue(object):
  def __init__(self):
    self.queue_url = 'https://sqs.us-east-1.amazonaws.com/398055134224/nonce-search-tasks.fifo'
    self.client = boto3.client('sqs', region_name="us-east-1")
    self.poll_retries_count = 0

  def send_ten_tasks(self, data, difficulty, batch_index, num_of_tests):
    messages = []
    task_index = batch_index * 10
    for index in range(task_index, task_index + 10):
      search_from = index * num_of_tests
      search_to = search_from + num_of_tests - 1
      messages.append(self.build_message(data, difficulty, index, search_from, search_to, batch_index))

    response = self.client.send_message_batch(QueueUrl = self.queue_url, Entries = messages)
    return response
  
  def approx_num_of_tasks(self):
    response = self.client.get_queue_attributes(
      QueueUrl=self.queue_url,
      AttributeNames=['ApproximateNumberOfMessages']
    )
    return int(response['Attributes']['ApproximateNumberOfMessages'])

  def poll_tasks(self, max_attempts=1, wait_time_seconds=0):
    messages = []
    attempt_num = 1
    while(not messages and attempt_num <= max_attempts):
      if attempt_num > 1: 
        self.poll_retries_count += 1
        print("Receive Message Attempt (Poll):", attempt_num)
      response = self.client.receive_message(
        QueueUrl = self.queue_url,
        AttributeNames = ['All'],
        MaxNumberOfMessages = 10,
        MessageAttributeNames = ['All'],
        WaitTimeSeconds = wait_time_seconds,
      )
      if 'Messages' in response:
        for message_info in response['Messages']:
          messages.append(self.__parse_task(message_info))
      attempt_num += 1
    return messages if messages else []

  def purge(self):
    self.client.purge_queue(QueueUrl=self.queue_url)

  def delete_message(self, receipt_handle):
    self.client.delete_message(QueueUrl=self.queue_url, ReceiptHandle=receipt_handle)

  def build_message(self, data, difficulty, index, search_from, search_to, batch_index):
    return {
      'Id': str(index),
      'MessageBody': f"D-{difficulty}: Search in {search_from} - {search_to}",
      'MessageAttributes': {
        'Data': {
          'StringValue': data,
          'DataType': 'String',
        },
        'Difficulty': {
            'StringValue': str(difficulty),
            'DataType': 'Number',
        },
        'SearchFrom': {
            'StringValue': str(search_from),
            'DataType': 'Number',
        },
        'SearchTo': {
            'StringValue': str(search_to),
            'DataType': 'Number',
        },
      },
      'MessageGroupId': str(batch_index),
    }

  def __parse_task(self, message):
    attributes = message['MessageAttributes']
    return {
      'Body': message['Body'],
      'ReceiptHandle': message['ReceiptHandle'],
      'SearchFrom': int(attributes['SearchFrom']['StringValue']),
      'SearchTo': int(attributes['SearchTo']['StringValue']),
      'Difficulty': int(attributes['Difficulty']['StringValue']),
      'Data': attributes['Data']['StringValue'],
    }

if __name__ == "__main__":
  data = "COMSM0010cloud"
  difficulty = 7
  task_queue = TasksQueue()

  batch_index = 0
  num_of_tasks = 10
  num_of_tests = 10000

  num_of_batches = int(num_of_tasks / 10)
  for index in range(num_of_batches):
    response = task_queue.send_ten_tasks(data, difficulty, batch_index, num_of_tests)
    batch_index += 1

  # tasks = task_queue.poll_tasks(max_attempts=3)
  # print("batch Index", batch_index)
  # # batch_index += num_of_batches

  # num_of_tasks = 10
  # num_of_batches = int(num_of_tasks / 10)
  # times = 3
  # while(times):
  #   for index in range(num_of_batches):
  #     response = task_queue.send_ten_tasks(data, difficulty, batch_index, num_of_tests)
  #     batch_index += 1
  #   print("batch Index", batch_index)
  #   times -= 1

  # print(response)