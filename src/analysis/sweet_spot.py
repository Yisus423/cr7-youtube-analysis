import pandas as pd


def analyze_duration_segments(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analiza el rendimiento por segmentos de duración para videos largos.
    """
    # 1. Filtramos para tener solo los videos largos
    long_df = df[df["video_type"] == "long"].copy()

    # 2. Creamos los bins y labels (rangos para pd.cut)
    bins = [0, 180, 600, 1800, 3600, float("inf")]
    labels = ["0-3m", "3-10m", "10-30m", "30-60m", "60m+"]

    # 3. realizamos el pd.cut para segmentar los videos
    long_df["duration_segment"] = pd.cut(
        long_df["duration_seconds"], bins=bins, labels=labels
    )

    # 4. Agregamos los resultados aplicando su respectiva funcion
    summary = (
        long_df.groupby("duration_segment", observed=True)
        .agg(
            mean_views=("viewCount", "mean"),
            median_views=("viewCount", "median"),
            video_count=("duration_segment", "count"),
        )
        .reset_index()
    )

    return summary  # (resultado del análisis)
