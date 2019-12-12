# Vergonzosamente Paralelizable

## Local Environment
### Simple Finder

## Cloud Environment

### Setup
A specific ARN is needed to setup the credentials used by `boto3` in the instances. The default role used for EC2 is "EMR_EC2_DefaultRole". However, it should be verified that this exists and has the right permissions.
```
export CND_IAM_PROFILE=EMR_EC2_DefaultRole
```

Running workers can are acessible by SSH connections. For that it is required to setup a the name of a Public key associated with your AWS account and the name of a SecurtiyGroup that allows SSH inbound connections. 
```
export CND_SECURITY_GROUP=<MySecurityGroup>
export CND_KEY_NAME=<MyKeyName>
```

### Run Direct Specification
```
cd golden-nonce-cloud
python cnd.py -d <difficulty> -n <num_of_workers>
```
By default the CND works with "COMSM0010cloud" as the data parameter. It can be changed by adding a `-a` flag.
```
python cnd.py -d <difficulty> -n <num_of_workers> -a <my_data>
```

### Emergency Scram
```
cd golden-nonce-cloud
python cnd.py -d <difficulty> -n <num_of_workers>
```
By default the CND works with "COMSM0010cloud" as the data parameter. It can be changed by adding a `-a` flag.
```
python cnd.py -d <difficulty> -n <num_of_workers> -a <my_data>
```

### How it works
1. Find or create queues.
2. Send X initial tasks
3. Spin up N instances
4. Sends more messages when available messages in queue decrease (controled by a threshold).
5. Constantly verify if there is an stop message.

### TearDown
- SQS: After use, queues should be deleted manually.
- EC2: Nothing to do. All workers are shut-down after the searching loop.
