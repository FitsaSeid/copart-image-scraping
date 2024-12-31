# Use a Python base image
FROM python:3.9-slim

# Install system dependencies required by Playwright
RUN apt-get update && apt-get install -y \
    libdrm2 \
    libgbm1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libxss1 \
    libnss3 \
    libgtk-3-0 \
    libxshmfence1 \
    libwayland-client0 \
    libxkbcommon0 \
    libxrender1 \
    libxtst6 \
    libpangocairo-1.0-0 \
    libpango-1.0-0 \
    libcairo2 \
    libcairo-gobject2 \
    && apt-get clean

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
