# Use the official Python image as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Expose port 5000
EXPOSE 5000

# Define the command to run your application
CMD ["python", "your_app_name.py"]
