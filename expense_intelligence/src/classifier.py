import os
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split

MODEL_PATH = "models/classifier.pkl"

RULES: dict[str, list[str]] = {
    "Food":          ["lunch", "dinner", "breakfast", "coffee", "snack", "restaurant",
                      "pizza", "groceries", "chai", "biryani", "swiggy", "zomato",
                      "food", "eat", "meal", "cafe", "dhaba", "burger", "juice",
                      "vegetable", "milk", "bread", "rice", "dal", "sabzi"],
    "Travel":        ["uber", "ola", "taxi", "metro", "bus", "petrol", "flight",
                      "train", "cab", "auto", "rickshaw", "toll", "parking",
                      "fuel", "rapido", "bike", "travel", "ticket", "irctc"],
    "Shopping":      ["amazon", "clothes", "shoes", "electronics", "books", "zara",
                      "flipkart", "myntra", "shirt", "dress", "bag", "watch",
                      "gadget", "shopping", "meesho", "ajio", "nykaa"],
    "Utilities":     ["electricity", "water", "wifi", "mobile", "recharge", "gas",
                      "bill", "internet", "broadband", "phone", "sim", "dth",
                      "maintenance", "rent", "society"],
    "Health":        ["medicine", "doctor", "gym", "pharmacy", "hospital", "clinic",
                      "tablet", "fitness", "yoga", "health", "checkup", "test",
                      "apollo", "1mg", "netmeds"],
    "Entertainment": ["netflix", "movie", "spotify", "game", "concert",
                      "amazon prime", "hotstar", "show", "outing", "party",
                      "fun", "disney", "youtube", "event", "amusement"],
}


def rule_label(description: str) -> str:
    d = description.lower()
    for cat, kws in RULES.items():
        if any(kw in d for kw in kws):
            return cat
    return "Other"


def train_classifier(df: pd.DataFrame):
    os.makedirs("models", exist_ok=True)
    df = df.copy()
    if "category" not in df.columns or df["category"].isin(["Other", ""]).all():
        df["category"] = df["description"].apply(rule_label)

    X = df["description"].astype(str)
    y = df["category"].astype(str)

    if len(X) < 6:
        return None

    test_sz = 0.2 if len(X) >= 15 else 0
    if test_sz:
        X_tr, _, y_tr, _ = train_test_split(X, y, test_size=test_sz, random_state=42)
    else:
        X_tr, y_tr = X, y

    pipe = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), max_features=5000)),
        ("clf",   MultinomialNB()),
    ])
    pipe.fit(X_tr, y_tr)
    joblib.dump(pipe, MODEL_PATH)
    return pipe


def load_classifier():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return None


def predict_category(description: str, model=None) -> str:
    d = description.strip()
    # Rule-based first (fast & reliable for known keywords)
    rule = rule_label(d)
    if rule != "Other":
        return rule
    # Fall back to ML model
    if model is None:
        model = load_classifier()
    if model:
        try:
            return model.predict([d])[0]
        except Exception:
            pass
    return "Other"


def label_dataframe(df: pd.DataFrame, model=None) -> pd.DataFrame:
    df = df.copy()
    df["category"] = df["description"].astype(str).apply(
        lambda d: predict_category(d, model)
    )
    return df