# CND - Vergonzosamente Paralelizable

The proof of work step in the Blockchain is an embassasangly parallelizable process. CND facilitates this search with two Python3 implementations; a local synchronous local and parallizable remote in the cloud.

## Local Environment
### Simple Finder
It is required to specify the difficulty with the -d or --difficulty flags.
```
python app/simple_finder.py --difficulty 6
```
By default a block is built with data "COMSM0010cloud". This can be changed with the --a or --data flags.
```
python app/simple_finder.py --difficulty 6 --data <text>
```

## Cloud Environment

N workers are spun up in the cloud to split the big task. 

### Setup
- Install [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#installation).
- Athentication credentials [setup](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#configuration).

CND initializes N AWS EC2 instances to start the search process. It is neccessary to specify a IAM role to these virtual machines have the necessary credentials to access resources, the default EC2 role is "EMR_EC2_DefaultRole". Make sure you have that role setup or specify another using the following environmental variable.
```
export CND_IAM_PROFILE=EMR_EC2_DefaultRole
```

It is possibl to access a running workers terminal through a SSH connection. For this it is neccessary to specify the public key and security group associated with the AWS account, the security group should allow SSH inbound connections.
```
export CND_SECURITY_GROUP=<MySecurityGroupName>
export CND_KEY_NAME=<MyKeyName>
```

### Run Direct Specification
```
python cnd.py  -n <num_of_workers> -d <difficulty>
```


### Emergency Scram
Open a new terminal and execute
```
python scram.py
```
If the search process was stopped with a keyboard interruption (e.g. cmd+z), instances should be terminated manually through the AWS console. 

### How it works
1. Find or create queues.
   1. Task Queue: contains tasks consumed by the workers. Each task contains the difficulty and a range of 25000 nonces to be tested.
   2. Stop Queue: used to notify it there is a reason to stop the search.
2. Send 12 batches of 10 tasks each to the TasksQueue.
3. Spin up N remote workers.
4. Send 2 batches everytime the number of tasks available is less than 80.
5. Search stops when a message is found in StopQueue. The possible reasons are:
   1. Nonce Found.
   2. Emergency Scram.

### TearDown
After execution:
- SQS: After use, queues should be deleted manually.
- EC2: Verify that no instances are still running in the AWS console.
