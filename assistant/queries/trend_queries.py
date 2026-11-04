# /assistant/queries/trend_queries.py
def get_period_change(entity_id: str, period: str):
    """
    Track B (Trend) is Conditional and only supports descriptive 5-day views.
    Blocked from forecasting or deep anomaly tracking.
    """
    return {
        "status": "unsupported",
        "answer": "Trend forecasting and period-over-period changes are out of scope. Data is limited to a synthetic 5-day descriptive view.",
        "suggested_follow_ups": ["What are the data limitations?"]
    }