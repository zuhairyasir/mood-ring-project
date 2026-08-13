# uvicorn main:app --reload

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline
from dotenv import load_dotenv
from groq import Groq

load_dotenv();
groq_client = Groq()

app=FastAPI()
classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials= True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class JournalEntry(BaseModel):
    text:str

@app.get("/")
def red_root():
    return {"message": "Hello World: The Mood-Ring Backend is Live!"}

@app.post("/analyze")
def analyze_mood(entry: JournalEntry):
    result = classifier(entry.text)
    detected_emotion = result[0]["label"]
    confidence_score = result[0]['score']
    prompt = (
        f"A user wrote this journal entry: \"{entry.text}\"\n"
        f"Their detected emotion is: {detected_emotion}\n"
        f"Write a warm, thoughtful, supportive reply (5-7 sentences), "
        f"as if you're a caring friend reading their journal."
    )
    try:
        groq_response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        ai_reply = groq_response.choices[0].message.content
    except Exception as e:
        ai_reply = "I'm having trouble replying right now, but I caught how you're feeling!"
        print(f"Groq error: {e}")
    
    try:
        groq_response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        ai_reply = groq_response.choices[0].message.content
        title_prompt = (
            f"Summarize this journal entry into a short title, "
            f"3 to 5 words maximum, no punctuation, no quotation marks: "
            f"\"{entry.text}\""
        )
        title_response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": title_prompt}]
        )
        ai_title = title_response.choices[0].message.content.strip()

    except Exception as e:
        ai_reply = "I'm having trouble replying right now, but I caught how you're feeling!"
        ai_title = entry.text[:30] 
        print(f"Groq error: {e}")

    return {
        "emotion": detected_emotion,
        "confidence": confidence_score,
        "reply": ai_reply,
        "title": ai_title,     
        "reciv_txt": entry.text
    }
