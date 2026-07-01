import streamlit as st
import pandas as pd
from src.preprocessing import run_preprocessing_pipeline
from src.analysis.shorts_vs_longs import analyze_engagement_by_type
from src.analysis.hype_decay import calculate_correlations
from src.analysis.sweet_spot import analyze_duration_segments


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
    selected_label = st.selectbox(
        "Selecciona la métrica de Engagement:",
        options=list(METRICS_MAP.keys()),
        index=0,  # El primer elemento de la lista (Mediana)
    )

    # Obtenemos el nombre técnico real para graficar
    selected_column = METRICS_MAP[selected_label]

    # Gráfico dinámico
    st.bar_chart(data=summary_h1, x="video_type", y=selected_column)


def render_hypothesis_2(df: pd.DataFrame):
    # Análisis Hipótesis 2: El Desgaste del Hype
    st.header("2. ¿Desgaste del Hype?")
    summary_h2 = calculate_correlations(df)
    st.table(summary_h2)  # Tabla para ver coeficientes

    # Scatter plot interactivo nativo de Streamlit
    st.scatter_chart(
        data=df, x="days_since_published", y="viewCount", color="video_type"
    )


def render_hypothesis_3(df: pd.DataFrame):
    st.header("3. ¿Cuál es el punto óptimo de duración?")

    # 1. Llamamos a nuestra lógica de análisis pura
    summary_h3 = analyze_duration_segments(df)

    # 2. Mostramos los datos
    st.dataframe(summary_h3, use_container_width=True)

    # 3. Visualizamos
    st.subheader("Promedio de vistas por segmento de duración")
    st.bar_chart(data=summary_h3, x="duration_segment", y="mean_views")


@st.cache_data
def load_and_preprocess():
    df = pd.read_csv("data/cristiano_youtube_stats.csv")
    return run_preprocessing_pipeline(df)


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
