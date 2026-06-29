import pandas as pd
import pytest
from src.analysis.shorts_vs_longs import analyze_engagement_by_type


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
