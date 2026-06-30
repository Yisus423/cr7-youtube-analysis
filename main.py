import pandas as pd
from src.analysis.shorts_vs_longs import analyze_engagement_by_type
from src.analysis.hype_decay import calculate_correlations
from src.preprocessing import calculate_engagement_rate, compute_days_since_published

df = pd.read_csv("data/cristiano_youtube_stats.csv")
df.info()

# Hypotesis 1
df = calculate_engagement_rate(df)
print(analyze_engagement_by_type(df))

# Hypotesis 2
df = compute_days_since_published(df)
print(calculate_correlations(df))
