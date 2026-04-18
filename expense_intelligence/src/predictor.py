import os
import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

MODEL_PATH = "models/predictor.pkl"


def _monthly_series(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby(["year", "month"])["amount"]
        .sum()
        .reset_index()
        .assign(time_index=lambda x: range(len(x)))
    )


def train_predictor(df: pd.DataFrame) -> dict:
    os.makedirs("models", exist_ok=True)
    date_range = (df["date"].max() - df["date"].min()).days

    if date_range < 90:
        # Day-wise: rolling 7-day average
        daily = df.groupby("date")["amount"].sum().reset_index()
        daily = daily.sort_values("date").reset_index(drop=True)
        result = {"mode": "day", "daily": daily}
        joblib.dump(result, MODEL_PATH)
        return result
    else:
        # Month-wise: linear regression
        monthly = _monthly_series(df)
        X = monthly[["time_index"]]
        y = monthly["amount"]
        model = LinearRegression()
        model.fit(X, y)
        result = {
            "mode":       "month",
            "model":      model,
            "last_index": len(monthly) - 1,
            "monthly":    monthly,
        }
        joblib.dump(result, MODEL_PATH)
        return result


def predict(n_periods: int = 1) -> dict:
    """
    Returns dict with keys: mode, values (list of predicted amounts), labels (list of str)
    """
    if not os.path.exists(MODEL_PATH):
        return {"mode": "none", "values": [], "labels": []}

    data = joblib.load(MODEL_PATH)
    mode = data["mode"]

    if mode == "day":
        daily = data["daily"]
        window = daily["amount"].tail(7).values
        preds, labels = [], []
        last_date = daily["date"].max()
        for i in range(1, n_periods + 1):
            val = float(np.mean(window))
            preds.append(round(max(val, 0), 2))
            labels.append((last_date + pd.Timedelta(days=i)).strftime("%d %b"))
            window = np.append(window[1:], val)
        return {"mode": "day", "values": preds, "labels": labels}

    else:  # month
        model      = data["model"]
        last_index = data["last_index"]
        preds, labels = [], []
        for i in range(1, n_periods + 1):
            val = model.predict([[last_index + i]])[0]
            preds.append(round(max(val, 0), 2))
            labels.append(f"Month +{i}")
        return {"mode": "month", "values": preds, "labels": labels}