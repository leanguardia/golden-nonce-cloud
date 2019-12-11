import boto3
import datetime
import time

class StopQueue(object):
  def __init__(self):
    self.queue_url  = 'https://sqs.us-east-1.amazonaws.com/398055134224/stop-search.fifo'
    self.client = boto3.client('sqs', region_name="us-east-1")

  def approx_num_of_tasks(self):
    response = self.client.get_queue_attributes(
      QueueUrl=self.queue_url,
      AttributeNames=['ApproximateNumberOfMessages']
    )
    return int(response['Attributes']['ApproximateNumberOfMessages'])

  def purge(self):
    self.client.purge_queue(QueueUrl=self.queue_url)

  def delete_message(self, receipt_handle):
    self.client.delete_message(QueueUrl=self.queue_url, ReceiptHandle=receipt_handle)

  def poll_stop_message(self, max_attempts=1, wait_time_seconds=1):
    message = None
    attempt_num = 1
    while(not message and attempt_num <= max_attempts):
      if attempt_num > 1: print("Poll Stop message attempt:", attempt_num)
      response = self.client.receive_message(
        QueueUrl = self.queue_url,
        AttributeNames = ['All'],
        MaxNumberOfMessages = 1,
        MessageAttributeNames = ['All'],
        WaitTimeSeconds = wait_time_seconds,
      )
      if 'Messages' in response: message = response['Messages'][0]
      attempt_num += 1
    return self.__parse_stop_message(response['Messages'][0]) if message else False

  def send_golden_nonce(self, nonce, binary_sequence, hexdigest):
    self.__send_ten_times(
      self.__build_golden_nonce_message(nonce, binary_sequence, hexdigest)
    )

  def __send_ten_times(self, message):
    response = self.client.send_message_batch(
      QueueUrl = self.queue_url,
      Entries = list(self.__make_unique(message, index) for index in range(10))
    )

  def __build_golden_nonce_message(self, nonce, binary_sequence, hexdigest):
    return {
      'MessageBody': (f"Golden {nonce}: {binary_sequence}|({len(binary_sequence)})"),
      'MessageAttributes': {
          'StopReason': {
            'StringValue': "NonceFound", 'DataType': 'String',
          },
          'Nonce': {
            'StringValue': str(nonce), 'DataType': 'Number',
          },
          'BinarySequence': {
            'StringValue': str(binary_sequence), 'DataType': 'String',
          },
          'Hexdigest': {
            'StringValue': hexdigest, 'DataType': 'String',
          },
      },
      'MessageGroupId': ("UniqueID")
    }

  def __make_unique(self, message, identifier):
    copy = message.copy()
    copy['Id'] = str(identifier)
    copy['MessageBody'] += " " + str(datetime.datetime.now())
    return copy

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
  stop_queue = StopQueue()
  # print(stop_queue.approx_num_of_tasks())
  # stop_queue.purge()
  # stop_queue.send_golden_nonce(56, "00010101010", "000002341234sdfkjadlfjasdlfkj")
  # print(stop_queue.poll_stop_message(max_attempts=15, wait_time_seconds=0))

  # sqs.emergency_scram()