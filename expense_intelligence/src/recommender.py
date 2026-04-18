import pandas as pd


def generate_recommendations(
    df: pd.DataFrame,
    alerts: list,
    anomalies: pd.DataFrame,
    mode: str = "day",
) -> list:
    """
    Returns list of dicts: {level: 'error'|'warning'|'info', text: str}
    """
    recs = []
    if df.empty:
        return [{"level": "info", "text": " Add more expenses to get insights."}]

    cat_totals  = df.groupby("category")["amount"].sum()
    total_spent = cat_totals.sum()

    # ── Period comparison ──────────────────────────────────────────────────
    df = df.sort_values("date")
    if mode == "day":
        mid  = df["date"].min() + (df["date"].max() - df["date"].min()) / 2
        prev = df[df["date"] <= mid]["amount"].sum()
        curr = df[df["date"] > mid]["amount"].sum()
        period_label = "second half vs first half"
    else:
        months = sorted(df["month_name"].unique())
        if len(months) >= 2:
            prev = df[df["month_name"] == months[-2]]["amount"].sum()
            curr = df[df["month_name"] == months[-1]]["amount"].sum()
            period_label = f"{months[-1]} vs {months[-2]}"
        else:
            prev, curr = 0, total_spent
            period_label = "current period"

    if prev > 0:
        change_pct = ((curr - prev) / prev) * 100
        if abs(change_pct) > 5:
            direction = "increased" if change_pct > 0 else "decreased"
            level = "error" if change_pct > 25 else ("warning" if change_pct > 10 else "info")
            recs.append({
                "level": level,
                "text":  f"📈 Spending {direction} by {abs(change_pct):.1f}% ({period_label}).",
            })

    # ── Dominant category ──────────────────────────────────────────────────
    if not cat_totals.empty:
        top_cat = cat_totals.idxmax()
        top_pct = (cat_totals[top_cat] / total_spent) * 100
        if top_pct > 35:
            recs.append({
                "level": "warning",
                "text":  f" {top_cat} dominates your expenses at {top_pct:.1f}% of total.",
            })

    # ── High-share categories ──────────────────────────────────────────────
    for cat, amt in cat_totals.items():
        pct = (amt / total_spent) * 100
        if pct > 40 and cat != cat_totals.idxmax():
            recs.append({
                "level": "warning",
                "text":  f"💡 {cat} is {pct:.1f}% of spending — consider a monthly cap.",
            })

    # ── Weekend spending ───────────────────────────────────────────────────
    if "is_weekend" in df.columns:
        wknd = df[df["is_weekend"]]["amount"].sum()
        wkdy = df[~df["is_weekend"]]["amount"].sum()
        if wknd > 0 and wkdy > 0:
            wknd_pct = (wknd / total_spent) * 100
            if wknd_pct > 40:
                recs.append({
                    "level": "warning",
                    "text":  f"🎉 High weekend spending detected: {wknd_pct:.1f}% of total.",
                })

    # ── Overspend alerts ───────────────────────────────────────────────────
    for a in alerts:
        recs.append({
            "level": "error",
            "text":  f"🚨 {a['category']} over budget by ₹{a['excess']:,.0f} (+{a['pct_over']}%).",
        })

    # ── Anomalies ──────────────────────────────────────────────────────────
    if not anomalies.empty:
        recs.append({
            "level": "error",
            "text":  f"🔍 {len(anomalies)} unusual transaction(s) detected. Review for errors.",
        })

    # ── Generic tips ───────────────────────────────────────────────────────
    recs.append({"level": "info", "text": "📅 Track daily — small amounts compound quickly."})
    recs.append({"level": "info", "text": "💰 50/30/20 rule: 50% needs · 30% wants · 20% savings."})

    return recs