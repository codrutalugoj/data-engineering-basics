FROM python:3.8-slim

RUN apt-get update && apt-get install -y postgresql-client

COPY elt.py .

CMD ["python", "elt.py"]