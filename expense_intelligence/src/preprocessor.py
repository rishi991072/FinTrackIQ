import pandas as pd


def load_and_preprocess(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.dropna(subset=["date", "amount"], inplace=True)
    df["description"] = df["description"].fillna("unknown")
    if "category" not in df.columns:
        df["category"] = "Other"
    else:
        df["category"] = df["category"].fillna("Other")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df.dropna(subset=["date"], inplace=True)

    df["year"]       = df["date"].dt.year
    df["month"]      = df["date"].dt.month
    df["day"]        = df["date"].dt.day
    df["weekday"]    = df["date"].dt.weekday
    df["is_weekend"] = df["weekday"].isin([5, 6])
    df["month_name"] = df["date"].dt.strftime("%b %Y")
    df["week"]       = df["date"].dt.isocalendar().week.astype(int)

    df = df[df["amount"] > 0].copy()
    df.sort_values("date", inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df