from openai import OpenAI
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from pydub import AudioSegment
from sys import argv
import time
import json

# use ./key.txt as the key file
with open("./key.txt", "r") as f:
    key = f.read().strip()

# create an OpenAI object
client = OpenAI(api_key=key)


def create_transcript_from_audio_file(audio_file: str):
    file = open(audio_file, "rb")
    response = client.audio.transcriptions.create(
        model="whisper-1", language="fr", file=file, response_format="verbose_json"
    )
    # response.segments
    # load into json file
    new_file = open(f"output.json", "w")
    new_file.write(json.dumps(response.segments))
    new_file.close()


def create_audio_file_from_text(text: str) -> str:
    audio_files = []
    for i in range(0, len(text), 4000):
        print(f"Creating audio file chunk {i} to {i+4000}...")
        file_name = f"temp/output-temp-{i}.mp3"
        chunk = text[i : i + 4000]
        response = client.audio.speech.create(
            model="tts-1-hd", voice="nova", input=chunk, speed=1
        )
        response.stream_to_file(file_name)
        audio_files.append(file_name)

    # combine audio files
    print("Combining audio files...")
    combined_file_name = f"output-{time.time()}.mp3"
    combined = AudioSegment.from_file(audio_files[0], format="mp3")
    for file in audio_files[1:]:
        next_segment = AudioSegment.from_file(audio_files, format="mp3")
        combined += next_segment

    combined.export(combined_file_name, format="mp3")

    print("Audio files combined.")

    return combined_file_name


def translate_and_reformat_transcript(
    transcript: str, target_language: str
) -> str | None:
    # go by 4000 char chunks
    translated_transcript = ""
    for i in range(0, len(transcript), 4000):
        print(f"Translating chunk {i} to {i+4000}...")
        chunk = transcript[i : i + 4000]
        resp = client.chat.completions.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {
                    "role": f"system",
                    "content": "You are a translation and reformatting bot. You only output the requested translation in {target_language} with no further commentary.",
                },
                {
                    "role": "user",
                    "content": f"Translate the following transcript into {target_language} and reformat it with punctuation: {chunk}",
                },
            ],
        )
        translated_transcript += " " + resp.choices[0].message.content
    return translated_transcript


def retrieve_youtube_transcript(youtube_id: str) -> str:
    transcript_resp = YouTubeTranscriptApi.get_transcript(youtube_id)
    # turn the transcript into a string
    transcript = TextFormatter().format_transcript(transcript_resp)
    # print first 20
    return transcript


def create_personal_podcast(youtube_id: str):
    print("Creating personal podcast for video: " + youtube_id)
    print("Retrieving transcript for video: " + youtube_id)
    transcript = retrieve_youtube_transcript(youtube_id)
    print("Transcript retrieved.")
    print("Translating and reformatting transcript...")
    translated_transcript = translate_and_reformat_transcript(transcript, "French")
    print("Translation and reformatting complete.")
    print("Creating audio file...")
    audio_file = create_audio_file_from_text(translated_transcript)
    # print("Audio file created.")
    # print("Transcribing audio file...")
    # create_transcript_from_audio_file(audio_file)

    # print("Audio file transcribed.")


if __name__ == "__main__":
    if len(argv) < 2:
        print("Usage: python personal-podcast.py <youtube_id>")
        exit(1)
    else:
        youtube_id = argv[1]
        create_personal_podcast(youtube_id)
