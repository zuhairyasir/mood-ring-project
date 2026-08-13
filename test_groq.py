from dotenv import load_dotenv
import os
from groq import Groq

load_dotenv()
client = Groq()

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", "content": "Say hello in one short sentence."}
    ]
)

print(response.choices[0].message.content)