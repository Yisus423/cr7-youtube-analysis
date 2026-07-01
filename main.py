import pandas as pd
from src.analysis.shorts_vs_longs import analyze_engagement_by_type
from src.analysis.hype_decay import calculate_correlations
from src.preprocessing import run_preprocessing_pipeline

df = pd.read_csv("data/cristiano_youtube_stats.csv")
df.info()

# Realizemos el preprocesamiento (limpieza y añadido de columnas)
df = run_preprocessing_pipeline(df)
# Hypotesis 1
print(analyze_engagement_by_type(df))

# Hypotesis 2
print(calculate_correlations(df))
