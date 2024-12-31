# Use a Python base image
FROM python:3.9-slim

# Install system dependencies required by Playwright
RUN apt-get update && apt-get install -y \
    libgstreamer1.0-0 \
    libatomic1 \
    libxslt1.1 \
    libwoff1 \
    libvpx7 \
    libevent-2.1-7 \
    libopus0 \
    libgstreamer-plugins-base1.0-0 \
    libgstaudio-1.0-0 \
    libgstgl-1.0-0 \
    libgstpbutils-1.0-0 \
    libgstvideo-1.0-0 \
    libgstcodecparsers-1.0-0 \
    libgstfft-1.0-0 \
    libflite1 \
    libwebpdemux2 \
    libavif15 \
    libharfbuzz-icu0 \
    libwebpmux3 \
    libenchant-2-2 \
    libsecret-1-0 \
    libhyphen0 \
    libmanette-0.2-0 \
    libpsl5 \
    libnghttp2-14 \
    libgles2-mesa \
    libx264-155 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

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
