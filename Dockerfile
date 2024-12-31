# Use a Python base image
FROM python:3.9-slim

# Install necessary system packages for Playwright
RUN apt-get update && apt-get install -y curl && apt-get clean

# Install Playwright dependencies
RUN npx playwright install-deps

# Set the working directory
WORKDIR /app

# Copy project files into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright and its browser binaries
RUN pip install playwright && playwright install

# Expose the application port
EXPOSE 5000

# Start the Flask application using Gunicorn
CMD ["gunicorn", "api:app", "--bind", "0.0.0.0:5000"]
