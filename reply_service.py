from groq import Groq

class ReplyService:
    def __init__(self):
        self.client = Groq()

    def generate_reply(self, text, emotion):
        prompt = (
            f"A user wrote this journal entry: \"{text}\"\n"
            f"Their detected emotion is: {emotion}\n"
            f"Write a warm, thoughtful, supportive reply (5-7 sentences), "
            f"as if you're a caring friend reading their journal."
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