import pandas as pd
from src.analysis.shorts_vs_longs import analyze_engagement_by_type
from src.preprocessing import calculate_engagement_rate

df = pd.read_csv("data/cristiano_youtube_stats.csv")
df.info()

analyze_engagement_by_type(calculate_engagement_rate(df)).info()
