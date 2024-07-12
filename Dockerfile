# Use an official Python runtime as a parent image
FROM python:3.11.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update

# Copy the rest of the application code
COPY . /usr/src/app/

RUN chmod +x /usr/src/app/run.sh

RUN cd /usr/src/app
RUN ./run.sh
