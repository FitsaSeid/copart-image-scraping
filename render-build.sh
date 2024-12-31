#!/bin/bash

echo "Installing missing libraries for Playwright..."

apt-get update && apt-get install -y \
    libnss3 \
    libx11-xcb1 \
    libxcb-dri3-0 \
    libxcomposite1 \
    libxrandr2 \
    libxi6 \
    libxtst6 \
    libasound2 \
    libpangocairo-1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libexpat1 \
    libfontconfig1 \
    libglib2.0-0 \
    libgdk-pixbuf2.0-0 \
    libgtk-3-0 \
    libxdamage1 \
    libxshmfence1 \
    libnspr4 \
    libxss1 \
    libxext6 \
    libwayland-client0 \
    libwayland-cursor0 \
    libwayland-egl1 \
    libenchant-2-2 \
    libavif15 \
    libgstcodecparsers-1.0-0 \
    libgstgl-1.0-0 \
    libmanette-0.2-0 \
    libsecret-1-0 \
    libgles2-mesa \
    libxkbcommon0

echo "Installing Playwright browsers..."
playwright install
