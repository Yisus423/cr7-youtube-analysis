import pandas as pd
from src.preprocessing import calculate_engagement_rate, compute_days_since_published


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
