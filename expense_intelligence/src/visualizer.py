import io
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import pandas as pd
import numpy as np

# Palette aligned with the dark UI
BG      = "#0f1117"
CARD    = "#1a1d27"
ACCENT  = "#22d3ee"   # cyan
ACCENT2 = "#f59e0b"   # amber
RED     = "#ef4444"
GREEN   = "#22c55e"
MUTED   = "#4b5563"
TEXT    = "#73960a"

sns.set_theme(style="dark")


def _fig_to_bytes(fig) -> bytes:
    buf = io.BytesIO()
    fig.patch.set_facecolor(BG)
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=130, facecolor=BG)
    buf.seek(0)
    plt.close(fig)
    return buf.read()


def _style_ax(ax, title: str = ""):
    ax.set_facecolor(CARD)
    ax.tick_params(colors=TEXT, labelsize=9)
    ax.xaxis.label.set_color(MUTED)
    ax.yaxis.label.set_color(MUTED)
    for spine in ax.spines.values():
        spine.set_edgecolor("#2d3748")
    if title:
        ax.set_title(title, color=TEXT, fontsize=11, fontweight="bold", pad=10)


# ── Daily trend ─────────────────────────────────────────────────────────────
def plot_daily_trend(df: pd.DataFrame, anomalies: pd.DataFrame = None) -> bytes:
    daily = df.groupby("date")["amount"].sum().reset_index()
    fig, ax = plt.subplots(figsize=(11, 3.8))
    ax.fill_between(daily["date"], daily["amount"], alpha=0.18, color=ACCENT)
    ax.plot(daily["date"], daily["amount"], color=ACCENT, linewidth=2, marker="o",
            markersize=4, zorder=3)
    # anomaly overlay
    if anomalies is not None and not anomalies.empty:
        anom_daily = anomalies.groupby("date")["amount"].sum().reset_index()
        ax.scatter(anom_daily["date"], anom_daily["amount"],
                   color=RED, s=70, zorder=5, label="Anomaly")
        ax.legend(facecolor=CARD, labelcolor=TEXT, fontsize=8)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.xticks(rotation=30)
    ax.set_ylabel("₹ Amount", color=MUTED)
    _style_ax(ax, "Daily Spending Trend")
    fig.tight_layout()
    return _fig_to_bytes(fig)


# ── Monthly trend ────────────────────────────────────────────────────────────
def plot_monthly_trend(df: pd.DataFrame) -> bytes:
    monthly = (
        df.groupby(["year", "month", "month_name"])["amount"]
        .sum()
        .reset_index()
        .sort_values(["year", "month"])
    )
    fig, ax = plt.subplots(figsize=(11, 3.8))
    bars = ax.bar(monthly["month_name"], monthly["amount"],
                  color=ACCENT, alpha=0.85, width=0.6)
    # highlight max
    max_idx = monthly["amount"].idxmax()
    bars[max_idx].set_color(ACCENT2)
    ax.set_ylabel("₹ Amount", color=MUTED)
    plt.xticks(rotation=30)
    _style_ax(ax, "Monthly Spending")
    fig.tight_layout()
    return _fig_to_bytes(fig)


# ── Category bar ─────────────────────────────────────────────────────────────
def plot_category_bar(df: pd.DataFrame) -> bytes:
    cat = df.groupby("category")["amount"].sum().sort_values(ascending=True)
    colors = sns.color_palette("cool", len(cat))
    fig, ax = plt.subplots(figsize=(9, max(3.5, len(cat) * 0.55)))
    bars = ax.barh(cat.index, cat.values, color=colors, height=0.6)
    for bar, val in zip(bars, cat.values):
        ax.text(val + cat.values.max() * 0.01, bar.get_y() + bar.get_height() / 2,
                f"₹{val:,.0f}", va="center", color=TEXT, fontsize=8)
    _style_ax(ax, "Spending by Category")
    ax.set_xlabel("₹ Amount", color=MUTED)
    fig.tight_layout()
    return _fig_to_bytes(fig)


