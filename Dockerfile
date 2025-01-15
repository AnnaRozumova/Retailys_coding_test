FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y gcc libxml2-dev libxslt1-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip && pip install pipenv

COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy
COPY src/ ./src
COPY data/ ./data
EXPOSE 5000
CMD ["python", "src/main.py"]