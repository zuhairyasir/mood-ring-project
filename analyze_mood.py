import pandas as pd
import matplotlib.pyplot as plt
import json

with open("mood_log.json", "r") as f:
    data = json.load(f)

df = pd.DataFrame(data)

df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
emotion_counts = df["emotion"].value_counts()

plt.figure(figsize=(8, 5))
emotion_counts.plot(kind="bar", color="#4a4a6a")
plt.title("Emotion Frequency — All Entries")
plt.xlabel("Emotion")
plt.ylabel("Number of Entries")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("emotion_frequency.png")  
plt.show()

plt.figure(figsize=(10, 5))
plt.plot(df["timestamp"], df["confidence"], marker="o", color="#4a4a6a")
plt.title("Model Confidence Over Time")
plt.xlabel("Time")
plt.ylabel("Confidence Score")
plt.ylim(0, 1)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("confidence_over_time.png")
plt.show()

print(f"Analyzed {len(df)} entries.")
print(f"Most common emotion: {emotion_counts.idxmax()}")