import streamlit as st
import pandas as pd
from src.preprocessing import calculate_engagement_rate, compute_days_since_published
from src.analysis.shorts_vs_longs import analyze_engagement_by_type
from src.analysis.hype_decay import calculate_correlations


def render_hypothesis_1(df: pd.DataFrame):
    # 2. Análisis Hipótesis 1: Shorts vs Longs
    st.header("1. ¿Shorts o Videos Largos?")
    summary_h1 = analyze_engagement_by_type(df)
    st.dataframe(summary_h1)
    st.bar_chart(data=summary_h1, x="video_type", y="mean_engagement")


def render_hypothesis_2(df: pd.DataFrame):
    # Análisis Hipótesis 2: El Desgaste del Hype
    st.header("2. ¿Desgaste del Hype?")
    summary_h2 = calculate_correlations(df)
    st.table(summary_h2)  # Tabla para ver coeficientes

    # Scatter plot interactivo nativo de Streamlit
    st.scatter_chart(
        data=df, x="days_since_published", y="viewCount", color="video_type"
    )


def main():
    st.set_page_config(page_title="CR7 YouTube Analysis", layout="wide")
    st.title("📊 Análisis de Rendimiento: Canal de Cristiano Ronaldo")
    # 1. Carga y preprocesamiento (esto se ejecuta cada vez que se recarga la app)
    # En un entorno profesional, aquí se usaría st.cache_data para no re-procesar todo
    df = pd.read_csv("data/cristiano_youtube_stats.csv")
    df = calculate_engagement_rate(df)
    df = compute_days_since_published(df)
    # 2.Cargamos las hipothesis:
    render_hypothesis_1(df)
    render_hypothesis_2(df)


if __name__ == "__main__":
    main()
