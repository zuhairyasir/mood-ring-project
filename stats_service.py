import pandas as pd
import matplotlib
matplotlib.use("Agg") 
import matplotlib.pyplot as plt
import io

class StatsService:
    def generate_emotion_chart(self, entries):
        data = [{"emotion": e.emotion, "confidence": e.confidence, "timestamp": e.timestamp} for e in entries]
        df = pd.DataFrame(data)

        emotion_counts = df["emotion"].value_counts()

        fig, ax = plt.subplots(figsize=(8, 5))
        emotion_counts.plot(kind="bar", color="#4a4a6a", ax=ax)
        ax.set_title("Emotion Frequency")
        ax.set_xlabel("Emotion")
        ax.set_ylabel("Number of Entries")
        plt.xticks(rotation=0)
        plt.tight_layout()

        buffer = io.BytesIO()
        fig.savefig(buffer, format="png")
        plt.close(fig)  
        buffer.seek(0)  
        return buffer

    def generate_confidence_chart(self, entries):
        data = [{"emotion": e.emotion, "confidence": e.confidence, "timestamp": e.timestamp} for e in entries]
        df = pd.DataFrame(data)
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(df["timestamp"], df["confidence"], marker="o", color="#4a4a6a")
        ax.set_title("Model Confidence Over Time")
        ax.set_xlabel("Time")
        ax.set_ylabel("Confidence Score")
        ax.set_ylim(0, 1)
        plt.xticks(rotation=45)
        plt.tight_layout()

        buffer = io.BytesIO()
        fig.savefig(buffer, format="png")
        plt.close(fig)
        buffer.seek(0)
        return buffer