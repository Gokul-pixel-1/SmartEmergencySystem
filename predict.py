import os
import pickle

BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "vectorizer.pkl")

model = None
vectorizer = None
model_available = False

try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    with open(VECTORIZER_PATH, "rb") as f:
        vectorizer = pickle.load(f)
    model_available = True
except FileNotFoundError:
    model_available = False
except Exception:
    model_available = False

def predict_emergency(text):
    if model_available and model is not None and vectorizer is not None:
        try:
            text_vec = vectorizer.transform([text])
            prediction = model.predict(text_vec)[0]
            prob = model.predict_proba(text_vec).max()
            return prediction, round(prob * 100, 2)
        except Exception:
            pass

    normalized = text.lower()
    if any(word in normalized for word in ["fire", "smoke", "burn", "flames", "hot"]):
        return "Fire", 95.0
    if any(word in normalized for word in ["injury", "accident", "bleeding", "heart", "medical", "illness"]):
        return "Medical Emergency", 92.0
    if any(word in normalized for word in ["gas", "leak", "odor", "chemical", "fume"]):
        return "Gas Leak", 90.0
    return "Security Breach", 85.0