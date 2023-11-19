from pathlib import Path
import openai
import requests
from io import BytesIO
import os
import time
from config import load_configuration
from twilio.rest import Client
from openai import OpenAI
from flask import url_for




# Load OpenAI API key from configuration
openai.api_key = load_configuration()

# Directory to save audio files (ensure this directory exists and is served by Flask)
AUDIO_FILES_DIR = 'path_to_audio_files_directory'

def text_to_speech(input_text, output_file_path):
    try:
        response = openai.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=input_text
        )
        response.stream_to_file(output_file_path)
        return output_file_path
    except Exception as e:
        print(f"Error in text_to_speech: {e}")
        return None

def speech_to_text(audio_url, retry_count=3, delay=1, file_path="temp_audio_file.wav"):
    try:
        # Twilio credentials
        TWILIO_ACCOUNT_SID = 'ACac00b5a7490fe4cb8d755138ca02c538'
        TWILIO_AUTH_TOKEN = '31dbc3b2a88a7d8fc80b47b0ffb47cd2'

        transcript = None
        for attempt in range(retry_count):
            try:
                time.sleep(delay)  # Delay before each attempt
                response = requests.get(audio_url, auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN))
                response.raise_for_status()

                # Save the audio file locally
                with open(file_path, "wb") as file:
                    file.write(response.content)

                # Debugging: Print the size of the downloaded file
                print(f"Downloaded file size: {os.path.getsize(file_path)} bytes")

                # Open the saved audio file and transcribe
                with open(file_path, "rb") as audio_file:
                    transcript_response = openai.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file
                    )

                # Debugging: Print the complete transcription response
                print("Transcription Response:", transcript_response)

                # Accessing the transcription text directly
                if hasattr(transcript_response, 'text'):
                    transcript = transcript_response.text
                    break

            except requests.exceptions.RequestException as e:
                print(f"Attempt {attempt + 1} failed: {e}")

        return transcript

    except Exception as e:
        print(f"Error in speech_to_text: {e}")
        return None

def text_to_speech_and_upload(input_text):
    try:
        # Define the directory to save audio files
        audio_files_dir = 'uploads'
        if not os.path.exists(audio_files_dir):
            os.makedirs(audio_files_dir, exist_ok=True)

        audio_file_name = f"speech_{int(time.time())}.mp3"
        audio_file_path = os.path.join(audio_files_dir, audio_file_name)

        # Convert text to speech
        result = text_to_speech(input_text, audio_file_path)
        if not result:
            raise Exception("Failed to create audio file.")

        # Construct the full URL for internal use
        full_audio_file_url = url_for('uploaded_file', filename=audio_file_name, _external=True)

        return full_audio_file_url
    except Exception as e:
        print(f"Error in text_to_speech_and_upload: {e}")
        return None




