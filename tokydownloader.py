import re
import json5
import requests
from pathlib import Path
from tqdm import tqdm
import time
import threading
import sys
import os
import select

def listen_for_input(pause_event, stop_event):
    """
    Listens for 'p' key press to toggle pause/resume.
    For Windows, msvcrt is used; for Unix, select on sys.stdin.
    """
    if os.name == 'nt':
        import msvcrt
        while not stop_event.is_set():
            if msvcrt.kbhit():
                key = msvcrt.getch().decode('utf-8').lower()
                if key == 'p':
                    if pause_event.is_set():
                        pause_event.clear()
                        print("\nDownload paused. Press 'p' to resume.")
                    else:
                        pause_event.set()
                        print("\nDownload resumed.")
            time.sleep(0.1)
    else:
        # Basic Unix non-blocking input using select
        while not stop_event.is_set():
            if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                key = sys.stdin.read(1).lower()
                if key == 'p':
                    if pause_event.is_set():
                        pause_event.clear()
                        print("\nDownload paused. Press 'p' to resume.")
                    else:
                        pause_event.set()
                        print("\nDownload resumed.")
            time.sleep(0.1)

def get_chapter_content(chapter_data, download_folder, pause_event):
    BASE_URLS = [
        'https://files01.tokybook.com/audio/',
        'https://files02.tokybook.com/audio/'
    ]

    for base_url in BASE_URLS:
        url = base_url + chapter_data['chapter_link_dropbox']
        try:
            response = requests.get(url, stream=True, timeout=10)
        except Exception as e:
            print("Error fetching URL:", e)
            continue

        if response.status_code == 200:
            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024  # 1 Kibibyte
            progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True, 
                                desc=f"Downloading {chapter_data['name']}", dynamic_ncols=True)
            start_time = time.time()
            downloaded_bytes = 0
            file_path = Path(download_folder) / (chapter_data['name'] + '.mp3')
            with open(file_path, 'wb') as f:
                for data in response.iter_content(block_size):
                    # Pause mechanism: wait here if paused
                    while not pause_event.is_set():
                        time.sleep(0.1)
                    f.write(data)
                    downloaded_bytes += len(data)
                    progress_bar.update(len(data))
                    elapsed_time = time.time() - start_time
                    speed = downloaded_bytes / elapsed_time if elapsed_time > 0 else 0
                    remaining_time = (total_size - downloaded_bytes) / speed if speed > 0 else 0
                    progress_bar.set_postfix(eta=f"{remaining_time:.2f}s")
            progress_bar.close()
            return True
        
    print('[FAILED] Failed to download chapter', chapter_data['name'])
    print(response.text)
    return False

def download_chapter(chapters_queue: list, download_folder: str, pause_event):
    chapter_info = chapters_queue.pop()
    print("Chapter info:", chapter_info)
    chapter_file = Path(download_folder) / (chapter_info['name'] + '.mp3')
    chapter_file.touch(exist_ok=True)

    start_time = time.time()
    downloaded = get_chapter_content(chapter_info, download_folder, pause_event)
    if downloaded:
        end_time = time.time()
        download_speed = chapter_file.stat().st_size / (end_time - start_time) / 1024  # KB/s
        print(f"Download speed: {download_speed:.2f} KB/s")

def extract_chapters_data(web_page_response: str) -> list:
    data = re.search(r"tracks\s*=\s*(\[[^\]]+\])\s*", web_page_response)
    parsed_data_str = data.group(1)
    parsed_data = json5.loads(parsed_data_str)
    
    # Remove the first entry which is not an actual chapter
    parsed_data.pop(0)
    return parsed_data

def get_tokybook_data(tokybook_url: str):
    response = requests.get(tokybook_url)
    return response.text

if __name__ == '__main__':
    # Get user input for URL and folder name
    tokybook_url = input("Please enter the Tokybook URL: ")
    download_folder = input("Enter folder name for mp3 files (default 'MP3'): ") or "MP3"
    
    # Fetch page and extract chapters
    toky_response = get_tokybook_data(tokybook_url)
    chapters_datas = extract_chapters_data(toky_response)
    
    # Ensure folder exists
    Path(download_folder).mkdir(exist_ok=True)
    
    # Create pause/resume control flags
    pause_event = threading.Event()
    pause_event.set()  # Initially running (not paused)
    stop_event = threading.Event()
    
    # Start key-listener thread for pause/resume functionality
    listener_thread = threading.Thread(target=listen_for_input, args=(pause_event, stop_event), daemon=True)
    listener_thread.start()
    
    print("Press 'p' to pause/resume downloads.")
    
    while chapters_datas:
        download_chapter(chapters_datas, download_folder, pause_event)
    
    # Signal the listener thread to stop
    stop_event.set()
    print("All downloads complete!")
