import pandas as pd


def calculate_correlations(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula la correlación de Pearson entre la antigüedad del video y sus métricas de rendimiento.

    Args:
        df: DataFrame que contiene 'days_since_published', 'viewCount' y 'engagement_rate'.

    Returns:
        Un DataFrame con los coeficientes de correlación.
    """
    # Calculamos correlaciones
    corr_views = df["days_since_published"].corr(df["viewCount"], method="pearson")
    corr_engagement = df["days_since_published"].corr(
        df["engagement_rate"], method="pearson"
    )

    # Pearson entre antiguedad y vistas LOGARÍTMICAS
    corr_log_views = df["days_since_published"].corr(
        df["log_viewCount"], method="pearson"
    )

    # Creamos un resumen limpio
    correlation_results = pd.DataFrame(
        {
            "metric": ["viewCount", "engagement_rate", "log_viewCount"],
            "pearson_correlation": [corr_views, corr_engagement, corr_log_views],
        }
    )

    return correlation_results
