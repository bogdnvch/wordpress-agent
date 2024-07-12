FROM python:3.11.9-slim

WORKDIR /app

# Poetry
#RUN apt-get update && \
#    apt-get install -y curl && \
#    curl -sSL https://install.python-poetry.org | python3 -
#
#ENV PATH="/root/.local/bin:$PATH"
#
#COPY pyproject.toml poetry.lock ./
#RUN poetry install --no-interaction --no-ansi

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x run.sh
RUN ./run.sh
