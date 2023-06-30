FROM python:3.9-alpine

COPY . /data

WORKDIR /data

RUN pip install -r ./requirements.txt

EXPOSE 8080
EXPOSE 8081

WORKDIR /data/app

ENTRYPOINT ["python", "app.py"]
