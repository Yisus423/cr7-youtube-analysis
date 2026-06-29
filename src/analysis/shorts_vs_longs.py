import pandas as pd


def analyze_engagement_by_type(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrupa el DataFrame por tipo de video y calcula estadísticas clave de engagement.

    Usa 'Named Aggregation' para evitar cabeceras MultiIndex jerárquicas y
    mantener las columnas limpias y fáciles de manipular.

    Args:
        df: DataFrame preprocesado que ya contiene la columna 'engagement_rate'.

    Returns:
        Un nuevo DataFrame con las métricas promedio, mediana y desviación estándar
        para cada tipo de video (short vs long).
    """
    # 1. Aseguramos que las columnas necesarias existan en el DataFrame de entrada
    required_columns = {"video_type", "engagement_rate", "viewCount"}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"El DataFrame debe contener las columnas: {required_columns}")

    # 2. Aplicamos Split-Apply-Combine de forma limpia
    summary = (
        df.groupby("video_type")
        .agg(
            # Formato: nombre_nueva_columna=(columna_origen, funcion_stat)
            mean_engagement=("engagement_rate", "mean"),
            median_engagement=("engagement_rate", "median"),
            std_engagement=("engagement_rate", "std"),
            mean_views=("viewCount", "mean"),
            video_count=("video_type", "count"),
        )
        .reset_index()
    )  # Convierte 'video_type' de índice a columna común

    return summary
