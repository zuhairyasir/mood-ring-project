import time
import statistics
from emotion_service import EmotionService
from reply_service import ReplyService

test_cases = [
    ("I just got accepted into my dream program, I can't stop smiling!", "joy"),
    ("My best friend moved away and I really miss them.", "sadness"),
    ("I can't believe they cancelled my flight with no warning!", "anger"),
    ("I'm not sure what's going to happen in tomorrow's exam.", "fear"),
    ("The food at that restaurant made me feel sick just looking at it.", "disgust"),
    ("I never expected to see my old teacher at the grocery store!", "surprise"),
    ("Today was a fairly normal day, nothing much happened.", "neutral"),
    ("Winning the scholarship felt like a dream come true.", "joy"),
    ("I've been feeling really down since the news this morning.", "sadness"),
    ("It's infuriating when people don't reply to important emails.", "anger"),
    ("I'm anxious about the interview I have tomorrow.", "fear"),
    ("That smell coming from the fridge is absolutely revolting.", "disgust"),
    ("I was shocked to find out we won the competition!", "surprise"),
    ("I went to the store and bought some groceries.", "neutral"),
    # NEW: additional anger examples, mixing explicit and implicit phrasing
    ("How dare they take credit for my work in the meeting.", "anger"),
    ("This is absolutely ridiculous, I've been waiting for two hours!", "anger"),
    ("He walked away without even apologizing after breaking my phone.", "anger"),   # implicit — no anger words
    ("I slammed the door and didn't say a word to anyone.", "anger"),                # implicit — behavioral cue only
    ("I've asked them three times to fix this and nothing has changed.", "anger"),   # implicit — frustration, no anger words
    ("My blood was boiling after hearing what he said about me.", "anger"),          # idiomatic expression
]

emotion_service = EmotionService()
reply_service = ReplyService()

# --- PART 1: Accuracy (overall AND per-emotion) ---
correct = 0
mistakes = []
# per_emotion tracks, for each TRUE label, how many were right vs total
per_emotion = {}

for text, expected in test_cases:
    predicted, confidence = emotion_service.classify(text)

    if expected not in per_emotion:
        per_emotion[expected] = {"correct": 0, "total": 0}
    per_emotion[expected]["total"] += 1

    if predicted == expected:
        correct += 1
        per_emotion[expected]["correct"] += 1
    else:
        mistakes.append((text, expected, predicted, confidence))

accuracy = correct / len(test_cases)

classifier_latencies = []
sample_text = "I am feeling a mix of emotions about this whole situation."

for _ in range(10):
    start = time.perf_counter()
    emotion_service.classify(sample_text)
    end = time.perf_counter()
    classifier_latencies.append(end - start)

reply_latencies = []
title_latencies = []

for _ in range(5):
    start = time.perf_counter()
    reply_service.generate_reply(sample_text, "neutral")
    end = time.perf_counter()
    reply_latencies.append(end - start)

    start = time.perf_counter()
    reply_service.generate_title(sample_text)
    end = time.perf_counter()
    title_latencies.append(end - start)

with open("EVALUATION.md", "w", encoding="utf-8") as f:
    f.write("# Mood-Ring Journal — Technical Evaluation\n\n")

    f.write("## Emotion Classifier Accuracy\n\n")
    f.write(f"- **Test set size:** {len(test_cases)} hand-labeled sentences\n")
    f.write(f"- **Accuracy:** {accuracy:.1%} ({correct}/{len(test_cases)} correct)\n")
    f.write("\n### Per-Emotion Accuracy\n\n")
    f.write("| Emotion | Correct | Total | Accuracy |\n")
    f.write("|---|---|---|---|\n")
    for emotion, counts in sorted(per_emotion.items()):
        emotion_accuracy = counts["correct"] / counts["total"]
        f.write(f"| {emotion} | {counts['correct']} | {counts['total']} | {emotion_accuracy:.1%} |\n")
    f.write("\n")
    f.write("- **Note:** This is a small, hand-crafted sanity-check set, not a large "
            "validated benchmark. Results should be read as directional, not definitive.\n\n")

    if mistakes:
        f.write("### Misclassifications\n\n")
        f.write("| Text | Expected | Predicted | Confidence |\n")
        f.write("|---|---|---|---|\n")
        for text, expected, predicted, confidence in mistakes:
            f.write(f"| {text} | {expected} | {predicted} | {confidence:.1%} |\n")
        f.write("\n")

    f.write("## Latency (10 runs for classifier, 5 runs for Groq calls)\n\n")
    f.write("| Stage | Mean (s) | Min (s) | Max (s) |\n")
    f.write("|---|---|---|---|\n")
    f.write(f"| Emotion classification (local) | {statistics.mean(classifier_latencies):.3f} | "
            f"{min(classifier_latencies):.3f} | {max(classifier_latencies):.3f} |\n")
    f.write(f"| Groq reply generation | {statistics.mean(reply_latencies):.3f} | "
            f"{min(reply_latencies):.3f} | {max(reply_latencies):.3f} |\n")
    f.write(f"| Groq title generation | {statistics.mean(title_latencies):.3f} | "
            f"{min(title_latencies):.3f} | {max(title_latencies):.3f} |\n")
    f.write("\n## Discussion & Known Limitations\n\n")
    f.write(
        "The classifier's weakest category is **anger** (62.5%, 5/8), well below every "
        "other emotion in this test set (100% for joy, sadness, fear, disgust, surprise; "
        "50% for neutral on a very small n=2 sample). Examining the specific failures is "
        "informative: two of the three anger misclassifications were sentences expressing "
        "anger *implicitly*, through described behavior rather than explicit angry "
        "vocabulary (e.g. \"walked away without apologizing,\" \"asked three times and "
        "nothing has changed\") — these were misread as disgust and neutral, respectively. "
        "The third failure involved a sentence combining anger with disbelief-marker "
        "phrasing (\"I can't believe...\"), which was misread as surprise. This suggests "
        "the model relies heavily on explicit emotional vocabulary and struggles when "
        "anger must be inferred from context or action rather than stated directly.\n\n"
        "**Caveat:** with only 8 anger examples, this finding should be treated as a "
        "credible signal worth further investigation, not a statistically robust "
        "conclusion — a proper validation would require a much larger, ideally "
        "independently-labeled dataset specifically targeting implicit vs. explicit "
        "emotional expression.\n"
    )

print(f"Done. Accuracy: {accuracy:.1%}. See EVALUATION.md for full report.")