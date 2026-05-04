"""
=======================================================
  AI Song Finder — Mood Classification Model  v3.0
  TF-IDF Vectorization + Multinomial Naive Bayes
=======================================================
"""

# ── Step 1: All Imports at the Top ─────────────────────────────────────────
import random
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.pipeline import Pipeline


# ── Step 2: Labeled Dataset (50 samples per class = 200 total) ─────────────
# Each sentence maps to: happy | sad | calm | energetic

data = {

    "happy": [
        "I feel so happy today",
        "Everything is going great",
        "I am so joyful right now",
        "Life is wonderful and beautiful",
        "I am on top of the world",
        "This is the best day ever",
        "I feel cheerful and positive",
        "I am delighted and overjoyed",
        "I cannot stop smiling",
        "I feel great and amazing",
        "Things are going perfectly",
        "I am thrilled about today",
        "I feel blessed and grateful",
        "My heart is full of joy",
        "I am in a fantastic mood",
        "I feel wonderful today",
        "I am so glad everything worked out",
        "I feel like celebrating",
        "What a lovely and bright day",
        "I am so pleased with how things turned out",
        "I feel ecstatic and full of life",
        "I woke up feeling so good",
        "I feel lucky and thankful",
        "I am beaming with happiness",
        "I feel upbeat and joyful",
        "Everything makes me smile today",
        "I feel radiant and full of positivity",
        "I had such a wonderful experience",
        "I feel like the luckiest person alive",
        "I am absolutely loving this day",
        "I feel jubilant and content",
        "My mood is on cloud nine",
        "I feel so satisfied and fulfilled",
        "I am glowing with happiness",
        "Life feels absolutely perfect right now",
        "I am laughing and having a great time",
        "I feel playful and lighthearted",
        "I just got amazing news",
        "I feel so alive and vibrant",
        "I am bursting with happiness",
        "I feel sunny and bright inside",
        "I had the most wonderful day",
        "I am grateful for every moment",
        "I feel merry and full of cheer",
        "I just feel really good about everything",
        "I am in a really good place emotionally",
        "I feel enthusiastic about what is ahead",
        "I feel triumphant and successful",
        "I feel warm and appreciated",
        "I am proud and happy with myself",
    ],

    "sad": [
        "I feel really sad and lonely",
        "Everything feels hopeless",
        "I am so depressed right now",
        "Nothing is going right for me",
        "I feel empty inside",
        "I am heartbroken and hurt",
        "I just want to cry",
        "I feel miserable and down",
        "I have lost all hope",
        "I feel blue and gloomy",
        "I am overwhelmed with grief",
        "I feel like nobody cares",
        "I am feeling very low today",
        "My heart hurts so much",
        "I feel broken and lost",
        "I cannot stop thinking about my loss",
        "I feel defeated and exhausted",
        "Nothing brings me joy anymore",
        "I feel so alone in this world",
        "I miss the way things used to be",
        "I feel deep sadness that will not go away",
        "I am crushed and disappointed",
        "Everything seems dark and heavy",
        "I feel numb and disconnected",
        "I cannot find any reason to smile",
        "I feel sorrowful and mourning",
        "I am in so much emotional pain",
        "I just want to disappear",
        "I feel abandoned and unwanted",
        "My world feels like it is falling apart",
        "I have been crying all day",
        "I feel like a burden to everyone",
        "I feel like I have failed",
        "I carry so much sadness inside me",
        "I feel tired of being unhappy",
        "I feel weighed down by everything",
        "I have no motivation and feel hopeless",
        "I feel like nothing will ever get better",
        "I feel a deep ache that I cannot shake",
        "I am drowning in my own thoughts",
        "I feel desperate and without purpose",
        "I feel utterly helpless",
        "Everything makes me want to weep",
        "I am consumed by sorrow",
        "I feel forgotten and invisible",
        "I feel regret about so many things",
        "I am grieving and cannot move forward",
        "I feel like giving up",
        "I feel hollow and without joy",
        "I feel so much pain inside",
    ],

    "calm": [
        "I feel very relaxed and peaceful",
        "Everything is quiet and serene",
        "I am at peace with myself",
        "I feel so tranquil right now",
        "I am in a very calm state",
        "I feel mellow and stress-free",
        "I just want to sit and breathe",
        "Nothing is bothering me today",
        "I feel centered and balanced",
        "I am totally at ease",
        "I feel gentle and collected",
        "I am in a meditative mood",
        "I feel still and undisturbed",
        "I am very comfortable and relaxed",
        "I feel soft and soothed",
        "I feel completely at peace",
        "My mind is quiet and still",
        "I feel grounded and steady",
        "I am enjoying a quiet moment",
        "I feel serene and undistracted",
        "Everything feels light and unhurried",
        "I feel refreshed and calm after a walk",
        "I am breathing slowly and feeling fine",
        "I feel no stress or anxiety right now",
        "I feel cozy and relaxed at home",
        "I am just unwinding and taking it easy",
        "I feel like floating on a calm sea",
        "I am completely present and mindful",
        "I feel settled and free from worry",
        "I am in a state of quiet contentment",
        "I feel rested and composed",
        "I feel very zen and undisturbed",
        "I am enjoying the stillness around me",
        "I feel harmonious and well-balanced",
        "I feel unhurried and perfectly calm",
        "I am soaking in the peaceful silence",
        "I feel fluid and easygoing today",
        "Everything is just as it should be",
        "I feel a quiet sense of happiness",
        "I am not rushing or worrying at all",
        "I feel comfortable and tension-free",
        "I have a calm and clear mind",
        "I feel so incredibly at peace",
        "I am fully relaxed in body and mind",
        "I feel light and carefree",
        "I am in a deeply restful mood",
        "I feel untroubled and open-hearted",
        "I am at ease with the world around me",
        "I feel collected and quietly joyful",
        "I feel a gentle warmth and contentment",
    ],

    "energetic": [
        "I feel pumped up and ready to go",
        "I have so much energy right now",
        "I am fired up and motivated",
        "I want to run and jump around",
        "I feel unstoppable today",
        "I am hyped and super active",
        "I am bursting with energy",
        "I feel electric and charged up",
        "I am ready to crush my workout",
        "I feel powerful and driven",
        "I am so excited and energized",
        "I want to dance and move around",
        "I feel active and alert",
        "I am pumped and full of adrenaline",
        "I feel like I can achieve anything",
        "I feel high energy and ready to hustle",
        "I am wired and raring to go",
        "I feel turbo-charged and unstoppable",
        "I am absolutely full of vigor and strength",
        "I feel like running a marathon",
        "I have so much drive and enthusiasm",
        "I feel on fire and absolutely motivated",
        "I am ready to take on any challenge",
        "I feel sharp, fast, and full of life",
        "I am highly charged and eager to act",
        "I feel like sprinting and not stopping",
        "I am excited and cannot hold still",
        "I feel superhuman strength and energy",
        "I am amped up and ready to perform",
        "I feel explosive power in every step",
        "I am fully awake and buzzing with energy",
        "I feel electrified and unstoppable",
        "I am thriving and pushing hard",
        "I feel alive and wildly energetic",
        "I am going at full throttle right now",
        "I feel intense focus and raw energy",
        "I am bursting to get moving",
        "I feel the rush of adrenaline pumping",
        "I am energized and cannot sit still",
        "I feel revved up and raring to go",
        "I am crushing goals with full energy",
        "I feel dynamic and full of momentum",
        "I am excited and moving fast",
        "I feel enthusiastic and driven right now",
        "I am switched on and full of power",
        "I feel turbocharged with excitement",
        "I want to hit the gym and push my limits",
        "I am in beast mode and loving it",
        "I feel the fire within me burning bright",
        "I am totally amped and ready to hustle",
    ],
}

