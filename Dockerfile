# Use the official Python image as a base image
FROM python:3.9-slim

# Set environment variables
ENV PORT=8080
ENV APP_HOME /app

# Create the directory for the application
WORKDIR $APP_HOME

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY . .

# Expose the port on which the Flask app will run
EXPOSE $PORT

# Run the Flask application
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
