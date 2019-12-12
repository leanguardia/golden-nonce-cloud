FROM python:3.7
LABEL MAINTAINER Denis Leandro Guardia Vaca <leandro.guardia@toptal.com>
COPY python-libraries.txt app/python-libraries.txt 
WORKDIR /app
RUN pip install -r python-libraries.txt
ENTRYPOINT celery -A app.async_finder worker -n=worker1 --loglevel=info
