# Mood-Ring Journal — Technical Evaluation

## Emotion Classifier Accuracy

- **Test set size:** 20 hand-labeled sentences
- **Accuracy:** 80.0% (16/20 correct)

### Per-Emotion Accuracy

| Emotion | Correct | Total | Accuracy |
|---|---|---|---|
| anger | 5 | 8 | 62.5% |
| disgust | 2 | 2 | 100.0% |
| fear | 2 | 2 | 100.0% |
| joy | 2 | 2 | 100.0% |
| neutral | 1 | 2 | 50.0% |
| sadness | 2 | 2 | 100.0% |
| surprise | 2 | 2 | 100.0% |

- **Note:** This is a small, hand-crafted sanity-check set, not a large validated benchmark. Results should be read as directional, not definitive.

### Misclassifications

| Text | Expected | Predicted | Confidence |
|---|---|---|---|
| I can't believe they cancelled my flight with no warning! | anger | surprise | 76.3% |
| I went to the store and bought some groceries. | neutral | joy | 54.9% |
| He walked away without even apologizing after breaking my phone. | anger | disgust | 49.1% |
| I've asked them three times to fix this and nothing has changed. | anger | neutral | 75.5% |

## Latency (10 runs for classifier, 5 runs for Groq calls)

| Stage | Mean (s) | Min (s) | Max (s) |
|---|---|---|---|
| Emotion classification (local) | 0.027 | 0.024 | 0.039 |
| Groq reply generation | 0.769 | 0.568 | 1.002 |
| Groq title generation | 0.167 | 0.094 | 0.411 |

## Discussion & Known Limitations

The classifier's weakest category is **anger** (62.5%, 5/8), well below every other emotion in this test set (100% for joy, sadness, fear, disgust, surprise; 50% for neutral on a very small n=2 sample). Examining the specific failures is informative: two of the three anger misclassifications were sentences expressing anger *implicitly*, through described behavior rather than explicit angry vocabulary (e.g. "walked away without apologizing," "asked three times and nothing has changed") — these were misread as disgust and neutral, respectively. The third failure involved a sentence combining anger with disbelief-marker phrasing ("I can't believe..."), which was misread as surprise. This suggests the model relies heavily on explicit emotional vocabulary and struggles when anger must be inferred from context or action rather than stated directly.

**Caveat:** with only 8 anger examples, this finding should be treated as a credible signal worth further investigation, not a statistically robust conclusion — a proper validation would require a much larger, ideally independently-labeled dataset specifically targeting implicit vs. explicit emotional expression.
