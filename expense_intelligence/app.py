"""
Personal Expense Intelligence System — app.py
Run: streamlit run app.py
"""

import os
import streamlit as st
import pandas as pd
from datetime import date, datetime

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Expense Intelligence",
    page_icon=" ",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────
DATA_PATH = "data/user_expenses.csv"
CATEGORIES = ["Food", "Travel", "Shopping", "Utilities", "Health", "Entertainment", "Other"]
MIN_FOR_ANALYSIS = 5


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

:root {
  --bg:      #0b0e17;
  --surface: #12161f;
  --card:    #181c28;
  --border:  #252a38;
  --accent:  #22d3ee;
  --amber:   #f59e0b;
  --green:   #22c55e;
  --red:     #ef4444;
  --text:    #e2e8f0;
  --muted:   #64748b;
  --font:    'Outfit', sans-serif;
  --mono:    'JetBrains Mono', monospace;
}

html, body, [class*="css"] { font-family: var(--font); }

/* ── app background ── */
.stApp { background: var(--bg) !important; color: var(--text); }
section[data-testid="stSidebar"] { background: var(--surface) !important; }

/* ── typography ── */
h1 { font-size: 1.9rem !important; font-weight: 700 !important; color: var(--text) !important; }
h2 { font-size: 1.25rem !important; font-weight: 600 !important; color: var(--text) !important; }
h3 { font-size: 1.05rem !important; color: var(--text) !important; }
p, li, label { color: var(--text) !important; }

