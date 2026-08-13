from transformers import pipeline
classifier = pipeline(
     "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base"
)
result = classifier("I am so excited for my MITACS internship application!")
print(result)