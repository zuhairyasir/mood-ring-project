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