import pandas as pd
import pytest
from src.analysis.shorts_vs_longs import analyze_engagement_by_type
from src.analysis.hype_decay import calculate_correlations


def test_analyze_engagement_by_type():
    # 1. Arrange: Un DataFrame preprocesado de prueba
    mock_data = pd.DataFrame(
        {
            "video_type": ["short", "short", "long"],
            "engagement_rate": [0.10, 0.20, 0.05],
            "viewCount": [1000, 2000, 5000],
        }
    )

    # 2. Act: Ejecutamos el análisis
    summary = analyze_engagement_by_type(mock_data)

    # 3. Assert: Verificamos la agrupación
    # Debería haber exactamente 2 grupos (short y long)
    assert len(summary) == 2

    # Verificamos los promedios calculados
    shorts = summary[summary["video_type"] == "short"].iloc[0]
    longs = summary[summary["video_type"] == "long"].iloc[0]

    assert shorts["mean_engagement"] == pytest.approx(0.15)  # (0.10 + 0.20) / 2
    assert longs["mean_engagement"] == pytest.approx(0.05)
    assert shorts["video_count"] == pytest.approx(2)


def test_calculate_correlations_perfect_negative():
    # 1. Arrange: Datos con correlación negativa perfecta
    mock_data = pd.DataFrame(
        {
            "days_since_published": [0, 1, 2],
            "viewCount": [100, 50, 0],
            "engagement_rate": [0.3, 0.2, 0.1],
        }
    )

    # 2. Act
    result = calculate_correlations(mock_data)

    # 3. Assert
    # Filtramos para obtener el valor de correlación para viewCount
    corr_views = result[result["metric"] == "viewCount"]["pearson_correlation"].iloc[0]
    corr_eng = result[result["metric"] == "engagement_rate"][
        "pearson_correlation"
    ].iloc[0]

    # Pearson de [100, 50, 0] vs [0, 1, 2] es -1.0
    assert corr_views == pytest.approx(-1.0)
    assert corr_eng == pytest.approx(-1.0)
