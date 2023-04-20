# Use the official Python image as the base image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt requirements.txt

# Install the required packages
RUN python3 -m pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Run the Python script (main.py) when the container starts
CMD ["python3", "main.py"]