# Verify all classes have exactly 50 samples
for mood_name, texts in data.items():
    assert len(texts) == 50, f"ERROR: '{mood_name}' has {len(texts)} samples, expected 50"

# Flatten dict → (sentences list, labels list)
sentences, labels = [], []
for mood_name, texts in data.items():
    for text in texts:
        sentences.append(text)
        labels.append(mood_name)

sentences = np.array(sentences)
labels    = np.array(labels)


# ── Step 3: Build Scikit-learn Pipeline ────────────────────────────────────
# Pipeline chains TF-IDF → MultinomialNB together.
# Benefit: vectorizer is fit ONLY on training data (no data leakage).
#
# Vectorizer settings:
#   stop_words=None    → keep all words (emotion words like "sad", "feel" matter)
#   ngram_range=(1,1)  → single words only (bigrams hurt on small datasets)
#   sublinear_tf=True  → log(1+tf) reduces dominance of very frequent words
#   min_df=1           → include every token (small dataset, keep all vocab)

pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(
        lowercase=True,
        stop_words=None,
        ngram_range=(1, 1),
        sublinear_tf=True,
        min_df=1,
        analyzer="word",
    )),
    ("clf", MultinomialNB(alpha=1.0)),  # Laplace smoothing handles unseen words
])


# ── Step 4: Stratified Train / Test Split ──────────────────────────────────
# 80% train (40 per class), 20% test (10 per class)
# stratify=labels → equal class distribution in both sets

