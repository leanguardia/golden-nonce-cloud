import boto3

class TasksQueue(object):
  def __init__(self):
    self.queue_url = 'https://sqs.us-east-1.amazonaws.com/398055134224/nonce-search-tasks.fifo'
    self.client = boto3.client('sqs', region_name="us-east-1")

  def send_tasks_batch(self, data, difficulty, task_index, num_of_tests):
    messages = []
    for index in range(task_index, task_index + 10):
      search_from = index * num_of_tests
      search_to = search_from + num_of_tests - 1
      print(search_from, search_to)
      messages.append(self.build_message(data, difficulty, index, search_from, search_to))

    response = self.client.send_message_batch(
      QueueUrl = self.queue_url,
      Entries = messages
    )
    return response

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
  # response = task_queue.send_tasks_batch(data, difficulty, 0, 100)
  # print(response)
  response = task_queue.send_tasks_batch(data, difficulty, 0, 10000)
  print(response)