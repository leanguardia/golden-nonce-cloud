# CND - Vergonzosamente Paralelizable

The Proof of Work step in Blockchain is an Embarrassingly Parallelizable process, CND facilitates the search of the Golden Nonce with a local implementation and in the Cloud.

## Local Environment
### Simple Finder
It is required to specify the difficulty with the `-d` or `--difficulty` flags.
```
python app/simple_finder.py --difficulty 6
```
By default a block is built with data `"COMSM0010cloud"`. This can be changed with the `-a` or `--data` flags.
```
python app/simple_finder.py --difficulty 6 --data <text>
```
By default the `Prepending Zeros` implementation is used.

## Cloud Environment
CND spins up N workers in the cloud to split the overall tasks in smaller and parallelizable ones. 

### Setup
- Install [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#installation).
- Setup [AWS Athentication](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#configuration) credentials.

It is neccessary to specify a IAM role for the virtual machines to be assigned the requires credentials to access other AWS resources. The default ARN for this is `EMR_EC2_DefaultRole` every AWS account comes with it by default. However, make sure you have that role setup or specify another one by setting the following environmental variable.
```
export CND_IAM_PROFILE=MY_EC2_Role
```

### Run Direct Specification
```
python cnd.py -d <difficulty> -n <num_of_workers>
```

### Emergency Scram
In order to stop a search in progress, open a new terminal and execute:
```
python scram.py
```
If the search finished by a message found in the `StopQueue` all instances should be cleanly terminated. In unexpected cases such as search search interrupted by keyboard (e.g. cmd + z), instances should be terminated manually through the AWS console.
