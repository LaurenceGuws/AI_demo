# Use an official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Set PYTHONPATH environment variable
ENV PYTHONPATH /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make the start.sh script executable
RUN chmod +x start.sh

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run start.sh when the container launches
CMD ["./start.sh"]
