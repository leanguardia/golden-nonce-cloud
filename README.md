### Where is the nonce? :S

## Local Environment - Celery & RabbitMQ
# Run a celery worker
celery -A async_finder worker -n=worker5 --loglevel=info

## Cloud Environment - Amazon Web Services
# SSH to EC2 instance
`ssh -i ~/.ssh/aws-key.pem ec2-user@ec2-52-90-79-36.compute-1.amazonaws.com`

