import boto3
import datetime
import time

class Sqs(object):
  def __init__(self):
    self.queue_url  = 'https://sqs.us-east-1.amazonaws.com/398055134224/stop-search.fifo'
    self.client = boto3.client('sqs', region_name="us-east-1")

  def delete_stop_message(self, receive_handle):
    self.client.delete_message(
      QueueUrl=self.queue_url,
      ReceiptHandle=receive_handle
    )

  def purge_stop_queue(self):
    self.client.purge_queue(QueueUrl=self.queue_url)

  def stop_search(self, max_retries=3):
    message = None
    attempt_num = 1
    while(not message and attempt_num <= max_retries):
      if attempt_num > 1: print("Receive Message Attempt (Stop):", attempt_num)
      response = self.client.receive_message(
        QueueUrl = self.queue_url,
        AttributeNames = ['All'],
        MaxNumberOfMessages = 1,
        MessageAttributeNames = ['All'],
        WaitTimeSeconds = 0,
      )
      if 'Messages' in response: message = response['Messages'][0]
      attempt_num += 1
    return self.__parse_stop_message(response['Messages'][0]) if message else False

  def send_golden_nonce(self, nonce, binary_sequence, hexdigest):
    self.__send_ten_times(
      self.__build_golden_nonce_message(nonce, binary_sequence, hexdigest)
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

  def __send_ten_times(self, message):
    response = self.client.send_message_batch(
      QueueUrl = self.queue_url,
      Entries = list(self.__make_unique(message, index) for index in range(10))
    )
    # print(response)

  def __build_golden_nonce_message(self, nonce, binary_sequence, hexdigest):
    return {
      'MessageBody': (f"Golden {nonce}: {binary_sequence}|({len(binary_sequence)})"),
      'MessageAttributes': {
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
      'MessageGroupId': ("UniqueID")
    }

  def __make_unique(self, message, identifier):
    copy = message.copy()
    copy['Id'] = str(identifier)
    copy['MessageBody'] += " " + str(datetime.datetime.now())
    return copy

  def __send_stop_message(self, message_body, message_attributes):
    return self.client.send_message(
      QueueUrl=self.queue_url,
      MessageBody=(message_body),
      MessageAttributes=message_attributes,
      MessageGroupId=("UniqueID"),
    )

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
  # print(task)

  sqs.send_golden_nonce(39, "00010101010", "000002341234sdfkjadlfjasdlfkj")
  # sqs.purge_all()
  
  # sqs.stop_search()

  # sqs.emergency_scram()
  