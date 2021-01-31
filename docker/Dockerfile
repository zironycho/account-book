FROM python:3.6.9-slim-stretch

COPY ./requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /workspace

COPY . .
RUN pip install -e .
