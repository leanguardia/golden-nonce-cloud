import boto3
import datetime

class Sqs(object):
  def __init__(self):
    self.tasks_queue_url = 'https://sqs.us-east-1.amazonaws.com/398055134224/nonce-search-tasks.fifo'
    self.stop_search_queue_url  = 'https://sqs.us-east-1.amazonaws.com/398055134224/stop-search.fifo'
    self.client = boto3.client('sqs', region_name="us-east-1")

  def send_task(self, data, difficulty, search_range):
    search_from, search_to = search_range
    response = self.client.send_message(
    QueueUrl=self.tasks_queue_url,
    MessageBody=(f"D-{difficulty}: Search in {search_from} - {search_to}"),
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

  def poll_task(self, max_retries=9):
    message = None
    attempt_num = 1
    while(not message and attempt_num <= max_retries):
      if attempt_num > 1: print("Receive Message Attempt (Poll):", attempt_num)
      response = self.client.receive_message(
        QueueUrl=self.tasks_queue_url,
        AttributeNames=['All'],
        MaxNumberOfMessages=1,
        MessageAttributeNames=['All'],
        WaitTimeSeconds=1,
      )
      if 'Messages' in response: message = response['Messages'][0]
      attempt_num += 1
    return self.__parse_task(response['Messages'][0]) if message else False

  def delete_task_message(self, receive_handle):
    self.client.delete_message(
      QueueUrl=self.tasks_queue_url,
      ReceiptHandle=receive_handle
    )

  def delete_stop_message(self, receive_handle):
    self.client.delete_message(
      QueueUrl=self.stop_search_queue_url,
      ReceiptHandle=receive_handle
    )

  def purge_all(self):
    self.purge_tasks_queue()
    self.purge_stop_queue()

  def purge_tasks_queue(self):
    self.client.purge_queue(QueueUrl=self.tasks_queue_url)

  def purge_stop_queue(self):
    self.client.purge_queue(QueueUrl=self.stop_search_queue_url)

  def stop_search(self, max_retries=3):
    message = None
    attempt_num = 1
    while(not message and attempt_num <= max_retries):
      if attempt_num > 1: print("Receive Message Attempt (Stop):", attempt_num)
      response = self.client.receive_message(
        QueueUrl=self.stop_search_queue_url,
        AttributeNames=['All'],
        MaxNumberOfMessages=1,
        MessageAttributeNames=['All'],
        WaitTimeSeconds=1,
      )
      if 'Messages' in response: message = response['Messages'][0]
      attempt_num += 1
    return self.__parse_stop_message(response['Messages'][0]) if message else False

  def publish_golden_nonce(self, nonce, binary_sequence, hexdigest):
    response = self.client.send_message(
      QueueUrl=self.stop_search_queue_url,
      MessageBody=(f"Golden {nonce}: {binary_sequence}|({len(binary_sequence)})"),
      MessageAttributes={
          'StopReason': {
            'DataType': 'String',
            'StringValue': "NonceFound"
          },
          'Nonce': {
            'DataType': 'Number',
            'StringValue': str(nonce)
          },
          'BinarySequence': {
            'DataType': 'String',
            'StringValue': str(binary_sequence)
          },
          'Hexdigest': {
            'DataType': 'String',
            'StringValue': hexdigest
          },
      },
      MessageGroupId=("UniqueID")
    )

  def emergency_scram(self):
    response = self.__send_stop_message(
      message_body=f"Emergency Scram, stoping all workers {datetime.datetime.now()}!",
      message_attributes={
        'StopReason': {
          'DataType': 'String',
          'StringValue': "EmergencyScram"
        },
      },
    )
  
  def approx_num_of_tasks(self):
    response = self.client.get_queue_attributes(
      QueueUrl=self.tasks_queue_url,
      AttributeNames=['ApproximateNumberOfMessages']
    )
    return int(response['Attributes']['ApproximateNumberOfMessages'])

  def __send_stop_message(self, message_body, message_attributes):
    return self.client.send_message(
      QueueUrl=self.stop_search_queue_url,
      MessageBody=(message_body),
      MessageAttributes=message_attributes,
      MessageGroupId=("UniqueID"),
    )

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

  def __parse_stop_message(self, message):
    attributes = message['MessageAttributes']
    stop_reason = attributes['StopReason']['StringValue']
    message = {
      'Body': message['Body'],
      'ReceiptHandle': message['ReceiptHandle'],
      'StopReason': stop_reason,
    }
    if stop_reason == "NonceFound":
      message['Nonce'] = int(attributes['Nonce']['StringValue'])
      message['BinarySequence'] = attributes['BinarySequence']['StringValue']
      message['Hexdigest'] = attributes['Hexdigest']['StringValue']
    return message

if __name__ == "__main__":
  # data = "CLOUDSMSlalala"
  # difficulty = 3
  sqs = Sqs()

  # batch_size = 10000
  # num_of_tasks = 100

  # for task_index in range(num_of_tasks):
  #   search_from = task_index * batch_size
  #   search_to = search_from + batch_size - 1
  #   sqs.create_task(data, difficulty, (search_from, search_to))

  # task = sqs.next_task()
  # print(task)
  
  # sqs.delete_task_message(task)

  # sqs.nonce_found(39, "00010101010")
  # sqs.purge_all()
  
  # sqs.stop_search()

  # sqs.emergency_scram()
  print(sqs.approx_num_of_tasks())
  