# ── Pie chart ────────────────────────────────────────────────────────────────
def plot_pie_chart(df: pd.DataFrame) -> bytes:
    cat = df.groupby("category")["amount"].sum()
    colors = sns.color_palette("cool", len(cat))
    fig, ax = plt.subplots(figsize=(6, 5))
    fig.patch.set_facecolor(BG)
    wedges, texts, autotexts = ax.pie(
        cat.values, labels=cat.index, autopct="%1.1f%%",
        colors=colors, startangle=140,
        wedgeprops={"linewidth": 1.5, "edgecolor": BG},
    )
    for t in texts:
        t.set_color(TEXT)
        t.set_fontsize(9)
    for at in autotexts:
        at.set_color(BG)
        at.set_fontsize(8)
        at.set_fontweight("bold")
    ax.set_title("Expense Distribution", color=TEXT, fontsize=11, fontweight="bold")
    fig.tight_layout()
    return _fig_to_bytes(fig)


# ── Weekend vs Weekday ───────────────────────────────────────────────────────
def plot_weekend_vs_weekday(df: pd.DataFrame) -> bytes:
    grp = df.groupby("is_weekend")["amount"].sum()
    labels = {False: "Weekday", True: "Weekend"}
    vals   = [grp.get(False, 0), grp.get(True, 0)]
    cols   = [ACCENT, ACCENT2]
    fig, ax = plt.subplots(figsize=(5, 3.5))
    ax.bar([labels[False], labels[True]], vals, color=cols, width=0.5)
    for i, v in enumerate(vals):
        ax.text(i, v + max(vals) * 0.02, f"₹{v:,.0f}", ha="center",
                color=TEXT, fontsize=9, fontweight="bold")
    _style_ax(ax, "Weekday vs Weekend")
    ax.set_ylabel("₹ Total", color=MUTED)
    fig.tight_layout()
    return _fig_to_bytes(fig)


# ── Prediction bar ───────────────────────────────────────────────────────────
def plot_prediction(pred_result: dict) -> bytes:
    labels = pred_result["labels"]
    values = pred_result["values"]
    fig, ax = plt.subplots(figsize=(max(6, len(labels) * 1.1), 3.5))
    colors = [GREEN] * len(labels)
    bars = ax.bar(labels, values, color=colors, width=0.55, alpha=0.9)
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max(values) * 0.02,
                f"₹{val:,.0f}", ha="center", color=TEXT, fontsize=8, fontweight="bold")
    _style_ax(ax, "Predicted Spending")
    ax.set_ylabel("₹ Amount", color=MUTED)
    plt.xticks(rotation=20)
    fig.tight_layout()
    return _fig_to_bytes(fig)


# ── Budget progress (horizontal bars) ───────────────────────────────────────
def plot_budget_progress(budget_report: list) -> bytes:
    cats     = [b["category"]  for b in budget_report]
    planned  = [b["planned"]   for b in budget_report]
    actual   = [b["actual"]    for b in budget_report]
    pct      = [min(a / max(p, 1), 1.5) for a, p in zip(actual, planned)]

    fig, ax = plt.subplots(figsize=(9, max(3.5, len(cats) * 0.65)))
    y = range(len(cats))
    ax.barh(y, planned, color=MUTED,   alpha=0.35, height=0.5, label="Budget")
    ax.barh(y, actual,  color=[RED if p > 1 else ACCENT for p in pct],
            alpha=0.85, height=0.5, label="Actual")
    ax.set_yticks(list(y))
    ax.set_yticklabels(cats, color=TEXT, fontsize=9)
    ax.legend(facecolor=CARD, labelcolor=TEXT, fontsize=8)
    _style_ax(ax, "Budget vs Actual")
    ax.set_xlabel("₹ Amount", color=MUTED)
    fig.tight_layout()
    return _fig_to_bytes(fig)