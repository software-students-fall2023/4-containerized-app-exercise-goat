# Use the official Python image as the base image
FROM python:3.8-slim

ENV GOOGLE_APPLICATION_CREDENTIALS="sunny-resolver-406200-d6e8c0dfe225.json"
# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Expose the port the app runs on
EXPOSE 5000

# Run the specified command within the container
CMD ["python3", "app.py"]
