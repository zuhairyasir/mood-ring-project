from transformers import pipeline

class EmotionService:
    def __init__(self):
        self.classifier = pipeline(
            "text-classification",
            model="j-hartmann/emotion-english-distilroberta-base"
        )
 def classify(self, text):
        result = self.classifier(text)
        emotion = result[0]['label']
        confidence = result[0]['score']
        return emotion, confidence 