#!/bin/bash

# YouTube Video Downloader Wrapper Script
# Usage: ./download.sh [start] [end]
# Example: ./download.sh 1 100

EXECUTABLE="./youtube_downloader"

# Check if executable exists
if [ ! -f "$EXECUTABLE" ]; then
    echo "Error: youtube_downloader executable not found!"
    echo "Make sure the executable is in the same directory as this script."
    exit 1
fi

# Check if video_links.json exists
if [ ! -f "video_links.json" ]; then
    echo "Error: video_links.json not found!"
    echo "Make sure video_links.json is in the same directory."
    exit 1
fi

# Make executable if it's not already
chmod +x "$EXECUTABLE"

# Run the downloader with arguments
if [ $# -eq 2 ]; then
    echo "Downloading videos from $1 to $2..."
    "$EXECUTABLE" "$1" "$2"
elif [ $# -eq 0 ]; then
    echo "Starting interactive mode..."
    "$EXECUTABLE"
else
    echo "Usage: $0 [start_number] [end_number]"
    echo "Examples:"
    echo "  $0 1 100      # Download videos 1 to 100"
    echo "  $0            # Interactive mode"
    exit 1
fi
