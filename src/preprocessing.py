import pandas as pd


def calculate_engagement_rate(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula la columna engagement_rate: (likeCount + commentCount) / viewCount

    Maneja cuidadosamente:
    - Valores nulos en likeCount y commentCount (reemplaza con 0)
    - Divisiones por cero en viewCount (usando pd.NA temporalmente)

    Args:
        df: DataFrame crudo con columnas: likeCount, commentCount, viewCount

    Returns:
        Nuevo DataFrame con la columna 'engagement_rate' agregada
    """
    # Hacemos una copia para no mutar el DataFrame original
    df_clean = df.copy()

    # 1. Reemplazamos nulos en likeCount y commentCount con 0
    df_clean["likeCount"] = df_clean["likeCount"].fillna(0)
    df_clean["commentCount"] = df_clean["commentCount"].fillna(0)

    # 2. Evitamos división por cero: convertimos ceros en NA temporalmente
    # Esto hará que Pandas calcule NaN para esos casos en lugar de devolver infinitos
    view_count_safe = df_clean["viewCount"].replace(0, pd.NA)

    # 3. Calculamos el engagement rate
    df_clean["engagement_rate"] = (
        df_clean["likeCount"] + df_clean["commentCount"]
    ) / view_count_safe

    # 4. Reemplazamos cualquier NaN resultante con 0
    df_clean["engagement_rate"] = df_clean["engagement_rate"].fillna(0)

    return df_clean


def compute_days_since_published(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula la antigüedad del video en días desde el video más antiguo del dataset.

    Args:
        df: DataFrame con la columna 'publishTime' en formato ISO 8601.

    Returns:
        DataFrame con la columna 'days_since_published' agregada.
    """
    df_clean = df.copy()

    # 1. Aseguramos que sea datetime
    df_clean["publishTime"] = pd.to_datetime(df_clean["publishTime"], errors="coerce")

    # 2. Calculamos days_since_published
    min_date = df_clean["publishTime"].min()
    df_clean["days_since_published"] = (df_clean["publishTime"] - min_date).dt.days

    return df_clean
