# Use an official Python runtime as a base image
FROM python:3.9-slim-buster

# Set environment variables
# Use unbuffered mode to receive logs from the output, recommended when running Python within Docker containers
# It prevents Python from buffering the standard outputs and it's recommended when running Python within Docker containers
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container to /app
WORKDIR /app

# Install system dependencies
# It's often a good idea to install system-level dependencies first and then copy over just the requirements.txt file
# This allows Docker to cache the step of installing dependencies, making subsequent builds faster
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt file into the container at /app
COPY requirements.txt /app/

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
# This is done after installing dependencies to leverage Docker cache
# and avoid reinstalling dependencies if your app code changes but dependencies remain the same
COPY . /app/

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["gunicorn", "-b", "0.0.0.0:8080", "main:app"]
