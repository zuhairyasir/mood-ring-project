# Mood-Ring Journal

A full-stack, experimental digital diary built to explore emotion classification, dynamic UI state management, and LLM prompt design.

Write a journal entry, and the app detects your emotion, shifts the entire page's color to match your mood, and replies like a genuinely emotionally intelligent friend and not a scripted chatbot.

Project Purpose: This repository is an educational portfolio project. I built it to get hands on experience integrating local Hugging Face transformer models into asynchronous web frameworks, custom data structures (like Tries), and empirical NLP evaluation. It is not intended as a commercial therapy or mental health tool.

---

## Demo



A ~6 minute walkthrough: writing an entry, the background shifting with the detected emotion, the hands free voice conversation loop, folders and search, and the mood trends charts.

---

## Features

### Core experience
- **Real-time emotion detection** via a Hugging Face Transformers model, with confidence scoring
- **Dynamic mood reactive theme** — automatically shifts the page background color to mirror the dominant detected emotion of your entry
- **AI-generated replies** via Groq's hosted LLM, prompted specifically to sound like a perceptive friend rather than a generic support bot
- **"Why this emotion?"** — a second AI call gives its best-effort interpretation of what triggered a classification (framed honestly as an interpretation, not the model's actual internals)

### Conversations
- Persistent, multi-chat sidebar with **star, rename, delete, and folders**
- **Folder picker** with one-click chips for existing folders, plus a "remove from folder" shortcut
- **Trie-based search** (a hand-built prefix tree) across all saved entries
- **Temporary ("ghost") chats** that are never saved anywhere
- **Edit a sent message** — truncates and resends the conversation from that point
- **Stop an in flight AI response** mid generation
- Custom in-app dialogs for every prompt/confirm/alert — no native browser popups anywhere

### Voice
- Speech-to-text journal entry via the browser's native Speech Recognition API
- **Hands-free conversation mode** — tap the mic once and the loop continues on its own: your speech is transcribed and sent, the reply is spoken aloud, and the mic reopens when it finishes. Cancel any time to drop back to typing
- Text-to-speech playback of any reply, with adjustable pitch and a lightweight Roman Urdu voice heuristic

### Accounts
- Email + password signup/login with bcrypt hashed passwords and session tokens (SQLite-backed)
- **Guest mode** — anyone can chat normally without an account; extras (Customization, Temporary Chat, Folders, Mood Stats) unlock after signing in
- Per-account local data — chats, mood logs, and the active conversation are namespaced by account email, so switching accounts (or logging out to guest) swaps in a separate history instead of sharing one
- Password visibility toggles, autofill-aware signup, and a confirmation step before logging out

### Analytics & Research
- **Mood Trends** dashboard — Pandas + Matplotlib charts (emotion frequency, confidence over time) generated server-side
- **Empirical evaluation script** (`benchmark.py`) — measures real classifier accuracy (with a per-emotion breakdown) and pipeline latency, producing `EVALUATION.md`
- Documented finding: the emotion classifier under-detects **implicit anger** (expressed through behavior rather than explicit vocabulary) — see `EVALUATION.md` for the full analysis

### Interface
- Editorial visual language: serif display type, a warm brass accent, and dark ink surfaces layered over the live mood color
- A single token scale for color, radii, and elevation, so every surface derives from the same set of CSS variables
- Cursor glow, mood-tinted composer gradient, and animated typing/waveform states
- Keyboard focus rings on every control, `prefers-reduced-motion` support, and touch-friendly fallbacks where hover isn't available

---

## Tech Stack

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
├── docs/                      # Demo video and screenshots
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

> Voice input uses the browser's Speech Recognition API, which is Chromium-only (Chrome, Edge). In other browsers the mic button hides itself and everything else works as normal.

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

- Chat data, settings, and mood logs live in browser `localStorage`. They're namespaced per account, so accounts don't see each other's history on a shared browser, but nothing is stored server-side — so there's still no sync across devices, and clearing site data wipes everything
- The emotion classifier is English-trained; results on other languages are not validated
- Can only detect one emotion at a time (No multiple emotions)
- Speech recognition and speech synthesis depend on the browser's built-in engines, so voice quality and language support vary by platform
- Free-tier API rate limits apply (Groq)

---

## Possible Future Work

- Migrate chat/settings storage from `localStorage` to per-user database records
- Fine-tune the emotion classifier (e.g. via LoRA) specifically to address the implicit-anger weakness identified in evaluation
- Expand the benchmark test set for more statistically robust accuracy claims

---

## License

This project was built for educational and portfolio purposes.
