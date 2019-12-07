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

  def next_task(self):
    response = self.client.receive_message(
      QueueUrl=self.tasks_queue_url,
      AttributeNames=['All'],
      MaxNumberOfMessages=1,
      MessageAttributeNames=['All'],
      WaitTimeSeconds=1
    )
    if not 'Messages' in response: print("-> NO MESSAGES!!!")
    return self.__build_task(response['Messages'][0])

  # def complete_task(self, message_id):
  #   sqs.delete_message(
  #       QueueUrl=tasks_queue_url,
  #       ReceiptHandle=receipt_handle
  #   )

  # def delete_task(receipt_handle):
  #   self.client()

  def purge_all(self):
    print("--> Purging Queues")
    self.client.purge_queue(QueueUrl=self.tasks_queue_url)

  def __build_task(self, message):
    attributes = message['MessageAttributes']
    # print(message['MessageAttributes'])
    print(message['MessageId'])
    return {
      'Body': message['Body'],
      'SearchFrom': attributes['SearchFrom']['StringValue'],
      'SearchTo': attributes['SearchTo']['StringValue'],
      'Difficulty': attributes['Difficulty']['StringValue'],
      'Data': attributes['Data']['StringValue'],
      'MessageID': message['MessageId'],
    }

if __name__ == "__main__":
  data = "CLOUDSMSlalala"
  difficulty = 3
  sqs = Sqs()

  batch_size = 100
  num_of_tasks = 10

  # for task_index in range(num_of_tasks):
  #   search_from = task_index * batch_size
  #   search_to = search_from + batch_size - 1
  #   sqs.create_task(data, difficulty, (search_from, search_to))

  task = sqs.next_task()
  print(task)

  print("Body", task["Body"])
  print("SearchFrom", task["SearchFrom"])
  print("SearchTo", task["SearchTo"])
  print("Difficulty", task["Difficulty"])
  print("Data", task["Data"])
  print("MessageId", task["MessageID"])
  # sps.delete_task(task)

  # sqs.stop_search()
  # sqs.complete_task()
  # sqs.purge_all()