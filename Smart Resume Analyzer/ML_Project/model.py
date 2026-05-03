import pickle
import os

# ============================================
# LOAD MODEL & VECTORIZER
# ============================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(BASE_DIR, "model.pkl")
vectorizer_path = os.path.join(BASE_DIR, "vectorizer.pkl")

model = pickle.load(open(model_path, "rb"))
vectorizer = pickle.load(open(vectorizer_path, "rb"))


# ============================================
# SINGLE PREDICTION
# ============================================
def predict_category(resume_text):
    if not resume_text:
        return "Unknown"

    text = vectorizer.transform([resume_text.lower()])
    prediction = model.predict(text)
    return prediction[0]


# ============================================
# TOP-K PREDICTIONS
# ============================================
def predict_top_k(resume_text, k=3):
    if not resume_text:
        return []

    text = vectorizer.transform([resume_text.lower()])

    scores = model.decision_function(text)[0]
    labels = model.classes_

    top_indices = scores.argsort()[-k:][::-1]

    results = []
    for i in top_indices:
        results.append((labels[i], float(scores[i])))

    return results