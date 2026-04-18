# FinTrackIQ

<div align="center">

# 💎 FinTrackIQ
### AI-Powered Expense Tracking and Budget Management System



**FinTrackIQ** is a fully interactive, AI-driven personal finance assistant that tracks your expenses, auto-categorises them using machine learning, detects anomalies, predicts future spending, and delivers smart budget insights — all through a clean, premium UI with zero CSV uploads required.

[Features](#-features) · [Quick Start](#-quick-start) · [Project Structure](#-project-structure) · [How It Works](#-how-it-works) · [Screenshots](#-ui-overview) · [Tech Stack](#-tech-stack)

---

</div>

## ✨ Features

### 🧠 AI & Machine Learning
| Module | What it does |
|---|---|
| **Hybrid Classifier** | Rule-based keyword matching + TF-IDF / Naive Bayes ML — auto-detects category as you type |
| **Adaptive Prediction** | < 90 days of data → rolling 7-day forecast · ≥ 90 days → Linear Regression monthly prediction |
| **Anomaly Detection** | Isolation Forest flags statistically unusual transactions in real time |
| **Smart Insights Engine** | Period-over-period % change, dominant category detection, weekend vs weekday pattern analysis |

### 📊 Adaptive Analysis Modes
- **Day-wise Mode** *(< 90 days data)* — Daily trend chart, anomaly overlay, 7-day prediction, spike detection
- **Month-wise Mode** *(≥ 90 days data)* — Monthly aggregation, bar chart, period comparison, next-month forecast
- Switches **automatically** based on your data range — no manual config needed

### 💰 Budget Management
- Set per-category budgets (Food, Travel, Shopping, Utilities, Health, Entertainment, Other)
- Live progress bars with colour-coded status: 🟢 Under · 🟡 Near Limit · 🔴 Over
- Overspend alerts with percentage excess
- Daily spending spike detection

### 🗄️ Persistent Storage
- All expenses saved to `data/user_expenses.csv`
- Auto-loaded every time the app starts — **your data never disappears on refresh**
- UTF-8 safe, handles missing values gracefully

### 🖥️ Premium UI
- Clean light theme — high contrast, fully readable
- Responsive tab-based layout: Add → Dashboard → Suggestions → Report
- KPI cards, section headers, badge indicators, insight cards
- No deprecated Streamlit APIs

### 📋 Data Management
- Add expenses with date picker, amount input, and description
- Live category auto-detection preview while typing
- Delete individual rows by index
- Clear all data with one click
- View full table with AI-labelled categories after analysis

### 📝 Report Generation
- Full-text report covering summary, category breakdown, predictions, alerts, anomalies, budget comparison, and smart suggestions
- Downloadable as `.txt` for any period

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- pip

### Installation

```bash
# 1. Clone or download the project
git clone https://github.com/yourusername/FinTrackIQ.git
cd FinTrackIQ

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch the app
streamlit run app.py
```

The app will open at `http://localhost:8501` in your browser.

> **Tip:** Add at least **5 expenses** to unlock the full AI analysis dashboard.

---

## 📁 Project Structure

```
FinTrackIQ/
│
├── data/
│   └── user_expenses.csv          ← auto-created · persists all your entries
│
├── models/                         ← auto-created when analysis runs
│   ├── classifier.pkl              trained Naive Bayes pipeline
│   ├── predictor.pkl               trained regression / rolling model
│   └── anomaly_detector.pkl        trained Isolation Forest
│
├── src/
│   ├── __init__.py
│   ├── preprocessor.py             date parsing & feature extraction
│   ├── classifier.py               hybrid rule-based + TF-IDF/Naive Bayes
│   ├── predictor.py                adaptive day/month spending forecast
│   ├── anomaly_detector.py         Isolation Forest anomaly flagging
│   ├── visualizer.py               all matplotlib charts → PNG bytes
│   ├── alert_engine.py             overspend & daily spike alerts
│   ├── budget_planner.py           planned vs actual per category
│   ├── recommender.py              period-comparison AI insights
│   └── report_generator.py         full-text report builder
│
├── app.py                          ← Streamlit UI · main entry point
├── requirements.txt
└── README.md
```

---

## 🔍 How It Works

```
User Input (description)
        │
        ▼
┌─────────────────────────┐
│  Hybrid Classifier       │  Rule keywords → ML fallback (TF-IDF + Naive Bayes)
│  → Category detected     │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  Preprocessor            │  Date parsing · feature extraction (day, weekday, month, week)
└────────────┬────────────┘
             │
             ▼
┌──────────────────────────────────────────────────────┐
│  Adaptive Analysis Engine                             │
│                                                       │
│  date_range < 90 days → DAY-WISE mode                 │
│    • Daily trend chart + anomaly overlay              │
│    • Weekend vs Weekday comparison                    │
│    • 7-day rolling average prediction                 │
│                                                       │
│  date_range ≥ 90 days → MONTH-WISE mode               │
│    • Monthly aggregation chart                        │
│    • Period-over-period % change                      │
│    • Linear Regression next-month forecast            │
└────────────┬─────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────┐     ┌─────────────────────────┐
│  Anomaly Detector        │     │  Budget Planner          │
│  Isolation Forest        │     │  Planned vs Actual       │
│  → flags outliers        │     │  → progress bars         │
└────────────┬────────────┘     └────────────┬────────────┘
             │                               │
             └──────────────┬────────────────┘
                            ▼
              ┌─────────────────────────┐
              │  Recommendations Engine  │
              │  → % change insights     │
              │  → spending spike alerts │
              │  → category warnings     │
              └────────────┬────────────┘
                           ▼
              ┌─────────────────────────┐
              │  Report Generator        │
              │  → downloadable .txt     │
              └─────────────────────────┘
```

---

## 🖥️ UI Overview

| Tab | Purpose |
|---|---|
| ➕ **Add Expense** | Form with date · amount · description · live category preview · delete rows |
| 📊 **Dashboard** | KPI cards · trend chart · category breakdown · anomalies · budget progress · alerts |
| 💡 **Smart Suggestions** | Color-coded AI insights — error / warning / info based on your spending patterns |
| 📝 **Report** | Full period report with download button |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **UI Framework** | [Streamlit](https://streamlit.io) |
| **Data Processing** | [Pandas](https://pandas.pydata.org) · [NumPy](https://numpy.org) |
| **Machine Learning** | [scikit-learn](https://scikit-learn.org) — TF-IDF, Naive Bayes, Linear Regression, Isolation Forest |
| **Visualisation** | [Matplotlib](https://matplotlib.org) · [Seaborn](https://seaborn.pydata.org) |
| **Model Persistence** | [joblib](https://joblib.readthedocs.io) |
| **Language** | Python 3.10+ |

---

## 📦 Dependencies

```
pandas>=2.1.0
numpy>=1.24.0
scikit-learn>=1.3.0
matplotlib>=3.7.2
seaborn>=0.12.2
streamlit>=1.27.0
joblib>=1.3.2
```

Install all with:
```bash
pip install -r requirements.txt
```

---

## 🗺️ Roadmap

- [ ] Export data as Excel / PDF report
- [ ] Multiple user profiles
- [ ] Bank statement import (PDF parsing)
- [ ] Email / WhatsApp expense input
- [ ] Mobile-optimised layout
- [ ] Recurring expense detection
- [ ] Goal-based savings tracker

---



<div align="center">

Built with ❤️ using Python & Streamlit

**FinTrackIQ** — *Know where your money goes.*

</div>
