from transformers import pipeline


class EmotionService:
    def __init__(self):
        self.classifier = pipeline(
            "text-classification",
            model="j-hartmann/emotion-english-distilroberta-base",
            truncation=True,
            max_length=512
        )

    def classify(self, text, confidence_threshold=0.35):
        """
        Returns the top predicted emotion and its confidence score.
        If the top prediction's confidence is below the threshold, falls back
        to 'neutral' instead of displaying an uncertain guess with false confidence.
        """
        results = self.classifier(text, top_k=None)
        top = results[0]

        if top['score'] < confidence_threshold:
            return "neutral", top['score']

        return top['label'], top['score']

    def classify_with_alternatives(self, text):
        """
        Returns every emotion label with its score, ranked highest to lowest.
        Useful for debugging misclassifications — lets you see whether a wrong
        top-1 prediction was a confident miss or a close call against the
        actual correct emotion.
        """
        results = self.classifier(text, top_k=None)
        return sorted(results, key=lambda x: x['score'], reverse=True)