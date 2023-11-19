from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse

# Twilio credentials (These should ideally be loaded from environment variables)
ACCOUNT_SID = 'ACac00b5a7490fe4cb8d755138ca02c538'
AUTH_TOKEN = '31dbc3b2a88a7d8fc80b47b0ffb47cd2'

# Initialize the Twilio clienta
client = Client(ACCOUNT_SID, AUTH_TOKEN)

def answer_call(call_sid):
    """ Answer an incoming call """
    call = client.calls(call_sid).update(
        method='POST',
        url='https://b04a-178-24-247-214.ngrok-free.app/voice'  # URL to handle the voice logic
    )
    return call




# In twilio_handler.py

def create_twilio_audio_response(audio_file_url):
    """ Create a Twilio VoiceResponse object to play the given audio file """
    response = VoiceResponse()
    response.play(audio_file_url)  # Assuming audio_file_url is accessible via HTTP
    return str(response)