/* ── cards ── */
.kpi-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 1.1rem 1.3rem;
  text-align: center;
}
.kpi-val {
  font-family: var(--mono);
  font-size: 1.55rem;
  font-weight: 600;
  color: var(--accent);
  line-height: 1.2;
}
.kpi-label {
  font-size: 0.72rem;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-top: 4px;
}
.kpi-sub {
  font-size: 0.78rem;
  color: var(--muted);
  margin-top: 2px;
}
.section-header {
  font-size: 0.72rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--accent);
  margin: 1.4rem 0 0.6rem 0;
  border-bottom: 1px solid var(--border);
  padding-bottom: 0.4rem;
}
.insight-card {
  background: var(--card);
  border-left: 3px solid var(--accent);
  border-radius: 0 10px 10px 0;
  padding: 0.75rem 1rem;
  margin-bottom: 0.6rem;
  font-size: 0.9rem;
}
.badge {
  display: inline-block;
  padding: 2px 10px;
  border-radius: 20px;
  font-size: 0.72rem;
  font-weight: 600;
}
.badge-day  { background: #22d3ee22; color: #22d3ee; }
.badge-month{ background: #f59e0b22; color: #f59e0b; }

/* ── tabs ── */
.stTabs [data-baseweb="tab-list"] {
  background: var(--surface) !important;
  border-radius: 12px;
  padding: 5px;
  gap: 4px;
  border: 1px solid var(--border);
}
.stTabs [data-baseweb="tab"] {
  border-radius: 9px !important;
  color: var(--muted) !important;
  font-weight: 500 !important;
  font-size: 0.88rem !important;
  padding: 0.45rem 1.1rem !important;
}
.stTabs [aria-selected="true"] {
  background: linear-gradient(135deg, #22d3ee22, #22d3ee11) !important;
  color: var(--accent) !important;
  font-weight: 600 !important;
}

/* ── buttons ── */
div.stButton > button {
  background: linear-gradient(135deg, #0891b2, #22d3ee) !important;
  color: #0b0e17 !important;
  border: none !important;
  border-radius: 9px !important;
  padding: 0.48rem 1.3rem !important;
  font-family: var(--font) !important;
  font-weight: 600 !important;
  font-size: 0.88rem !important;
  letter-spacing: 0.02em !important;
}
div.stButton > button:hover { opacity: 0.88 !important; }
div.stButton > button[kind="secondary"] {
  background: var(--card) !important;
  border: 1px solid var(--border) !important;
  color: var(--muted) !important;
}

/* ── form inputs ── */
.stTextInput input,
.stNumberInput input,
.stDateInput input,
.stSelectbox div[data-baseweb="select"] > div {
  background: var(--card) !important;
  border: 1px solid var(--border) !important;
  border-radius: 9px !important;
  color: var(--text) !important;
  font-family: var(--font) !important;
}
.stTextInput input:focus,
.stNumberInput input:focus { border-color: var(--accent) !important; }

/* ── dataframe ── */
.stDataFrame { border-radius: 12px; overflow: hidden; }

/* ── progress bars ── */
.stProgress > div > div { background: var(--accent) !important; }

/* ── alerts ── */
.stAlert { border-radius: 10px !important; }

/* ── metric delta ── */
[data-testid="stMetricDelta"] { font-size: 0.78rem !important; }

/* ── hide streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


def load_from_disk() -> pd.DataFrame:
    if os.path.exists(DATA_PATH):
        try:
            df = pd.read_csv(DATA_PATH, encoding="utf-8")
            for col in ["date", "amount", "description"]:
                if col not in df.columns:
                    df[col] = "" if col != "amount" else 0.0
            return df
        except Exception:
            pass
    return pd.DataFrame(columns=["date", "amount", "description", "category"])


def save_to_disk(df: pd.DataFrame):
    os.makedirs("data", exist_ok=True)
    df.to_csv(DATA_PATH, index=False, encoding="utf-8")


if "expenses" not in st.session_state:
    st.session_state.expenses = load_from_disk()

if "analysis" not in st.session_state:
    st.session_state.analysis = {}

if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

if "budget" not in st.session_state:
    st.session_state.budget = {c: 5000 for c in CATEGORIES}


# ─────────────────────────────────────────────────────────────────────────────
# CORE ANALYSIS RUNNER
# ─────────────────────────────────────────────────────────────────────────────
def run_analysis(df_raw: pd.DataFrame, budget: dict) -> dict:
    from src.preprocessor     import load_and_preprocess
    from src.classifier       import train_classifier, label_dataframe
    from src.predictor        import train_predictor, predict
    from src.anomaly_detector import train_anomaly_detector, detect_anomalies
    from src.visualizer       import (plot_daily_trend, plot_monthly_trend,
                                      plot_category_bar, plot_pie_chart,
                                      plot_weekend_vs_weekday,
                                      plot_prediction, plot_budget_progress)
    from src.alert_engine     import check_overspending, check_daily_spike
    from src.budget_planner   import compare_budget
    from src.recommender      import generate_recommendations
    from src.report_generator import generate_report

    df = load_and_preprocess(df_raw)

    # Auto-categorise
    clf = train_classifier(df)
    df  = label_dataframe(df, clf)

    # Determine mode
    date_range = (df["date"].max() - df["date"].min()).days
    mode = "month" if date_range >= 90 else "day"

    # Train models
    pred_meta  = train_predictor(df)
    train_anomaly_detector(df)

    # Predict
    n = 1 if mode == "month" else 7
    pred_result = predict(n)

    # Anomalies
    anomalies = detect_anomalies(df)

    # Charts
    if mode == "day":
        trend_chart = plot_daily_trend(df, anomalies)
    else:
        trend_chart = plot_monthly_trend(df)

    cat_bar   = plot_category_bar(df)
    pie       = plot_pie_chart(df)
    wknd      = plot_weekend_vs_weekday(df)
    pred_chart= plot_prediction(pred_result) if pred_result["values"] else None

    # Alerts & budget
    alerts       = check_overspending(df, budget)
    spikes       = check_daily_spike(df)
    budget_report, total_planned, total_actual = compare_budget(df, budget)
    budget_chart  = plot_budget_progress(budget_report)

    # Suggestions
    recs = generate_recommendations(df, alerts, anomalies, mode)

    # Report
    period_label = (
        f"{df['date'].min().strftime('%d %b %Y')} – {df['date'].max().strftime('%d %b %Y')}"
    )
    report_text = generate_report(
        df, alerts, recs, budget_report, pred_result, anomalies, period_label
    )

    return {
        "df":            df,
        "mode":          mode,
        "date_range":    date_range,
        "pred_result":   pred_result,
        "anomalies":     anomalies,
        "charts": {
            "trend":  trend_chart,
            "cat_bar": cat_bar,
            "pie":    pie,
            "wknd":   wknd,
            "pred":   pred_chart,
            "budget": budget_chart,
        },
        "alerts":        alerts,
        "spikes":        spikes,
        "budget_report": budget_report,
        "total_planned": total_planned,
        "total_actual":  total_actual,
        "recs":          recs,
        "report_text":   report_text,
        "period_label":  period_label,
    }


# ─────────────────────────────────────────────────────────────────────────────
# KPI CARD HELPER
# ─────────────────────────────────────────────────────────────────────────────
def kpi(val: str, label: str, sub: str = ""):
    sub_html = f'<div class="kpi-sub">{sub}</div>' if sub else ""
    st.markdown(
        f'<div class="kpi-card">'
        f'<div class="kpi-val">{val}</div>'
        f'<div class="kpi-label">{label}</div>'
        f'{sub_html}</div>',
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────────────────
col_h1, col_h2 = st.columns([6, 1])
with col_h1:
    st.markdown(
        "<h1>💎 FinTrackIQ</h1>"
        "<p style='color:#64748b; margin-top:-10px; font-size:0.9rem;'>"
        "AI-Powered Expense Tracking and Budget Management System</p>",
        unsafe_allow_html=True,
    )
with col_h2:
    n_exp = len(st.session_state.expenses)
    st.markdown(
        f'<div class="kpi-card" style="margin-top:8px;">'
        f'<div class="kpi-val">{n_exp}</div>'
        f'<div class="kpi-label">Saved Entries</div></div>',
        unsafe_allow_html=True,
    )

st.markdown("---")

# ─────────────────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────────────────
tab_add, tab_dash, tab_sug, tab_report = st.tabs([
    "➕  Add Expense",
    "📊  Dashboard",
    "💡  Smart Suggestions",
    "📝  Report",
])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 ─ ADD EXPENSE
# ══════════════════════════════════════════════════════════════════════════════
with tab_add:
    st.markdown('<div class="section-header">New Entry</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns([1.1, 1, 1.8, 1.2])
    with c1:
        exp_date = st.date_input("📅 Date", value=date.today())
    with c2:
        exp_amount = st.number_input("₹ Amount", min_value=0.01, value=500.0, step=50.0)
    with c3:
        exp_desc = st.text_input("📝 Description",
                                 placeholder="e.g. lunch, uber, netflix…")
    with c4:
        # Live category preview
        from src.classifier import predict_category
        detected = predict_category(exp_desc) if exp_desc.strip() else "—"
        st.markdown(
            f'<div class="kpi-card" style="margin-top:28px;">'
            f'<div class="kpi-val" style="font-size:1.05rem;">{detected}</div>'
            f'<div class="kpi-label">Auto-detected</div></div>',
            unsafe_allow_html=True,
        )

    cb1, cb2, cb3 = st.columns([1, 1, 6])
    with cb1:
        add_clicked = st.button("✅ Add Expense")
    with cb2:
        clear_all = st.button("🗑️ Clear All", type="secondary")

    if add_clicked:
        if not exp_desc.strip():
            st.warning("Please enter a description.")
        else:
            cat = predict_category(exp_desc.strip())
            new_row = pd.DataFrame([{
                "date":        str(exp_date),
                "amount":      exp_amount,
                "description": exp_desc.strip(),
                "category":    cat,
            }])
            st.session_state.expenses = pd.concat(
                [st.session_state.expenses, new_row], ignore_index=True
            )
            save_to_disk(st.session_state.expenses)
            st.session_state.analysis_done = False
            st.success(f"✅ **{exp_desc}** added as **{cat}** — ₹{exp_amount:,.2f}")

    if clear_all:
        st.session_state.expenses = pd.DataFrame(
            columns=["date", "amount", "description", "category"]
        )
        save_to_disk(st.session_state.expenses)
        st.session_state.analysis_done = False
        st.session_state.analysis = {}
        st.info("All data cleared.")

    # ── View & manage existing data ────────────────────────────────────────
    df_view = st.session_state.expenses
    if not df_view.empty:
        st.markdown('<div class="section-header">Your Expenses</div>', unsafe_allow_html=True)

        # Quick stats
        total_v = df_view["amount"].astype(float).sum()
        m1, m2, m3, m4 = st.columns(4)
        with m1: kpi(f"{len(df_view)}", "Total Entries")
        with m2: kpi(f"₹{total_v:,.0f}", "Total Spent")
        with m3: kpi(f"₹{total_v/max(len(df_view),1):,.0f}", "Avg per Entry")
        if "category" in df_view.columns:
            top = df_view.groupby("category")["amount"].sum().idxmax()
            with m4: kpi(top, "Top Category")

        st.markdown("<br>", unsafe_allow_html=True)

        # Editable table with delete
        display_df = df_view.copy()
        display_df.index = range(1, len(display_df) + 1)
        display_df["amount"] = display_df["amount"].apply(lambda x: f"₹{float(x):,.2f}")

        st.dataframe(display_df[["date", "amount", "description", "category"]],
                     use_container_width=True, height=350)

        # Delete by index
        st.markdown('<div class="section-header">Delete Entry</div>', unsafe_allow_html=True)
        del_col1, del_col2 = st.columns([1, 4])
        with del_col1:
            del_idx = st.number_input("Row # to delete", min_value=1,
                                      max_value=len(df_view), value=1, step=1)
        with del_col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🗑️ Delete Row", type="secondary"):
                st.session_state.expenses = (
                    df_view.drop(index=df_view.index[del_idx - 1])
                    .reset_index(drop=True)
                )
                save_to_disk(st.session_state.expenses)
                st.session_state.analysis_done = False
                st.success(f"Row {del_idx} deleted.")
                st.rerun()
    else:
        st.markdown(
            "<p style='color:#4b5563; text-align:center; padding:2rem 0;'>"
            "No expenses yet — add your first one above </p>",
            unsafe_allow_html=True,
        )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 ─ DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
with tab_dash:
    n_exp = len(st.session_state.expenses)

    if n_exp < MIN_FOR_ANALYSIS:
        st.info(f"Add at least **{MIN_FOR_ANALYSIS}** expenses to unlock the dashboard. "
                f"You have **{n_exp}** so far.")
    else:
        # ── Budget settings (sidebar-like expander) ────────────────────────
        with st.expander("⚙️  Budget Settings (click to customise)", expanded=False):
            budget_cols = st.columns(len(CATEGORIES))
            for i, cat in enumerate(CATEGORIES):
                with budget_cols[i]:
                    st.session_state.budget[cat] = st.number_input(
                        cat, min_value=0, value=st.session_state.budget[cat],
                        step=500, key=f"budget_{cat}"
                    )

        run_col, _ = st.columns([1, 5])
        with run_col:
            run_btn = st.button("🚀 Run Analysis")

        if run_btn:
            with st.spinner("Running AI analysis…"):
                try:
                    result = run_analysis(
                        st.session_state.expenses.copy(),
                        st.session_state.budget,
                    )
                    st.session_state.analysis = result
                    st.session_state.analysis_done = True
                    st.success("Analysis complete!")
                except Exception as e:
                    st.error(f"Analysis error: {e}")

        if st.session_state.analysis_done:
            r  = st.session_state.analysis
            df = r["df"]
            mode = r["mode"]

            # Mode badge
            badge_cls = "badge-month" if mode == "month" else "badge-day"
            badge_lbl = ("📅 Month-wise Mode (≥90 days data)"
                         if mode == "month"
                         else "📆 Day-wise Mode (<90 days data)")
            st.markdown(
                f'<span class="badge {badge_cls}">{badge_lbl}</span>',
                unsafe_allow_html=True,
            )
            st.markdown("<br>", unsafe_allow_html=True)

            # ── KPIs ──────────────────────────────────────────────────────
            st.markdown('<div class="section-header">Key Metrics</div>',
                        unsafe_allow_html=True)
            total = df["amount"].sum()
            avg_d = df.groupby("date")["amount"].sum().mean()
            top_c = df.groupby("category")["amount"].sum().idxmax()
            top_d = df.groupby("date")["amount"].sum().idxmax()
            pred  = r["pred_result"]
            pred_val = f"₹{pred['values'][0]:,.0f}" if pred.get("values") else "N/A"
            pred_lbl = pred["labels"][0] if pred.get("labels") else ""

            k1, k2, k3, k4, k5, k6 = st.columns(6)
            with k1: kpi(f"₹{total:,.0f}", "Total Spent")
            with k2: kpi(str(len(df)), "Transactions")
            with k3: kpi(f"₹{avg_d:,.0f}", "Avg / Day")
            with k4: kpi(pred_val, "Prediction", pred_lbl)
            with k5: kpi(top_c, "Top Category")
            with k6: kpi(top_d.strftime("%d %b"), "Highest Day")

            st.markdown("<br>", unsafe_allow_html=True)

            # ── Trend chart ───────────────────────────────────────────────
            st.markdown('<div class="section-header">Spending Trend</div>',
                        unsafe_allow_html=True)
            st.image(r["charts"]["trend"], use_container_width=True)

            # ── Category + Pie ─────────────────────────────────────────────
            st.markdown('<div class="section-header">Category Breakdown</div>',
                        unsafe_allow_html=True)
            ch1, ch2 = st.columns([1.5, 1])
            with ch1:
                st.image(r["charts"]["cat_bar"], use_container_width=True)
            with ch2:
                st.image(r["charts"]["pie"], use_container_width=True)

            # ── Weekend vs Weekday + Prediction ───────────────────────────
            st.markdown('<div class="section-header">Patterns & Forecast</div>',
                        unsafe_allow_html=True)
            pw1, pw2 = st.columns(2)
            with pw1:
                st.image(r["charts"]["wknd"], use_container_width=True)
            with pw2:
                if r["charts"]["pred"]:
                    st.image(r["charts"]["pred"], use_container_width=True)

            # ── Anomalies ─────────────────────────────────────────────────
            anomalies = r["anomalies"]
            if not anomalies.empty:
                st.markdown('<div class="section-header">⚠️ Anomalies Detected</div>',
                            unsafe_allow_html=True)
                st.error(f"{len(anomalies)} unusual transaction(s) flagged by Isolation Forest.")
                st.dataframe(
                    anomalies[["date", "description", "category", "amount", "anomaly_score"]],
                    use_container_width=True,
                )

            # ── Daily spikes ──────────────────────────────────────────────
            if r["spikes"]:
                st.markdown('<div class="section-header">📈 Daily Spending Spikes</div>',
                            unsafe_allow_html=True)
                for sp in r["spikes"]:
                    st.warning(sp["message"])

            # ── Budget ────────────────────────────────────────────────────
            st.markdown('<div class="section-header">Budget vs Actual</div>',
                        unsafe_allow_html=True)
            st.image(r["charts"]["budget"], use_container_width=True)

            # Progress bars
            for b in r["budget_report"]:
                pct = min(b["pct_used"] / 100, 1.5)
                color_note = "🔴" if b["pct_used"] > 100 else ("🟡" if b["pct_used"] > 80 else "🟢")
                st.markdown(
                    f"**{color_note} {b['category']}** — "
                    f"₹{b['actual']:,.0f} of ₹{b['planned']:,} "
                    f"({b['pct_used']:.0f}%) {b['status']}"
                )
                st.progress(min(b["pct_used"] / 100, 1.0))

            # ── Overspending alerts ────────────────────────────────────────
            if r["alerts"]:
                st.markdown('<div class="section-header">🚨 Overspending Alerts</div>',
                            unsafe_allow_html=True)
                for a in r["alerts"]:
                    if a["level"] == "critical":
                        st.error(f"🔴 {a['message']}")
                    else:
                        st.warning(f"🟡 {a['message']}")

            st.markdown(
                f"<p style='color:var(--muted); font-size:0.78rem; margin-top:1rem;'>"
                f"Analysis period: {r['period_label']} · "
                f"Mode: {'Monthly' if mode=='month' else 'Daily'} "
                f"({r['date_range']} days of data)</p>",
                unsafe_allow_html=True,
            )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 ─ SMART SUGGESTIONS
# ══════════════════════════════════════════════════════════════════════════════
with tab_sug:
    st.markdown('<div class="section-header">AI-Powered Insights</div>',
                unsafe_allow_html=True)

    if not st.session_state.analysis_done:
        st.info("Run **Dashboard → Run Analysis** first to generate personalised suggestions.")
    else:
        recs  = st.session_state.analysis.get("recs", [])
        mode  = st.session_state.analysis.get("mode", "day")
        r     = st.session_state.analysis

        # Period comparison summary card
        df = r["df"]
        total = df["amount"].sum()
        top_c = df.groupby("category")["amount"].sum().idxmax()
        top_c_pct = (df.groupby("category")["amount"].sum()[top_c] / total * 100)
        wknd_amt = df[df["is_weekend"]]["amount"].sum()
        wknd_pct = wknd_amt / total * 100 if total else 0

        st.markdown(
            f'<div class="insight-card">'
            f'<b>📊 Period Summary</b><br>'
            f'₹{total:,.0f} across {len(df)} transactions · '
            f'Top: <b>{top_c}</b> ({top_c_pct:.1f}%) · '
            f'Weekend: {wknd_pct:.1f}% of spend'
            f'</div>',
            unsafe_allow_html=True,
        )

        if not recs:
            st.success("🎉 Your spending pattern looks balanced. Keep it up!")
        else:
            for rec in recs:
                level = rec.get("level", "info") if isinstance(rec, dict) else "info"
                text  = rec.get("text", rec) if isinstance(rec, dict) else rec
                if level == "error":
                    st.error(text)
                elif level == "warning":
                    st.warning(text)
                else:
                    st.info(text)

        st.markdown("---")
        st.caption("💡 Suggestions update each time you run a fresh analysis.")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 ─ REPORT
# ══════════════════════════════════════════════════════════════════════════════
with tab_report:
    st.markdown('<div class="section-header">Download Your Report</div>',
                unsafe_allow_html=True)

    if not st.session_state.analysis_done:
        st.info("Run **Dashboard → Run Analysis** first to generate your report.")
    else:
        report_text = st.session_state.analysis.get("report_text", "")
        period      = st.session_state.analysis.get("period_label", "period")

        st.text(report_text)

        st.download_button(
            label="⬇️  Download Report (.txt)",
            data=report_text.encode("utf-8"),
            file_name=f"expense_report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain",
        )