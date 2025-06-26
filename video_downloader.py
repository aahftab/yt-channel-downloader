import json
import yt_dlp
import os
import re
import sys
from tqdm import tqdm

# Show usage information
def show_usage():
    print("YouTube Video Downloader")
    print("=" * 40)
    print("Usage:")
    print("  1. Full command line: ./youtube_downloader start end [input_file] [folder]")
    print("  2. Range only: ./youtube_downloader start end")
    print("  3. Interactive mode: ./youtube_downloader")
    print()
    print("Examples:")
    print("  ./youtube_downloader 1 100")
    print("  ./youtube_downloader 1 100 my_videos.json my_downloads")
    print("  ./youtube_downloader")
    print()

# Check for help argument
if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', 'help']:
    show_usage()
    sys.exit(0)

# Get user inputs
def get_user_inputs():
    # Check if all parameters are provided via command line
    # Usage: script.py start_num end_num [input_file] [download_folder]
    if len(sys.argv) >= 5:
        # All parameters provided via command line
        input_file = sys.argv[3] if sys.argv[3] else "video_links.json"
        folder_name = sys.argv[4] if sys.argv[4] else "downloads"
        return input_file, folder_name
    elif len(sys.argv) >= 3:
        # Only range provided, use defaults for files
        return "video_links.json", "downloads"
    else:
        # Interactive mode - ask for everything with error handling
        try:
            input_file = input("Enter video links filename (default: video_links.json): ").strip()
            if not input_file:
                input_file = "video_links.json"
            
            folder_name = input("Enter download folder name (default: downloads): ").strip()
            if not folder_name:
                folder_name = "downloads"
                
            return input_file, folder_name
        except (EOFError, KeyboardInterrupt):
            print("\nUsing default values: video_links.json and downloads folder")
            return "video_links.json", "downloads"

# Get file and folder names
INPUT_FILE, DOWNLOAD_FOLDER = get_user_inputs()
LOG_FILE = "failed_downloads.log"

# Validate input file exists
if not os.path.exists(INPUT_FILE):
    print(f"Error: File '{INPUT_FILE}' not found!")
    sys.exit(1)

# Create download folder
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Get range input from user
def get_download_range():
    if len(sys.argv) >= 3:
        try:
            start_num = int(sys.argv[1])
            end_num = int(sys.argv[2])
            return start_num, end_num
        except ValueError:
            print("Error: Please provide valid integers for start and end numbers.")
            sys.exit(1)
    else:
        # Interactive mode with error handling
        try:
            while True:
                try:
                    range_input = input("Enter the range (start,end) e.g., '1,100': ")
                    start_str, end_str = range_input.split(',')
                    start_num = int(start_str.strip())
                    end_num = int(end_str.strip())
                    return start_num, end_num
                except (ValueError, IndexError):
                    print("Invalid input. Please enter in format: start,end (e.g., 1,100)")
        except (EOFError, KeyboardInterrupt):
            print("\nError: Unable to get input. Please use command line arguments.")
            print("Usage: python script.py start_num end_num [input_file] [download_folder]")
            print("Example: python script.py 1 100 video_links.json downloads")
            sys.exit(1)

# Sanitize title to remove characters not allowed in file names
def sanitize_title(title):
    return re.sub(r'[\\/*?:"<>|]', "", title).strip()

# Load video list
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    video_entries = json.load(f)

# Get download range
start_index, end_index = get_download_range()

# Validate range
total_videos = len(video_entries)
if start_index < 1 or end_index > total_videos or start_index > end_index:
    print(f"Error: Invalid range. Available videos: 1 to {total_videos}")
    sys.exit(1)

# Convert to 0-based indexing and slice the list
start_idx = start_index - 1
end_idx = end_index
selected_entries = video_entries[start_idx:end_idx]

# Flatten into [(title, url), ...] with numbering
video_list = []
for i, item in enumerate(selected_entries, start=start_index):
    title = sanitize_title(list(item.keys())[0])
    url = list(item.values())[0]
    # Add number prefix to the title
    numbered_title = f"{i:03d}. {title}"
    video_list.append((numbered_title, url, i))

print(f"Downloading videos {start_index} to {end_index} ({len(video_list)} videos)")
print(f"Files will be saved to: {DOWNLOAD_FOLDER}")
print(f"Videos will be numbered from {start_index:03d} to {end_index:03d}")

# Clear or create log file
with open(LOG_FILE, "w", encoding="utf-8") as log:
    log.write(f"Failed Downloads (Range: {start_index}-{end_index}):\n\n")

# Download videos with progress bar
for numbered_title, url, video_num in tqdm(video_list, desc="Downloading videos"):
    outtmpl_path = os.path.join(DOWNLOAD_FOLDER, f"{numbered_title}.%(ext)s")
    ydl_opts = {
        'outtmpl': outtmpl_path,
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'merge_output_format': 'mp4',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"✓ Downloaded video #{video_num}: {numbered_title}")
    except Exception as e:
        with open(LOG_FILE, "a", encoding="utf-8") as log:
            log.write(f"Video #{video_num} - \"{numbered_title}\": \"{url}\" - Error: {str(e)}\n")
        print(f"✗ Failed video #{video_num}: {numbered_title}")

print(f"\nDownload completed! Check '{DOWNLOAD_FOLDER}' folder for downloaded videos.")
print(f"Failed downloads logged in '{LOG_FILE}'")