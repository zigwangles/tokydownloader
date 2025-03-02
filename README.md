# Toykdownloader

Toykdownloader is a slick Python command-line tool to download audio chapters from Tokybook. It lets you save MP3 files in a custom folder, provides real-time progress with ETA, and even supports pause/resume functionality. Sit back, relax, and let Toykdownloader do the heavy lifting!

## Features

- **Custom Download Folder:** Save MP3 files into any folder you choose.
- **Progress Bar with ETA:** Monitor your download's progress, speed, and estimated time remaining.
- **Pause/Resume Functionality:** Press `p` to pause or resume downloads whenever you need a break.
- **Interactive Command-Line Interface:** Simple prompts guide you through the process.

## Requirements

- Python 3.6 or higher
- Python packages:
  - `requests`
  - `tqdm`
  - `json5`

Install the required packages using pip:

```bash
pip install requests tqdm json
```

## How to Use
1. Clone or Download the Repository
   ```bash
   git clone https://github.com/zigwangles/toykdownloader.git
   cd toykdownloader
   ```
   
2. Run the Script:
   ```bash
   python tokydownloader.py
   ```
   
3. Follow the Prompts:
   - **Tokybook URL**: Paste the URL of the Tokybook page containing the audio chapters.
   - **Download Folder**: Enter the folder name where you’d like the MP3 files to be saved (default is MP3).
   - 
4. During the Download
   - Watch the progress bar for real-time updates on speed and estimated time remaining.
   - Press p to pause or resume downloads as needed.
   - 
5. Enjoy
   Let Toykdownloader handle your downloads while you relax and enjoy the audio!

## Troubleshooting
   - **Network Issues**: Ensure you have a stable internet connection.
   - **Incorrect URL**: Double-check the Tokybook URL if errors occur.
   - **Permissions**: Verify you have write access to the chosen download directory.

## License
This project is licensed under the MIT License.

Kick back and enjoy hassle-free downloads with Toykdownloader!
