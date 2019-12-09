import boto3

class TasksQueue(object):
  def __init__(self):
    self.queue_url = 'https://sqs.us-east-1.amazonaws.com/398055134224/nonce-search-tasks.fifo'
    self.client = boto3.client('sqs', region_name="us-east-1")

  def send_batch_of_ten(self, data, difficulty, task_index, num_of_tests):
    messages = []
    for index in range(task_index, task_index + 10):
      search_from = index * num_of_tests
      search_to = search_from + num_of_tests - 1
      print(search_from, search_to)
      messages.append(self.build_message(data, difficulty, index, search_from, search_to))

    # response = self.client.send_message_batch(
    #   QueueUrl = self.queue_url,
    #   Entries = messages
    # )
    # return response
  
  def approx_num_of_tasks(self):
    response = self.client.get_queue_attributes(
      QueueUrl=self.queue_url,
      AttributeNames=['ApproximateNumberOfMessages']
    )
    return int(response['Attributes']['ApproximateNumberOfMessages'])

  def build_message(self, data, difficulty, index, search_from, search_to):
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
      'MessageGroupId': 'UniqueID',
    }

if __name__ == "__main__":
  data = "COMSM0010cloud"
  difficulty = 7
  task_queue = TasksQueue()

  batch_index = 0
  task_index = 0
  num_of_tasks = 30
  num_of_tests = 100

  num_of_batches = int(num_of_tasks / 10)
  for index in range(num_of_batches):
    response = task_queue.send_batch_of_ten(data, difficulty, task_index, num_of_tests)
    task_index += 10
  # batch_index += num_of_batches

  num_of_tasks = 10
  num_of_batches = int(num_of_tasks / 10)
  print("jump")
  for index in range(num_of_batches):
    response = task_queue.send_batch_of_ten(data, difficulty, task_index, num_of_tests)
    task_index += 10
  # batch_index += num_of_batches
  print("jump")
  for index in range(num_of_batches):
    response = task_queue.send_batch_of_ten(data, difficulty, task_index, num_of_tests)
    task_index += 10
  # batch_index += num_of_batches
  print("jump")
  for index in range(num_of_batches):
    response = task_queue.send_batch_of_ten(data, difficulty, task_index, num_of_tests)
    task_index += 10
  # batch_index += num_of_batches

  # print(response)