DEFAULT_THRESHOLDS = {
    "Food":          5000,
    "Shopping":      8000,
    "Travel":        6000,
    "Utilities":     3000,
    "Health":        4000,
    "Entertainment": 3000,
    "Other":         5000,
}


def check_overspending(df, thresholds: dict | None = None) -> list:
    if thresholds is None:
        thresholds = DEFAULT_THRESHOLDS

    alerts = []
    cat_totals = df.groupby("category")["amount"].sum()

    for category, spent in cat_totals.items():
        limit = thresholds.get(category, 10000)
        if spent > limit:
            pct = ((spent - limit) / limit) * 100
            level = "critical" if pct > 50 else "warning"
            alerts.append({
                "category": category,
                "spent":    round(spent, 2),
                "limit":    limit,
                "excess":   round(spent - limit, 2),
                "pct_over": round(pct, 1),
                "level":    level,
                "message":  (
                    f"{category}: ₹{spent:,.0f} spent vs ₹{limit:,} limit "
                    f"(+{pct:.0f}% over)"
                ),
            })
    return alerts


def check_daily_spike(df, multiplier: float = 2.5) -> list:
    """Flag days where spending is > multiplier × average daily spending."""
    daily = df.groupby("date")["amount"].sum()
    mean  = daily.mean()
    spikes = daily[daily > mean * multiplier]
    return [
        {
            "date":    str(d.date()),
            "amount":  round(v, 2),
            "message": f"Spending spike on {d.strftime('%d %b')}: ₹{v:,.0f} (avg ₹{mean:,.0f})",
        }
        for d, v in spikes.items()
    ]