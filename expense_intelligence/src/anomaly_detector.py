import os
import joblib
import pandas as pd
from sklearn.ensemble import IsolationForest

MODEL_PATH = "models/anomaly_detector.pkl"


def train_anomaly_detector(df: pd.DataFrame):
    os.makedirs("models", exist_ok=True)
    X = df[["amount", "month", "weekday"]].values
    contamination = min(0.1, max(0.01, 2 / max(len(df), 1)))
    iso = IsolationForest(contamination=contamination, random_state=42)
    iso.fit(X)
    joblib.dump(iso, MODEL_PATH)
    return iso


def detect_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    if not os.path.exists(MODEL_PATH) or len(df) < 5:
        return pd.DataFrame()
    iso = joblib.load(MODEL_PATH)
    X = df[["amount", "month", "weekday"]].values
    df = df.copy()
    df["anomaly_score"] = iso.decision_function(X)
    df["is_anomaly"]    = iso.predict(X) == -1
    return df[df["is_anomaly"]].copy()