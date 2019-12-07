import boto3

class Sqs(object):
  def __init__(self):
    self.tasks_queue_url = 'https://sqs.us-east-1.amazonaws.com/398055134224/nonce-search-tasks.fifo'
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

  # def next_task(self):
  #   response = sqs.receive_message(
  #     QueueUrl=self.tasks_queue_url,
  #     AttributeNames=[
  #         'SentTimestamp'
  #     ],
  #     MaxNumberOfMessages=1,
  #     MessageAttributeNames=[
  #         'All'
  #     ],
  #     VisibilityTimeout=0,
  #     WaitTimeSeconds=0
  #   )
  #   message = response['Messages'][0]
  #   receipt_handle = message['ReceiptHandle']

  # def complete_task(self, message_id):
  #   sqs.delete_message(
  #       QueueUrl=tasks_queue_url,
  #       ReceiptHandle=receipt_handle
  #   )
  def purge_all(self):
    print("Purging Queues")
    self.client.purge_queue(QueueUrl=self.tasks_queue_url)


if __name__ == "__main__":
  data = "CLOUDSMSlalala"
  difficulty = 3
  sqs = Sqs()

  batch_size = 100
  num_of_tasks = 10

  for task_index in range(num_of_tasks):
    search_from = task_index * batch_size
    search_to = search_from + batch_size - 1
    sqs.create_task(data, difficulty, (search_from, search_to))

  # sqs.stop_search()
  # sqs.complete_task()
  # sqs.purge_all()