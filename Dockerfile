FROM python:3.9-alpine

RUN pip install -r ./requirements.txt

COPY . /opt/

EXPOSE 8080
EXPOSE 8081

WORKDIR /opt

ENTRYPOINT ["python", "app.py"]
