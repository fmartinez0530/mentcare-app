# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install system dependencies for mysqlclient and pkg-config
RUN apt-get update && apt-get install -y \
    build-essential \
    libmariadb-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside the container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=backend/app.py

# Run Flask when the container launches
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
