import streamlit as st
import pandas as pd
from src.preprocessing import run_preprocessing_pipeline
from src.analysis.shorts_vs_longs import analyze_engagement_by_type
from src.analysis.hype_decay import calculate_correlations
from src.analysis.sweet_spot import analyze_duration_segments


def render_metric_selector(
    label: str, options: dict[str, str], key: str, default_index: int = 0
) -> str:
    """
    Renderiza un componente de selección (selectbox) de Streamlit.

    Este helper encapsula la lógica de renderizado para evitar la repetición
    de código (DRY) al permitir mapear etiquetas legibles por el usuario
    hacia claves técnicas necesarias para el análisis.

    Args:
        label (str): Texto de encabezado que verá el usuario.
        options (dict[str, str]): Diccionario donde la llave es la etiqueta
            mostrada al usuario y el valor es la columna técnica.
        key (str): Identificador único para el widget en Streamlit.
        default_index (int, optional): Índice de la opción seleccionada
            por defecto. Defaults a 0.
    Returns:
        str: El valor técnico seleccionado correspondiente a la etiqueta elegida.
    """
    selected_label = st.selectbox(
        label, options=list(options.keys()), key=key, index=default_index
    )
    return options[selected_label]


def render_hypothesis_1(df: pd.DataFrame):
    # Análisis Hipótesis 1: Shorts vs Longs
    st.header("1. ¿Shorts o Videos Largos?")

    # Obtenemos los datos (asumiendo que ya tienes el df preprocesado)
    summary_h1 = analyze_engagement_by_type(df)
    st.dataframe(summary_h1)

    # Mostramos el subheader
    st.subheader("Análisis por tipo de video: ")

    # Definimos un diccionario de mapeo (User Friendly Name -> Columna técnica)
    METRICS_MAP = {
        "Mediana (Recomendado)": "median_engagement",
        "Promedio (Mean)": "mean_engagement",
        "Desviación (std)": "std_engagement",
        "Promedio de vistas (extra)": "mean_views",
        "Número de videos (extra)": "video_count",
    }

    # Selector:
    selected_column = render_metric_selector(
        "Selecciona la métrica de Engagement:", METRICS_MAP, key="h1_metrics"
    )

    # Gráfico dinámico
    st.bar_chart(data=summary_h1, x="video_type", y=selected_column)


def render_hypothesis_2(df: pd.DataFrame):
    # Análisis Hipótesis 2: El Desgaste del Hype
    st.header("2. ¿Desgaste del Hype?")
    summary_h2 = calculate_correlations(df)
    st.table(summary_h2)  # Tabla para ver coeficientes

    # Creamos el diccionario de mapeo
    METRICS_MAP = {
        "Vistas (log)": "log_viewCount",
        "Engagement": "engagement_rate",
        "Vistas": "viewCount",
    }

    # Creamos el selector
    selected_column = render_metric_selector(
        "Selecciona la variable requerida:", METRICS_MAP, key="h2_metrics"
    )

    # Scatter plot interactivo nativo de Streamlit
    st.scatter_chart(
        data=df, x="days_since_published", y=selected_column, color="video_type"
    )


def render_hypothesis_3(df: pd.DataFrame):
    st.header("3. ¿Cuál es el punto óptimo de duración?")

    # Llamamos a nuestra lógica de análisis pura
    summary_h3 = analyze_duration_segments(df)

    # Mostramos los datos
    st.dataframe(summary_h3, use_container_width=True)

    # Creamos el diccionario de mapeo
    METRICS_MAP = {
        "Promedio Vistas": "mean_views",
        "Mediana Vistas": "median_views",
        "Número de vídeos (extra)": "video_count",
    }

    # Creamos el selector
    selected_column = render_metric_selector(
        "Selecciona la métrica de Vistas:", METRICS_MAP, key="h3_metric"
    )

    # Graficamos la barra con la metrica seleccionada
    st.bar_chart(data=summary_h3, x="duration_segment", y=selected_column)


@st.cache_data
def load_and_preprocess():
    # Carga el parquet pre-procesado directamente
    return pd.read_parquet("data/processed_data.parquet")


def main():
    st.set_page_config(page_title="CR7 YouTube Analysis", layout="wide")
    st.title("📊 Análisis de Rendimiento: Canal de Cristiano Ronaldo")
    # 1. Carga y preprocesamiento (esto se ejecuta una vez y se guarda en cache para mayor eficiencia)
    df = load_and_preprocess()
    # 2.Cargamos las hipothesis:
    render_hypothesis_1(df)
    render_hypothesis_2(df)
    render_hypothesis_3(df)


if __name__ == "__main__":
    main()