X_train, X_test, y_train, y_test = train_test_split(
    sentences, labels,
    test_size=0.20,
    random_state=42,
    stratify=labels,
)

print("=" * 60)
print("  AI Song Finder — Mood Classifier  v3.0")
print("=" * 60)
print(f"\n  Total samples  : {len(sentences)} ({len(data)} classes x 50 each)")
print(f"  Training set   : {len(X_train)} samples")
print(f"  Test set       : {len(X_test)} samples\n")


# ── Step 5: Train the Model ─────────────────────────────────────────────────
# pipeline.fit() runs TF-IDF on X_train, then trains Naive Bayes.

pipeline.fit(X_train, y_train)
print("  [OK] Model trained successfully!\n")


# ── Step 6: 5-Fold Cross-Validation ────────────────────────────────────────
# More reliable than a single train/test split.
# StratifiedKFold keeps class balance in every fold.

cv        = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = cross_val_score(pipeline, sentences, labels, cv=cv, scoring="accuracy")

print("  5-Fold Cross-Validation:")
print(f"  Fold Scores : {[f'{s*100:.1f}%' for s in cv_scores]}")
print(f"  Mean        : {cv_scores.mean()*100:.2f}%")
print(f"  Std Dev     : +/-{cv_scores.std()*100:.2f}%\n")


# ── Step 7: Evaluate on Held-Out Test Set ──────────────────────────────────
y_pred   = pipeline.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"  Test Accuracy : {accuracy * 100:.2f}%\n")

print("  Classification Report:")
print("-" * 60)
print(classification_report(
    y_test, y_pred,
    target_names=sorted(data.keys()),
    digits=2,
))

# Confusion Matrix
print("  Confusion Matrix (rows=actual, cols=predicted):")
class_names = sorted(data.keys())
print(f"  {'':12}", end="")
for c in class_names:
    print(f"{c:>11}", end="")
print()
cm = confusion_matrix(y_test, y_pred, labels=class_names)
for i, row_label in enumerate(class_names):
    print(f"  {row_label:12}", end="")
    for val in cm[i]:
        print(f"{val:>11}", end="")
    print()
print()


# ── Step 8: Song Genre Mapping ─────────────────────────────────────────────
mood_suggestions = {
    "happy":     "Upbeat pop, Bollywood hits, feel-good dance tracks",
    "sad":       "Soulful ballads, acoustic, lo-fi chill, ghazals",
    "calm":      "Ambient, classical, jazz, meditation, soft instrumental",
    "energetic": "EDM, hip-hop, Punjabi beats, rock, workout anthems",
}


