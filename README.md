# youtube-chat

Get YouTube video summaries, then chat about the video with a GPT. 

Using GPT-4 and Whisper from OpenAI.

**Currently only works on MacOS**

## Setup

Install Certificates
1. Go to the Python folder in your Applications directory (e.g., /Applications/Python 3.x).
2. Run the "Install Certificates.command" script.

Install ffmpeg:
```
brew install ffmpeg
```
Installations:
```
pip install openai whisper pytube
```

OpenAI API key:
Run in terminal: export OPENAI_API_KEY='your_api_key'

## How to Use

To get the summary of a YouTube video and chat about it with a gpt, run:
```
python main.py
```
