import os
import re
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()

class ReplyService:
    def __init__(self):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ.get("OPENROUTER_API_KEY"),
        )
        # Tried in order — first one that returns a valid-looking reply wins
        self.model_fallback_chain = [
            "openrouter/free",
            "z-ai/glm-5.2:free",
            "qwen/qwen3.8-27b:free",
        ]
        self.app_url = os.environ.get("APP_URL", "http://127.0.0.1:5500")

    def _looks_like_garbage(self, text):
        """Catches leaked moderation/classifier metadata instead of a real reply."""
        if not text or not text.strip():
            return True
        garbage_patterns = [
            r"user safety\s*:",
            r"safety\s*:\s*(safe|unsafe)",
            r"^\s*\{.*\}\s*$",   # a bare JSON blob instead of prose
            r"content policy",
            r"moderation\s*result",
        ]
        lowered = text.lower()
        return any(re.search(pattern, lowered) for pattern in garbage_patterns)

    def _call_model(self, model, prompt):
        response = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            extra_headers={
                "HTTP-Referer": self.app_url,
                "X-Title": "Mood Ring Journal",
            },
        )
        return response.choices[0].message.content

    def _generate_with_fallback(self, prompt):
        last_error = None
        for model in self.model_fallback_chain:
            try:
                content = self._call_model(model, prompt)
                if not self._looks_like_garbage(content):
                    return content
                print(f"Model {model} returned garbage output, trying next fallback.")
            except Exception as e:
                last_error = e
                print(f"Model {model} failed: {e}")
        if last_error:
            print(f"All fallback models failed. Last error: {last_error}")
        return None

    def generate_reply(self, text, emotion):
        prompt = (
            f"Your friend just texted you this: \"{text}\"\n"
            f"You can tell they're feeling {emotion}.\n\n"
            f"Respond the way a genuinely emotionally intelligent friend would. Guidelines:\n"
            f"- First, actually engage with what they specifically said — not generic emotion talk\n"
            f"- Then, when it genuinely fits, offer something real: encouragement, a "
            f"different perspective, or a specific reassurance tied to what THEY said "
            f"(not a generic 'you're valid' line). Good friends don't just mirror feelings "
            f"back forever — they also help you see something you might be missing.\n"
            f"- Example of the difference: if someone with a great GPA says they feel like "
            f"they're falling behind, don't just describe that disconnect back to them — "
            f"actually push back on it a little, the way a friend who cares about you would\n"
            f"- Don't force positivity if the moment doesn't call for it — if someone just "
            f"needs to vent, let them vent without redirecting\n"
            f"- Use casual, everyday language and contractions, like a real text message\n"
            f"- Avoid clichés: no 'that's completely valid', 'I'm here for you', 'sending "
            f"you love'\n"
            f"- Don't default to asking a question every time — but it's fine to ask one "
            f"occasionally if it's specific and genuinely curious, not generic\n"
            f"- Match their energy and keep length natural, not always long\n\n"
            f"If what they wrote suggests they might be in real danger or crisis (not just "
            f"having a hard day), gently and naturally suggest talking to someone they "
            f"trust or a crisis line, without being clinical about it.\n"
            f"IMPORTANT: Reply in the SAME language/style the person wrote in. If they wrote "
            f"in Roman Urdu (Urdu written in English letters) or mixed English-Urdu, reply "
            f"naturally in Roman Urdu or mixed English-Urdu too, the way a real bilingual "
            f"friend would text back — don't switch to pure English.\n"
        )
        result = self._generate_with_fallback(prompt)
        if result is None:
            return "I'm having a little trouble finding the words right now — mind trying again in a moment?"
        return result

    def generate_title(self, text):
        title_prompt = (
            f"Summarize this journal entry into a short title, "
            f"3 to 5 words maximum, no punctuation, no quotation marks: "
            f"\"{text}\""
        )
        result = self._generate_with_fallback(title_prompt)
        if result is None:
            return "Untitled entry"
        return result.strip()