# ── Step 8b: Friendly AI Advice Per Mood ───────────────────────────────────
# 4 rotating suggestions per mood — one is picked randomly each time.

mood_advice = {
    "happy": [
        "You're radiating great energy! Keep that smile going and share it with someone today. :)",
        "Love the good vibes! This is the perfect moment to do something you truly enjoy.",
        "You're in a great place — ride this wave and make something memorable today!",
        "Happiness looks good on you! Celebrate the little wins and keep spreading joy.",
    ],
    "sad": [
        "It's okay to feel this way — give yourself some grace. Try calming music and rest; things will get better.",
        "You don't have to be okay all the time. Take a deep breath and be kind to yourself.",
        "Tough moments don't last forever. A soothing playlist might be just what you need right now.",
        "Feeling sad is valid. Be gentle with yourself today — healing takes time and that's perfectly fine.",
    ],
    "calm": [
        "You're in a beautiful state of peace — embrace it! Soft music will make this moment even more perfect.",
        "That calm energy is precious. Use it to reflect, create, or simply enjoy the stillness around you.",
        "What a serene headspace to be in! Pair it with ambient music and let your mind wander freely.",
        "You're centred and balanced — a rare gift. Take a mindful moment and savour this tranquility.",
    ],
    "energetic": [
        "You're on fire! Channel that energy into something productive — now is the time to crush your goals.",
        "High energy mode: activated! A pumped-up playlist will keep that momentum going all day long.",
        "Unstoppable! Whether it's a workout or a project — go for it with full power!",
        "Love that electric energy! Put on a high-BPM track and make the most of this amazing feeling.",
    ],
}


def get_advice(mood):
    """Return a random friendly suggestion for the detected mood."""
    return random.choice(mood_advice[mood])


# ── Step 9: Prediction Function ─────────────────────────────────────────────
def predict_mood(user_text):
    """
    Predict the mood of a free-text sentence.

    Args:
        user_text (str): A sentence describing how the user feels.

    Returns:
        mood (str)       : Predicted mood (happy / sad / calm / energetic).
        confidence (float): Confidence as a percentage (0-100).
        all_probs (dict) : Probability scores for all 4 moods.
        advice (str)     : A short friendly AI suggestion.
    """
    # Vectorize and classify in one step using the pipeline
    probs_array = pipeline.predict_proba([user_text])[0]
    classes     = pipeline.classes_

    mood       = classes[np.argmax(probs_array)]
    confidence = float(max(probs_array)) * 100
    all_probs  = {c: round(float(p) * 100, 1) for c, p in zip(classes, probs_array)}
    advice     = get_advice(mood)

    return mood, confidence, all_probs, advice


# ── Step 10: Interactive Mood Input Loop ────────────────────────────────────
def main():
    print("=" * 60)
    print("  AI Song Finder — Mood Predictor")
    print("=" * 60)
    print("  Tell me how you feel and I will suggest music for you.")
    print("  Type 'quit' or 'exit' to stop.\n")

    while True:
        user_input = input("  How are you feeling? --> ").strip()

        # Exit condition
        if user_input.lower() in ("quit", "exit", "q"):
            print("\n  Goodbye! Enjoy your music.\n")
            break

        # Skip empty input
        if not user_input:
            print("  [!] Please type a sentence describing your mood.\n")
            continue

        # Run prediction
        mood, confidence, all_probs, advice = predict_mood(user_input)

        print(f"\n  Detected Mood  : {mood.upper()}  ({confidence:.1f}% confidence)")
        print(f"\n  AI Suggestion  : {advice}")
        print(f"\n  Music For You  : {mood_suggestions[mood]}")
        print(f"\n  Mood Breakdown :")
        for m, prob in sorted(all_probs.items(), key=lambda x: -x[1]):
            filled = int(prob / 5)
            bar    = "#" * filled + "-" * (20 - filled)
            print(f"    {m:>10}  [{bar}]  {prob:.1f}%")
        print("-" * 60 + "\n")


if __name__ == "__main__":
    main()
