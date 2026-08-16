from groq import Groq

class ReplyService:
    def __init__(self):
        self.client = Groq()

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
        )
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    def generate_title(self, text):
        title_prompt = (
            f"Summarize this journal entry into a short title, "
            f"3 to 5 words maximum, no punctuation, no quotation marks: "
            f"\"{text}\""
        )
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": title_prompt}]
        )
        return response.choices[0].message.content.strip()