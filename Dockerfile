# Use the official Python image.
# https://hub.docker.com/_/python
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Copy config.yaml to the appropriate location
COPY config/config.yaml /app/config/config.yaml

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define environment variable
ENV NAME DataSanity

# Run app.py when the container launches
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8080"]
