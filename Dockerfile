# Use an official Python runtime as a parent image
FROM python:3.11.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install Poetry
RUN apt-get update && \
    apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to the PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy only the pyproject.toml and poetry.lock to leverage Docker cache
COPY pyproject.toml poetry.lock* /usr/src/app/

# Install dependencies
RUN poetry install --no-root

# Copy the rest of the application code
COPY . /usr/src/app/

RUN chmod +x /usr/src/app/run.sh

RUN cd /usr/src/app
RUN ./run.sh
