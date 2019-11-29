# Vergonzosamente Paralelizable

## Local Environment - Celery & RabbitMQ
### Run a celery worker
celery -A async_finder worker -n=worker1 --loglevel=info

## Cloud Environment - Amazon Web Services
#### SSH to EC2 instance
`ssh -i ~/.ssh/aws-key.pem ec2-user@ec2-52-90-79-36.compute-1.amazonaws.com`

```
sudo yum update -y
sudo yum install python3 -y
sudo yum install git -y
sudo amazon-linux-extras install docker -y
sudo service docker start
```

#### Install Dependencies in Amazon Linux EC2 Instance
```
sudo yum update -y
sudo amazon-linux-extras install docker
sudo service docker start # run docker service
sudo usermod -a -G docker ec2-user # allow ec2-user to run docker without sudo
sudo yum install git -y # intall git
```

#### Some portions of the code have been taken from the following repository:
https://github.com/awsdocs/aws-doc-sdk-examples/tree/master/python/example_code
