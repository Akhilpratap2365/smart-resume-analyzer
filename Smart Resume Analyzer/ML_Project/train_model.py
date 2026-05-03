import pandas as pd
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report

# ============================================
# PATH SETUP
# ============================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "Resume.csv")

# ============================================
# LOAD DATASET
# ============================================
df = pd.read_csv(file_path)

# ============================================
# DATA CLEANING
# ============================================
df['Resume'] = df['Resume'].fillna("").str.lower()

X = df['Resume']
y = df['Category']

# ============================================
# TF-IDF VECTORIZATION
# ============================================
tfidf = TfidfVectorizer(stop_words='english', max_features=5000)
X_tfidf = tfidf.fit_transform(X)

# ============================================
# TRAIN TEST SPLIT (IMPROVED)
# ============================================
X_train, X_test, y_train, y_test = train_test_split(
    X_tfidf,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y   # ✅ important fix
)

# ============================================
# MODEL TRAINING
# ============================================
model = LinearSVC()
model.fit(X_train, y_train)

# ============================================
# SAVE MODEL
# ============================================
model_path = os.path.join(BASE_DIR, "model.pkl")
vectorizer_path = os.path.join(BASE_DIR, "vectorizer.pkl")

pickle.dump(model, open(model_path, "wb"))
pickle.dump(tfidf, open(vectorizer_path, "wb"))

# ============================================
# EVALUATION
# ============================================
y_pred = model.predict(X_test)

print("Model trained successfully!")
print("Accuracy:", model.score(X_test, y_test))
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))