from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import json

# Replace with the channel's videos tab URL
CHANNEL_VIDEOS_URL = 'https://www.youtube.com/@channelname/videos'  # Replace with actual channel URL and with streams for live streams

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run browser in headless mode
options.add_argument('--log-level=3')  # Suppress warnings
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open the videos page of the channel
driver.get(CHANNEL_VIDEOS_URL)
time.sleep(3)

# Scroll to load all videos
SCROLL_PAUSE_TIME = 2
last_height = driver.execute_script("return document.documentElement.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.documentElement.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height


# Extract video URLs
videos = driver.find_elements(By.ID, "video-title-link")
video_links = [{video.get_attribute('title'):video.get_attribute('href')} for video in videos if video.get_attribute('href')]

# Save to JSON
with open("videos_links.json", "w", encoding="utf-8") as f:
    json.dump(video_links, f, indent=2, ensure_ascii=False)

print(f"Found {len(video_links)} videos. Links saved to video_links.json")

driver.quit()