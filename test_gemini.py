from dotenv import load_dotenv
import os
from google import genai

load_dotenv()
client = genai.Client()

response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents="say hello in one short sentence."
)

print(response.text)