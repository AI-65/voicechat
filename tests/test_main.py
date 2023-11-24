from config import load_configuration


from openai import OpenAI
import openai

# Load OpenAI API key from a configuration method
openai.api_key = load_configuration()

# Initialize OpenAI client
#client = OpenAI(api_key=openai.api_key)

def generate_chatbot_response(prompt_content):

        client = OpenAI()
        messages = [
            {"role": "system", "content": "Du bist ein freundlicher Telefon-angestellter für die Koban Bauservice Gmbh. EIne Firma die Glasfasern verlegt und Termine für Monatage und Hausbesuche macht"},
            {"role": "user", "content": prompt_content}  # Use the selected prompt type
        ]

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Choose the appropriate model
            messages=messages,
            max_tokens=100
        )


        return response.choices[0].message.content

# Example usage

hi = "hi"
response_text = generate_chatbot_response(hi)
print(response_text)
