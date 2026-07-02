import pandas as pd
from scripts.preprocessing import (
    calculate_engagement_rate,
    compute_days_since_published,
    add_log_features,
    run_preprocessing_pipeline,
)


def test_calculate_engagement_rate_behavior():
    # 1. Arrange: Datos ficticios con casos normales, división por cero y nulos
    mock_data = pd.DataFrame(
        {
            "likeCount": [10, None, 0],
            "commentCount": [5, 5, 0],
            "viewCount": [100, 50, 0],  # Incluye un video con 0 vistas
        }
    )

    # 2. Act: Ejecutamos el cálculo
    result = calculate_engagement_rate(mock_data)

    # 3. Assert: Verificamos resultados esperados
    # Fila 0: (10 + 5) / 100 = 0.15
    assert result.loc[0, "engagement_rate"] == 0.15

    # Fila 1: (0 + 5) / 50 = 0.10 (Manejo de nulos en likeCount)
    assert result.loc[1, "engagement_rate"] == 0.10

    # Fila 2: (0 + 0) / 0 = 0.0 (Evita división por cero de forma segura)
    assert result.loc[2, "engagement_rate"] == 0.0


def test_compute_days_since_published():
    # 1. Arrange: 3 videos con fechas consecutivas
    mock_data = pd.DataFrame(
        {
            "publishTime": [
                "2024-01-01T12:00:00Z",
                "2024-01-02T12:00:00Z",
                "2024-01-03T12:00:00Z",
            ]
        }
    )

    # 2. Act
    result = compute_days_since_published(mock_data)

    # 3. Assert
    # Esperamos que el primero sea 0, el segundo 1, el tercero 2
    assert result["days_since_published"].tolist() == [0, 1, 2]


def test_add_log_features():
    # Arrange
    mock_data = pd.DataFrame(
        {"viewCount": [0, 9, 99]}
    )  # log1p(0)=0, log1p(9)=1, log1p(99)=2 (base 10)

    # Act
    result = add_log_features(mock_data)

    # Assert: usamos np.log10(x + 1)
    assert result.loc[0, "log_viewCount"] == 0.0
    assert result.loc[1, "log_viewCount"] == 1.0
    assert result.loc[2, "log_viewCount"] == 2.0


def test_run_preprocessing_pipeline():
    # Arrange: Datos que requieren limpieza y transformación
    mock_data = pd.DataFrame(
        {
            "likeCount": [10],
            "commentCount": [5],
            "viewCount": [100],
            "publishTime": ["2024-01-01"],
        }
    )

    # Act: Corremos todo el orquestador
    result = run_preprocessing_pipeline(mock_data)

    # Assert: Verificamos que todas las columnas nuevas existan
    expected_cols = {"engagement_rate", "days_since_published", "log_viewCount"}
    assert expected_cols.issubset(result.columns)
