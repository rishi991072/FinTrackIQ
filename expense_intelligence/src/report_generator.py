from datetime import datetime


def generate_report(
    df,
    alerts: list,
    recommendations: list,
    budget_report: list,
    pred_result: dict,
    anomalies,
    period_label: str = "All Time",
) -> str:
    sep  = "=" * 64
    sep2 = "─" * 64
    lines = [
        sep,
        "   PERSONAL EXPENSE INTELLIGENCE — AI FINANCE REPORT",
        f"   Period   : {period_label}",
        f"   Generated: {datetime.now().strftime('%d %b %Y, %H:%M')}",
        sep,
    ]

    total = df["amount"].sum()
    avg   = df.groupby("date")["amount"].sum().mean() if not df.empty else 0
    lines += [
        f"\n  SUMMARY",
        sep2,
        f"  Total Spending  : ₹{total:,.2f}",
        f"  Transactions    : {len(df)}",
        f"  Avg per Day     : ₹{avg:,.2f}",
        f"  Unique Categories: {df['category'].nunique()}",
    ]

    lines += [f"\n  CATEGORY BREAKDOWN", sep2]
    for cat, amt in df.groupby("category")["amount"].sum().sort_values(ascending=False).items():
        pct = (amt / total * 100) if total else 0
        lines.append(f"  {cat:<18} ₹{amt:>10,.2f}   {pct:5.1f}%")

    lines += [f"\n  PREDICTION", sep2]
    if pred_result and pred_result.get("values"):
        mode = pred_result["mode"]
        for lbl, val in zip(pred_result["labels"], pred_result["values"]):
            lines.append(f"  {lbl:<14} → ₹{val:,.2f}")
    else:
        lines.append("  Not enough data for prediction.")

    lines += [f"\n  OVERSPENDING ALERTS  ({len(alerts)})", sep2]
    for a in alerts:
        lines.append(f"  ⚠  {a['message']}")
    if not alerts:
        lines.append("  ✅ No overspending detected.")

    lines += [f"\n  ANOMALIES  ({len(anomalies) if not anomalies.empty else 0})", sep2]
    if not anomalies.empty:
        for _, row in anomalies.iterrows():
            lines.append(
                f"  {str(row['date'].date()):<12}  {str(row['description']):<22}  ₹{row['amount']:,.2f}"
            )
    else:
        lines.append("  ✅ No anomalies found.")

    lines += [f"\n  BUDGET COMPARISON", sep2]
    for b in budget_report:
        lines.append(
            f"  {b['category']:<18}  Planned ₹{b['planned']:>7,}  "
            f"Actual ₹{b['actual']:>9,.2f}  {b['status']}"
        )

    lines += [f"\n  SMART RECOMMENDATIONS", sep2]
    for r in recommendations:
        text = r["text"] if isinstance(r, dict) else r
        lines.append(f"  {text}")

    lines.append(f"\n{sep}\n")
    return "\n".join(lines)