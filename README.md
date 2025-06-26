# YouTube Video Downloader Suite

A complete solution for downloading YouTube videos from channels, including tools for collecting video links and downloading them in batches.

## Components

### 1. Video Link Collector (`ytvideolinkcollector.py`)

- **Purpose**: Automatically collect all video links from a YouTube channel
- **Output**: Creates `videos_links.json` with all video titles and URLs
- **Technology**: Uses Selenium WebDriver for web scraping
- **Features**:
  - Headless browser operation
  - Automatic scrolling to load all videos
  - Supports both regular videos and live streams
  - Extracts video titles and URLs

### 2. Video Downloader (`video_downloader.py`)

- **Purpose**: Download videos from the collected links
- **Input**: Uses `video_links.json` (or custom file)
- **Features**:
  - Range-based downloading (e.g., videos 1-100)
  - High-quality MP4 downloads
  - Progress tracking and error logging
  - Sequential numbering of files

## Features

- **Complete workflow**: Collect links → Download videos
- **Batch processing**: Download specific ranges of videos
- **High-quality downloads**: Best available MP4 format
- **Progress tracking**: Real-time download progress
- **Error handling**: Failed downloads logged automatically
- **Cross-platform**: Works on Windows, macOS, and Linux
- **Sanitized filenames**: Safe file naming for all operating systems

## Usage

### Method 1: Command Line Arguments (Recommended for executables)

```bash
./youtube_downloader 1 100                                    # Download videos 1-100 with defaults
./youtube_downloader 1 100 video_links.json downloads        # Specify all parameters
```

### Method 2: Interactive Mode

```bash
./youtube_downloader                                          # Will prompt for all inputs
```

## Complete Workflow

### Step 1: Collect Video Links

First, use the video link collector to gather all videos from a YouTube channel:

1. **Edit the channel URL** in `ytvideolinkcollector.py`:

```python
CHANNEL_VIDEOS_URL = 'https://www.youtube.com/@your_channel_name/videos' #replace with your channel URL and videos with streams for live streams   
```

1. **Install dependencies**:

```bash
pip install selenium webdriver-manager
```

1. **Run the collector**:

```bash
python ytvideolinkcollector.py
```

1. **Output**: Creates `video_links.json` with all video information

### Step 2: Download Videos
Use the video downloader to download specific ranges:

1. **Download videos**:
```bash
# Download first 50 videos
./youtube_downloader 1 50

# Download videos 100-200
./youtube_downloader 100 200

# Download with custom settings
./youtube_downloader 1 100 stream_links.json my_downloads
```

### Alternative: Manual Link Collection
If you prefer to create your own video list, create a `video_links.json` file manually:

```json
[
  {
    "Video Title 1": "https://www.youtube.com/watch?v=VIDEO_ID1"
  },
  {
    "Video Title 2": "https://www.youtube.com/watch?v=VIDEO_ID2"
  }
]
```

## Creating a Binary/Executable

If you want to create your own executable from the Python script, follow these steps:

### Prerequisites
1. Make sure you have Python 3.7+ installed
2. Install the required dependencies:
```bash
pip install yt-dlp tqdm pyinstaller
```

### Build Process
1. **Clone or download the script**:

   - Make sure you have `video_downloader.py` in your working directory

2. **Install PyInstaller** (if not already installed):

```bash
pip install pyinstaller
```

1. **Create the executable**:

```bash
pyinstaller --onefile --name youtube_downloader video_downloader.py
```

1. **Find your executable**:
   - The executable will be created in the `dist/` folder
   - On Windows: `dist/youtube_downloader.exe`
   - On macOS/Linux: `dist/youtube_downloader`

2. **Make it executable** (macOS/Linux only):
```bash
chmod +x dist/youtube_downloader
```

1. **Optional: Copy to desired location**:
```bash
cp dist/youtube_downloader /usr/local/bin/  # System-wide installation
# or
cp dist/youtube_downloader ~/Desktop/       # Desktop shortcut
```

### Build Options
- **Single file**: `--onefile` (creates one executable file)
- **Custom name**: `--name your_app_name`
- **Include icon**: `--icon=icon.ico` (Windows) or `--icon=icon.icns` (macOS)
- **Console app**: `--console` (default for this script)
- **Windowed app**: `--windowed` (hides console, not recommended for this script)

### Example Build Commands
```bash
# Basic build
pyinstaller --onefile video_downloader.py

# Custom name with icon
pyinstaller --onefile --name "YT-Downloader" --icon=icon.ico video_downloader.py

# Debug version (shows more output)
pyinstaller --onefile --name youtube_downloader --debug video_downloader.py
```


## Video Links Format

Your `video_links.json` should be formatted like this:

```json
[
  {
    "Video Title 1": "https://www.youtube.com/watch?v=VIDEO_ID1"
  },
  {
    "Video Title 2": "https://www.youtube.com/watch?v=VIDEO_ID2"
  }
]
```

## Examples

- Download first 50 videos: `./youtube_downloader 1 50`
- Download videos 100-200: `./youtube_downloader 100 200`
- Download last 10 videos: `./youtube_downloader 1471 1481`
- Download with custom files: `./youtube_downloader 1 100 my_videos.json my_folder`


## Troubleshooting

1. **Permission denied**: Run `chmod +x youtube_downloader` to make it executable
2. **Missing video_links.json**: Make sure this file exists in the same directory
3. **Network issues**: Check your internet connection
4. **Failed downloads**: Check `failed_downloads.log` for details
5. **EOFError in executable**: Use command line arguments instead of interactive mode

## Development

### Running from Source
If you prefer to run the Python scripts directly:

```bash
# Install dependencies for link collection
pip install selenium webdriver-manager

# Install dependencies for video downloading
pip install yt-dlp tqdm

# Step 1: Collect video links from a channel
python ytvideolinkcollector.py

# Step 2: Download videos
python video_downloader.py 1 100
python video_downloader.py 1 100 video_links.json downloads
```

### Dependencies

- **yt-dlp**: YouTube video downloading library
- **tqdm**: Progress bar library
- **selenium**: Web automation for link collection
- **webdriver-manager**: Automatic Chrome driver management
- **PyInstaller**: For creating executables (development only)

## Notes

- The executable is approximately 15MB and includes all dependencies
- Downloaded videos are saved in MP4 format with best quality available
- Video titles are sanitized to remove invalid filename characters
- Videos are numbered sequentially (001, 002, etc.) based on their position
- The progress bar shows real-time download progress
- Failed downloads are automatically logged for review
