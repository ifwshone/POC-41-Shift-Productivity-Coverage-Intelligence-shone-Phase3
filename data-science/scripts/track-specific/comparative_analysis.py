import pandas as pd

def run_comparative_track(df):
    """
    Track A: Comparative Analysis
    Filters for Frontend data only to prevent mixing shift scopes.
    Calculates 5-day average output and overtime for each facility/team.
    Compares against a simple baseline (overall frontend average).
    """
    fe_data = df[(df['source_name'].str.startswith('Frontend')) & (df['record_type'] == 'measurement')].copy()
    
    # Baseline
    baseline = fe_data.groupby('metric_name')['metric_value'].mean().to_dict()
    
    # Group calculations
    grouped = fe_data.groupby(['entity_id', 'subcategory', 'category', 'metric_name']).agg(
        record_count=('metric_value', 'count'),
        avg_value=('metric_value', 'mean')
    ).reset_index()
    
    # Use pivot_table to avoid Pandas multi-index errors
    pivot = grouped.pivot_table(index=['entity_id', 'subcategory', 'category', 'record_count'], columns='metric_name', values='avg_value').reset_index()
    
    pivot['output_gap_vs_baseline'] = pivot['output_per_hour'] - baseline.get('output_per_hour', 0)
    pivot['overtime_gap_vs_baseline'] = pivot['overtime_hours'] - baseline.get('overtime_hours', 0)
    
    # Rank by output gap (worst/lowest output ranks 1 for priority review)
    pivot['priority_rank'] = pivot['output_gap_vs_baseline'].rank(method='dense', ascending=True).astype(int)
    
    return pivot.sort_values('priority_rank').to_dict(orient='records'), baseline