import pandas as pd
from src.analysis.shorts_vs_longs import analyze_engagement_by_type
from src.analysis.hype_decay import calculate_correlations
from src.analysis.sweet_spot import analyze_duration_segments

# Cargamos el dataset preprocesado
df = pd.read_parquet("data/processed_data.parquet")
df.info()

# Hypotesis 1
print(analyze_engagement_by_type(df))

# Hypotesis 2
print(calculate_correlations(df))

# Hypotesis 3
print(analyze_duration_segments(df))
