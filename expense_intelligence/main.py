from src.data_generator    import generate_sample_data
from src.preprocessor      import load_and_preprocess
from src.classifier        import train_classifier, predict_category
from src.predictor         import train_predictor, predict_next_month
from src.anomaly_detector  import train_anomaly_detector, detect_anomalies
from src.visualizer        import plot_category_bar, plot_pie_chart, plot_monthly_trend, plot_anomalies
from src.alert_engine      import check_overspending
from src.budget_planner    import compare_budget
from src.recommender       import generate_recommendations
from src.report_generator  import generate_report

def run():
    print(" Starting Personal Expense Intelligence System\n")

    # 1. Generate or load data
    generate_sample_data()

    # 2. Preprocess
    df = load_and_preprocess()

    # 3. Train models
    classifier = train_classifier(df)
    _,  monthly = train_predictor(df)
    train_anomaly_detector(df)

    # 4. Predictions & detection
    prediction = predict_next_month()
    anomalies  = detect_anomalies(df)

    # 5. Visualizations
    plot_category_bar(df)
    plot_pie_chart(df)
    plot_monthly_trend(df)
    plot_anomalies(df, anomalies)

    # 6. Alerts
    alerts = check_overspending(df)

    # 7. Budget
    budget = {"Food":5000,"Travel":6000,"Shopping":8000,"Utilities":3000,"Health":4000,"Entertainment":3000}
    budget_report, _, _ = compare_budget(df, budget)

    # 8. Recommendations
    recommendations = generate_recommendations(df, alerts, anomalies)

    # 9. Report
    generate_report(df, alerts, recommendations, budget_report, prediction, anomalies)

    print("\n✅ All done! Check outputs/ for charts and reports.")

if __name__ == "__main__":
    run()