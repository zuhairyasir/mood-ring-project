# uvicorn main:app --reload
# git add .
# git commit -m "Initial commit: working Mood-Ring Journal with emotion detection, AI replies, chat history sidebar"
# git log

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from emotion_service import EmotionService
from reply_service import ReplyService
from fastapi.responses import StreamingResponse
from models import JournalEntry, MoodLogPayload
from stats_service import StatsService

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

stats_service = StatsService()
emotion_service = EmotionService()
reply_service = ReplyService()

@app.post("/stats")
def get_stats(payload: MoodLogPayload):
    buffer = stats_service.generate_emotion_chart(payload.entries)
    return StreamingResponse(buffer, media_type="image/png")

@app.get("/")
def read_root():
    return {"message": "Hello World: The Mood-Ring Backend is Live!"}

@app.post("/analyze")
def analyze_mood(entry: JournalEntry):
    detected_emotion, confidence_score = emotion_service.classify(entry.text)

    try:
        ai_reply = reply_service.generate_reply(entry.text, detected_emotion)
        ai_title = reply_service.generate_title(entry.text)
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