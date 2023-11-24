from flask import Flask, request, send_from_directory, url_for
from twilio.twiml.voice_response import VoiceResponse
from twilio_handler import create_twilio_audio_response
from speech_handler import speech_to_text, text_to_speech_and_upload  # updated function
from openai_handler import generate_chatbot_response

from init import create_app

app = create_app()

# Add other necessary initializations or configurations
@app.route('/voice', methods=['POST'])
def voice():

    
    response = VoiceResponse()

    # Instruct Twilio to record the caller's message
    response.say("What do you want?")
    response.record(maxLength="8", action="/handle-recording")

    return str(response)

@app.route('/handle-recording', methods=['POST'])
def handle_recording():
    recording_url = request.values.get("RecordingUrl", None)
    print("Received Recording URL:", recording_url)  # Debug print

    # Convert the recording to text
    transcript = speech_to_text(recording_url)
    print("Transcription:", transcript)  # Debug print
    print("Type of Transcription:", type(transcript))  # Print the data type of transcript

    # Generate AI response
    ai_response = generate_chatbot_response(transcript)
    print("AI Response:", ai_response)  # Debug print

    # Convert AI text response to speech and get the URL to the audio file
    ai_speech_url = text_to_speech_and_upload(ai_response)
    if not ai_speech_url:
        print("Failed to convert text to speech.")
        return "Error in text-to-speech conversion", 500
    print("AI Speech URL:", ai_speech_url)  # Debug print

    # Create Twilio VoiceResponse to play the audio and then record the next message
    response = VoiceResponse()
    if ai_speech_url:
        response.play(ai_speech_url)  # Play AI response
    else:
        response.say("Sorry, I could not process your request.")  # Fallback in case of error

    # Instruct Twilio to record the user's next message
    response.record(maxLength="8", action="/handle-recording")

    return str(response), 200, {'Content-Type': 'text/xml'}




@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)

if __name__ == "__main__":
    app.run(debug=True)


