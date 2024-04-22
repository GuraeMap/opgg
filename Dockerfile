FROM python:3.11-slim



WORKDIR /app

COPY requirement.txt .


RUN pip install --upgrade pip
RUN pip install -r requirement.txt