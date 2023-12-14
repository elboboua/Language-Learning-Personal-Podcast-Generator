# Language Learning Personal Podcast Generator

## Description
This pet project uses the new OpenAI TTS models to take a youtube video, and convert it into an audio resource in the language of your choosing. It does this by following a few steps:
1. Retrieves the transcript from Youtube.
2. Translates and reformats the transcript using the `GPT3.5` model.
3. Generates the audio for the transcript using the `tts-1-hd` model.
4. Combines the individual audio files into one output mp3.

## Setup
1. Create a virtual env and activate it: `python3 -m venv env && source env/bin/activate` 
2. install dependencies: `pip install -r requirements.txt`
3. Create txt file named `key.txt` with your OpenAI api key.

## Usage
To generate a `"podast"`, run:
```bash
python personal-podcast.py <youtube_video_id> <ISO_language_code>
```