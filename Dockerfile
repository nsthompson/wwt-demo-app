FROM python:3.9-alpine

COPY . /data

WORKDIR /data

RUN pip install -r ./requirements.txt
RUN chgrp -R 0 /data && \
    chmod -R g=u /data

EXPOSE 8080
EXPOSE 8081

WORKDIR /data/app

ENTRYPOINT ["python", "app.py"]
