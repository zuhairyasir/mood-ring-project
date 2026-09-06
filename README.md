#  Mood-Ring Journal

A full-stack, experimental digital diary built to explore emotion classification, dynamic UI state management, and LLM prompt design.

Write a journal entry, and the app detects your emotion, shifts the entire page's color to match your mood, and replies like a genuinely emotionally intelligent friend and not a scripted chatbot.

Project Purpose: This repository is an educational portfolio project. I built it to get hands on experience integrating local Hugging Face transformer models into asynchronous web frameworks, custom data structures (like Tries), and empirical NLP evaluation. It is not intended as a commercial therapy or mental health tool.

---

##  Features

### Core experience
- **Real-time emotion detection** via a Hugging Face Transformers model, with confidence scoring
- **Dynamic mood reactive theme** — automatically shifts the page background color to mirror the dominant detected emotion of your entry
- **AI-generated replies** via Groq's hosted LLM, prompted specifically to sound like a perceptive friend rather than a generic support bot
- **"Why this emotion?"** — a second AI call gives its best-effort interpretation of what triggered a classification (framed honestly as an interpretation, not the model's actual internals)

### Conversations
- Persistent, multi-chat sidebar with **star, rename, delete, and folders**
- **Trie-based search** (a hand-built prefix tree) across all saved entries
- **Temporary ("ghost") chats** that are never saved anywhere
- **Edit a sent message** — truncates and resends the conversation from that point
- **Stop an in flight AI response** mid generation

### Voice
- Speech-to-text journal entry via the browser's native Speech Recognition API
- Text-to-speech playback of AI replies, with an adjustable pitch and a lightweight Roman Urdu voice heuristic

### Accounts
- Email + password signup/login with bcrypt hashed passwords and session tokens (SQLite-backed)
- **Guest mode** — anyone can chat normally without an account; extras (Settings, Temporary Chat, Folders, Mood Stats) unlock after signing in

### Analytics & Research
- **Mood Trends** dashboard — Pandas + Matplotlib charts (emotion frequency, confidence over time) generated server-side
- **Empirical evaluation script** (`benchmark.py`) — measures real classifier accuracy (with a per-emotion breakdown) and pipeline latency, producing `EVALUATION.md`
- Documented finding: the emotion classifier under-detects **implicit anger** (expressed through behavior rather than explicit vocabulary) — see `EVALUATION.md` for the full analysis

---

##  Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI, Uvicorn |
| Emotion detection | Hugging Face Transformers (local model) |
| AI replies | Groq API (hosted LLM) |
| Accounts | SQLite, bcrypt |
| Analytics | Pandas, Matplotlib |
| Frontend | Vanilla JavaScript, HTML, CSS (no framework) |

---

## Project Structure

```
mood-ring-journal/
├── main.py                # FastAPI app: routes and orchestration
├── models.py               # Pydantic request/response models
├── emotion_service.py       # EmotionService — Hugging Face classifier wrapper
├── reply_service.py         # ReplyService — Groq prompt design and calls
├── stats_service.py         # StatsService — Pandas/Matplotlib chart generation
├── search_service.py        # SearchService — Trie-based prefix search
├── auth_service.py          # AuthService — signup/login, sessions, bcrypt
├── benchmark.py              # Standalone accuracy/latency evaluation script
├── EVALUATION.md              # Generated report from benchmark.py
├── index.html                # Entire frontend (HTML/CSS/JS)
├── requirements.txt           # Python dependencies
├── .env                        # API keys (not committed — see setup below)
└── .gitignore
```

---

## Setup and initialization

### 1. Clone and create a virtual environment
```bash
git clone <your-repo-url>
cd mood-ring-journal
python -m venv env
```
Activate it:
- Windows: `env\Scripts\activate`
- macOS/Linux: `source env/bin/activate`

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up your API key
Create a `.env` file in the project root:
```
GROQ_API_KEY=your_key_here
```
Get a free key at [console.groq.com](https://console.groq.com).

### 4. Run the backend
```bash
uvicorn main:app --reload
```
The first run will download the emotion classification model (~330MB) — this only happens once.

### 5. Serve the frontend
In a separate terminal:
```bash
python -m http.server 5500
```
Open `http://127.0.0.1:5500` in your browser.

---

## 🔌 Key API Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/analyze` | POST | Classify emotion + generate AI reply for a journal entry |
| `/stats` | POST | Generate mood trend charts from logged emotion data |
| `/search` | POST | Trie-based prefix search across saved chats |
| `/explain` | POST | AI-generated interpretation of a detected emotion |
| `/signup` / `/login` | POST | Account creation and authentication |
| `/me` | GET | Validate a session token |

---

## Evaluation

Run the benchmark suite yourself:
```bash
python benchmark.py
```
This measures classifier accuracy against a hand labeled test set (with per emotion breakdown), plus latency for each pipeline stage, and writes the results to `EVALUATION.md`.

**Key finding:** the emotion classifier performs well overall but shows a meaningful weakness on **implicit anger** — anger expressed through described behavior rather than explicit angry vocabulary. Full analysis, including specific misclassification examples, is in `EVALUATION.md`.

---

## Known Limitations

- Chat data, settings, and mood logs are stored in browser `localStorage`, not tied to user accounts server-side — logging in personalizes the experience but doesn't yet sync data across devices
- The emotion classifier is English-trained; results on other languages are not validated
- Can only detect one emotion at a time (No multiple emotions)
- Free-tier API rate limits apply (Groq)

---

## Possible Future Work

- Migrate chat/settings storage from `localStorage` to per-user database records
- Fine-tune the emotion classifier (e.g. via LoRA) specifically to address the implicit-anger weakness identified in evaluation
- Expand the benchmark test set for more statistically robust accuracy claims

---

## License

This project was built for educational and portfolio purposes.
