# Use the latest stable Python 3.11 slim image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy requirements file from the current folder (where the Dockerfile is located)
COPY requirements /app/requirements

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements

# Copy the rest of the application code from the current folder
COPY . /app

# Start the application
CMD ["python", "api.py"]