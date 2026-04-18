def compare_budget(df, budget: dict) -> tuple[list, float, float]:
    cat_totals = df.groupby("category")["amount"].sum().to_dict()
    report = []
    for category, planned in budget.items():
        actual = cat_totals.get(category, 0)
        diff   = planned - actual
        pct    = (actual / max(planned, 1)) * 100
        report.append({
            "category":  category,
            "planned":   planned,
            "actual":    round(actual, 2),
            "diff":      round(diff, 2),
            "pct_used":  round(pct, 1),
            "status":    " Under" if diff >= 0 else " Over",
        })
    total_planned = sum(budget.values())
    total_actual  = round(sum(cat_totals.get(c, 0) for c in budget), 2)
    return report, total_planned, total_actual