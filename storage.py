import pandas as pd
from datetime import datetime

FILE = "incidents.csv"

def save_incident(text, label):
    try:
        df = pd.read_csv(FILE)
    except:
        df = pd.DataFrame(columns=["time", "text", "label"])

    new = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "text": text,
        "label": label
    }

    df = pd.concat([df, pd.DataFrame([new])], ignore_index=True)
    df.to_csv(FILE, index=False)

def load_incidents():
    try:
        return pd.read_csv(FILE)
    except:
        return pd.DataFrame(columns=["time", "text", "label"])