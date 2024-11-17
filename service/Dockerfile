FROM python:3.11-slim

WORKDIR /app

COPY requirements /app/requirements

RUN pip install --no-cache-dir -r /app/requirements

COPY . /app

CMD ["python", "api.py"]