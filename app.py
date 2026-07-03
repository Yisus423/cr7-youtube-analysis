import streamlit as st
import pandas as pd
from src.analysis.shorts_vs_longs import analyze_engagement_by_type
from src.analysis.hype_decay import calculate_correlations
from src.analysis.sweet_spot import analyze_duration_segments


# ---------------------------------------------------------------------------
# CSS personalizado
# ---------------------------------------------------------------------------
st.markdown(
    """
<style>
.hero-title {
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #e6b450 0%, #fce3a1 50%, #e6b450 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.2rem;
}
.hero-subtitle {
    font-size: 1.1rem;
    color: #8a8a8a;
    margin-bottom: 1.5rem;
    letter-spacing: 0.5px;
}
.hero-divider {
    height: 3px;
    background: linear-gradient(90deg, #e6b450, #129153, transparent);
    border-radius: 2px;
    margin: 0.5rem 0 2rem 0;
}
div[data-testid="stMetric"] {
    background: #1a1f2b;
    border: 1px solid #2a3040;
    border-radius: 10px;
    padding: 0.8rem 1rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
}
div[data-testid="stMetric"] label {
    color: #e6b450 !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.5px;
}
.conclusion-box {
    background: linear-gradient(135deg, #1a2030 0%, #1f2a3a 100%);
    border-left: 4px solid #e6b450;
    border-radius: 6px;
    padding: 1.2rem 1.5rem;
    margin: 1.5rem 0;
}
.conclusion-box h4 {
    color: #e6b450;
    margin-top: 0;
    font-size: 1.1rem;
}
.conclusion-box p {
    margin-bottom: 0.3rem;
    line-height: 1.6;
}
.sweet-spot-badge {
    display: inline-block;
    background: linear-gradient(135deg, #e6b450, #c6922d);
    color: #0a0e14;
    font-weight: 800;
    font-size: 1.3rem;
    padding: 0.4rem 1.2rem;
    border-radius: 30px;
    margin: 0.5rem 0;
}
.section-header {
    border-bottom: 2px solid #2a3040;
    padding-bottom: 0.5rem;
    margin-bottom: 1rem;
}
.section-header h2 {
    color: #e6b450;
}
.insights-footer {
    background: linear-gradient(135deg, #1a1520 0%, #1f1a2a 100%);
    border: 1px solid #3a2a40;
    border-radius: 12px;
    padding: 2rem;
    margin-top: 2rem;
}
.insights-footer h2 {
    color: #e6b450;
    text-align: center;
    margin-bottom: 1.5rem;
}
.insight-card {
    background: #1a1f2b;
    border-radius: 8px;
    padding: 1.2rem;
    height: 100%;
    border-top: 3px solid #e6b450;
}
.insight-card h4 {
    color: #59c2ff;
    margin-bottom: 0.5rem;
}
/* Tab styling */
div[data-testid="stTabs"] button {
    font-weight: 600;
    letter-spacing: 0.3px;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
    border-bottom: 3px solid #e6b450 !important;
    color: #e6b450 !important;
}
</style>
""",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Carga de datos (cacheada)
# ---------------------------------------------------------------------------
@st.cache_data
def load_data() -> pd.DataFrame:
    return pd.read_parquet("data/processed_data.parquet")


# ---------------------------------------------------------------------------
# Helpers de UI
# ---------------------------------------------------------------------------
def render_metric_selector(
    label: str, options: dict[str, str], key: str, default_index: int = 0
) -> str:
    selected_label = st.selectbox(
        label, options=list(options.keys()), key=key, index=default_index
    )
    return options[selected_label]


def conclusion_box(title: str, body: str):
    st.markdown(
        f"""
        <div class="conclusion-box">
            <h4>🎯 {title}</h4>
            <p>{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def sweet_spot_badge(text: str):
    st.markdown(
        f'<span class="sweet-spot-badge">🏆 {text}</span>',
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Datos precomputados para KPIs y conclusiones
# ---------------------------------------------------------------------------
df = load_data()

# Métricas globales
total_videos = len(df)
total_shorts = (df["video_type"] == "short").sum()
total_longs = (df["video_type"] == "long").sum()
mean_engagement_global = df["engagement_rate"].mean()
long_engagement_global = df[df["video_type"] == "long"]["engagement_rate"].mean()
short_engagement_global = df[df["video_type"] == "short"]["engagement_rate"].mean()

# H1
summary_h1 = analyze_engagement_by_type(df)
long_row = summary_h1[summary_h1["video_type"] == "long"].iloc[0]
short_row = summary_h1[summary_h1["video_type"] == "short"].iloc[0]
long_views_m = long_row["mean_views"] / 1e6
short_views_m = short_row["mean_views"] / 1e6

# H2
corr_df = calculate_correlations(df)
corr_log = corr_df.loc[
    corr_df["metric"] == "log_viewCount", "pearson_correlation"
].values[0]
corr_engagement = corr_df.loc[
    corr_df["metric"] == "engagement_rate", "pearson_correlation"
].values[0]

# H3
summary_h3 = analyze_duration_segments(df)
best_idx = summary_h3["mean_views"].idxmax()
best_segment = summary_h3.loc[best_idx]
r_3_10 = summary_h3.loc[summary_h3["duration_segment"] == "3-10m", "mean_views"].values[0] / 1e6
r_0_3 = summary_h3.loc[summary_h3["duration_segment"] == "0-3m", "mean_views"].values[0] / 1e6
r_60 = summary_h3.loc[summary_h3["duration_segment"] == "60m+", "mean_views"].values[0] / 1e6


# ═══════════════════════════════════════════════════════════════════════════
#  TABS
# ═══════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📋 Dataset",
    "🥊 Shorts vs Longs",
    "📉 Hype Decay",
    "⏱️ Sweet Spot",
    "📋 Playbook",
])


# ═══════════════════════════════════════════════════════════════════════════
#  TAB 1 — DATASET
# ═══════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<p class="hero-title">CR7 • YouTube Analytics</p>', unsafe_allow_html=True)
    st.markdown(
        f'<p class="hero-subtitle">'
        f"Análisis de rendimiento del canal de Cristiano Ronaldo · "
        f"{total_videos} videos · Sep 2024 – Jun 2026"
        f"</p>",
        unsafe_allow_html=True,
    )
    st.markdown('<div class="hero-divider"></div>', unsafe_allow_html=True)

    # KPIs
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.metric(
            label="🎬 Total Videos",
            value=f"{total_videos}",
            delta=f"{total_shorts} Shorts · {total_longs} Longs",
        )
    with kpi2:
        st.metric(
            label="📈 Engagement Promedio",
            value=f"{mean_engagement_global:.1%}",
            delta=f"Longs {long_engagement_global:.1%} · Shorts {short_engagement_global:.1%}",
        )
    with kpi3:
        st.metric(
            label="🔥 Mejor Formato",
            value="Longs",
            delta=f"{long_views_m:.1f}M vistas vs {short_views_m:.1f}M",
        )
    with kpi4:
        st.metric(
            label="⏱️ Sweet Spot",
            value=f"{best_segment['duration_segment']}",
            delta=f"{best_segment['mean_views'] / 1e6:.1f}M vistas promedio",
        )

    st.markdown("### 📄 Dataset Completo")
    st.markdown(
        """
        Aquí están los **100 videos** del canal de CR7 después del preprocesamiento.
        Cada fila es un video con sus métricas de rendimiento y las columnas calculadas
        durante el feature engineering (`engagement_rate`, `days_since_published`,
        `log_viewCount`, `duration_segment`).
        """
    )
    st.dataframe(df, use_container_width=True)

    st.markdown("### 🧠 Feature Engineering — ¿Cómo se crearon estas columnas?")

    st.markdown(
        """
        El pipeline de preprocesamiento usa `df.pipe()` para encadenar 3 transformaciones
        sobre el dataset crudo. Cada función recibe un DataFrame, lo transforma y lo devuelve.
        """
    )

    with st.expander("1️⃣ `engagement_rate` — Ratio de interacción por video"):
        st.code(
            """
def calculate_engagement_rate(df: pd.DataFrame) -> pd.DataFrame:
    df_clean = df.copy()

    # 1. Los videos sin likes/comentarios no deben romper el cálculo
    df_clean["likeCount"] = df_clean["likeCount"].fillna(0)
    df_clean["commentCount"] = df_clean["commentCount"].fillna(0)

    # 2. viewCount = 0 causaría división por cero.
    #    Lo reemplazamos temporalmente con NA para que Pandas devuelva NaN en lugar de infinito
    view_count_safe = df_clean["viewCount"].replace(0, pd.NA)

    # 3. Engagement rate = (likes + comments) / views
    df_clean["engagement_rate"] = (
        df_clean["likeCount"] + df_clean["commentCount"]
    ) / view_count_safe

    # 4. Los NaN resultantes (videos con 0 vistas) se convierten en 0
    df_clean["engagement_rate"] = df_clean["engagement_rate"].fillna(0)

    return df_clean
            """,
            language="python",
        )

    with st.expander("2️⃣ `days_since_published` — Antigüedad del video en días"):
        st.code(
            """
def compute_days_since_published(df: pd.DataFrame) -> pd.DataFrame:
    df_clean = df.copy()

    # 1. Convertimos el string ISO 8601 a datetime de Pandas
    #    errors="coerce" convierte fechas inválidas en NaT en vez de crash
    df_clean["publishTime"] = pd.to_datetime(df_clean["publishTime"], errors="coerce")

    # 2. Calculamos días desde el video más antiguo del dataset
    #    Esto nos da una escala temporal relativa, no absoluta
    min_date = df_clean["publishTime"].min()
    df_clean["days_since_published"] = (df_clean["publishTime"] - min_date).dt.days

    return df_clean
            """,
            language="python",
        )

    with st.expander("3️⃣ `log_viewCount` — Transformación logarítmica de vistas"):
        st.code(
            """
def add_log_features(df: pd.DataFrame) -> pd.DataFrame:
    df_clean = df.copy()

    # log10(x + 1) es el estándar para manejar ceros sin indefinición
    # La transformación logarítmica "comprime" la escala de millones a unidades manejables
    # y revela relaciones lineales que en escala bruta no se ven
    df_clean["log_viewCount"] = np.log10(df_clean["viewCount"] + 1)

    return df_clean
            """,
            language="python",
        )

    st.markdown(
        """
        > **El orchestrador:** `run_preprocessing_pipeline()` encadena las 3 funciones
        > con `df.pipe()`, manteniendo el código legible y fácil de modificar:
        > ```python
        > return (
        >     df.pipe(calculate_engagement_rate)
        >     .pipe(compute_days_since_published)
        >     .pipe(add_log_features)
        > )
        > ```
        """
    )


# ═══════════════════════════════════════════════════════════════════════════
#  TAB 2 — SHORTS vs LONGS
# ═══════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown(
        '<div class="section-header"><h2>🥊 H1 · ¿Shorts o Videos Largos?</h2></div>',
        unsafe_allow_html=True,
    )

    col_intro, _ = st.columns([3, 1])
    with col_intro:
        st.markdown(
            """
            El formato de contenido lo es todo. En la era de TikTok, los Shorts prometen
            viralidad instantánea — pero en el canal del Bicho, donde cada video es un evento,
            **¿vale la pena sacrificar profundidad por velocidad?**

            Comparamos el engagement rate y las vistas promedio de los **54 videos largos**
            contra los **46 Shorts** publicados hasta la fecha.
            """
        )

    st.markdown("#### 🧠 Código del análisis")
    with st.expander("Ver código de `shorts_vs_longs.py`"):
        st.code(
            """
def analyze_engagement_by_type(df: pd.DataFrame) -> pd.DataFrame:
    # Agrupamos los 100 videos por tipo: 'short' vs 'long'
    summary = (
        df.groupby("video_type")

        # Named Aggregation: cada columna nueva se define como (columna, función)
        .agg(
            mean_engagement=("engagement_rate", "mean"),   # Promedio de engagement por grupo
            median_engagement=("engagement_rate", "median"),  # Mediana (más robusta ante outliers)
            std_engagement=("engagement_rate", "std"),     # Desviación estándar (consistencia)
            mean_views=("viewCount", "mean"),              # Vistas promedio por tipo
            video_count=("video_type", "count"),           # Cuántos videos hay en cada grupo
        )
        .reset_index()  # Convertimos el índice 'video_type' en columna normal
    )
    return summary
            """,
            language="python",
        )

    st.dataframe(summary_h1, use_container_width=True)

    st.markdown("#### 🔍 Explora las métricas por tipo de video")
    METRICS_MAP_H1 = {
        "Mediana (Recomendado)": "median_engagement",
        "Promedio (Mean)": "mean_engagement",
        "Desviación (std)": "std_engagement",
        "Promedio de vistas (extra)": "mean_views",
        "Número de videos (extra)": "video_count",
    }
    selected_col_h1 = render_metric_selector(
        "Selecciona la métrica de Engagement:", METRICS_MAP_H1, key="h1_metrics"
    )
    st.bar_chart(data=summary_h1, x="video_type", y=selected_col_h1)

    conclusion_box(
        title="Conclusión · Gana el formato largo por KO técnico",
        body=(
            f"Aunque los Shorts tienen un <em>mean engagement</em> ligeramente superior "
            f"({short_row['mean_engagement']:.2%} vs {long_row['mean_engagement']:.2%}), "
            f"los videos largos arrasan en <strong>vistas absolutas: {long_views_m:.1f}M</strong> "
            f"contra {short_views_m:.1f}M de los Shorts. "
            f"La audiencia de CR7 no busca píldoras de 30 segundos — busca contenido premium "
            f"de calidad. El verdadero engagement no está en un ratio, está en <strong>"
            f"más de {long_views_m - short_views_m:.1f} millones de vistas extra</strong>."
        ),
    )


# ═══════════════════════════════════════════════════════════════════════════
#  TAB 3 — HYPE DECAY
# ═══════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown(
        '<div class="section-header"><h2>📉 H2 · ¿Desgaste del Hype?</h2></div>',
        unsafe_allow_html=True,
    )

    col_intro2, _ = st.columns([3, 1])
    with col_intro2:
        st.markdown(
            """
            En YouTube, el algoritmo castiga sin piedad: cuanto más viejo es un video,
            menos lo recomienda. Pero… ¿le aplica esa regla a uno de los **canales más
            seguidos del mundo**?

            Medimos la **correlación de Pearson** entre los días transcurridos desde la
            publicación y el rendimiento actual (vistas y engagement).
            """
        )

    st.markdown("#### 🧠 Código del análisis")
    with st.expander("Ver código de `hype_decay.py`"):
        st.code(
            """
def calculate_correlations(df: pd.DataFrame) -> pd.DataFrame:
    # Correlación de Pearson entre antigüedad del video y métricas de rendimiento
    # r = -1 (negativa perfecta) → 0 (sin relación) → +1 (positiva perfecta)
    corr_views = df["days_since_published"].corr(df["viewCount"])
    #                    ⬆ días desde publicación      ⬆ vistas brutas

    corr_engagement = df["days_since_published"].corr(df["engagement_rate"])
    #                                                      ⬆ ratio de interacción

    corr_log_views = df["days_since_published"].corr(df["log_viewCount"])
    #                                                      ⬆ vistas logarítmicas
    # La transformación logarítmica captura mejor el decaimiento exponencial del hype

    # Armamos un DataFrame limpio con los resultados
    correlation_results = pd.DataFrame({
        "metric": ["viewCount", "engagement_rate", "log_viewCount"],
        "pearson_correlation": [corr_views, corr_engagement, corr_log_views],
    })
    return correlation_results
            """,
            language="python",
        )

    st.table(corr_df)

    st.markdown("#### 🔍 Visualiza la tendencia")
    METRICS_MAP_H2 = {
        "Vistas (log)": "log_viewCount",
        "Engagement": "engagement_rate",
        "Vistas": "viewCount",
    }
    selected_col_h2 = render_metric_selector(
        "Selecciona la variable:", METRICS_MAP_H2, key="h2_metrics"
    )
    st.scatter_chart(
        data=df, x="days_since_published", y=selected_col_h2, color="video_type"
    )

    conclusion_box(
        title="Conclusión · El rey resiste, pero no es inmune",
        body=(
            f"Existe una <strong>correlación negativa moderada</strong> entre la antigüedad "
            f"y el rendimiento: <em>r = {corr_log:.2f}</em> para vistas logarítmicas "
            f"y <em>r = {corr_engagement:.2f}</em> para engagement. "
            f"No es un desplome — CR7 mantiene una base sólida incluso en videos con más "
            f"de 600 días. Pero el algoritmo de YouTube sí premia la frescura. "
            f"<strong>La lección táctica: publicar con cadencia constante</strong> para "
            f"mantener el canal en el radar del algoritmo es clave."
        ),
    )


# ═══════════════════════════════════════════════════════════════════════════
#  TAB 4 — SWEET SPOT
# ═══════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown(
        '<div class="section-header"><h2>⏱️ H3 · El Sweet Spot de Duración</h2></div>',
        unsafe_allow_html=True,
    )

    col_intro3, _ = st.columns([3, 1])
    with col_intro3:
        st.markdown(
            """
            Ni un tuit ni una película. ¿Cuál es la duración exacta que maximiza las vistas
            en los videos largos de CR7? Para descubrirlo, segmentamos los 54 videos largos
            en 5 rangos de duración y calculamos el rendimiento promedio de cada uno.
            """
        )

    st.markdown("#### 🧠 Código del análisis")
    with st.expander("Ver código de `sweet_spot.py`"):
        st.code(
            """
def analyze_duration_segments(df: pd.DataFrame) -> pd.DataFrame:
    # Solo nos interesan los videos largos (el concepto de "duración" en Shorts no aplica)
    long_df = df[df["video_type"] == "long"].copy()

    # Definimos los rangos de duración en segundos:
    # 0-3 min = [0, 180s), 3-10 min = [180, 600s), 10-30 min = [600, 1800s),
    # 30-60 min = [1800, 3600s), 60m+ = [3600s, infinito)
    bins = [0, 180, 600, 1800, 3600, float("inf")]
    labels = ["0-3m", "3-10m", "10-30m", "30-60m", "60m+"]

    # pd.cut() segmenta una variable continua en rangos categóricos
    long_df["duration_segment"] = pd.cut(
        long_df["duration_seconds"], bins=bins, labels=labels
    )

    # Agrupamos por segmento y calculamos métricas de rendimiento
    summary = (
        long_df.groupby("duration_segment", observed=True)
        # observed=True asegura que solo aparezcan segmentos con datos reales
        .agg(
            mean_views=("viewCount", "mean"),      # Vistas promedio del segmento
            median_views=("viewCount", "median"),   # Mediana (resistente a outliers)
            video_count=("duration_segment", "count"),  # Cuántos videos caen en este rango
        )
        .reset_index()
    )
    return summary
            """,
            language="python",
        )

    st.dataframe(summary_h3, use_container_width=True)

    st.markdown("#### 🔍 Explora por métrica de vistas")
    METRICS_MAP_H3 = {
        "Promedio Vistas": "mean_views",
        "Mediana Vistas": "median_views",
        "Número de vídeos (extra)": "video_count",
    }
    selected_col_h3 = render_metric_selector(
        "Selecciona la métrica de Vistas:", METRICS_MAP_H3, key="h3_metric"
    )
    st.bar_chart(data=summary_h3, x="duration_segment", y=selected_col_h3)

    # ── Sweet Spot Callout ──
    st.markdown("### 🎯 El Punto Dulce")
    col_ss1, col_ss2 = st.columns([1, 2])
    with col_ss1:
        sweet_spot_badge(f"{best_segment['duration_segment']}")
    with col_ss2:
        st.markdown(
            f"""
            <div style='margin-top: 0.5rem; font-size: 1.1rem;'>
            <strong>{best_segment["mean_views"] / 1e6:.1f} millones de vistas promedio</strong><br>
            <span style='color: #8a8a8a;'>
            {int(best_segment["video_count"])} videos en este rango ·
            mediana de {best_segment["median_views"] / 1e6:.1f}M
            </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    conclusion_box(
        title="Conclusión · 10 a 30 minutos es la zona de gloria",
        body=(
            f"Los videos de <strong>10 a 30 minutos</strong> dominan con autoridad: "
            f"<strong>{best_segment['mean_views'] / 1e6:.1f} millones de vistas promedio</strong>, "
            f"más del doble que el siguiente rango (3-10m con {r_3_10:.1f}M). "
            f"Los videos ultra-cortos (0-3 min: {r_0_3:.1f}M) "
            f"y los maratónicos (60m+: {r_60:.1f}M) "
            f"pierden tracción. "
            f"<strong>La estrategia ganadora es clara: contenido profundo y sustancioso, "
            f"pero sin estirarlo más de media hora.</strong>"
        ),
    )


# ═══════════════════════════════════════════════════════════════════════════
#  TAB 5 — PLAYBOOK
# ═══════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown(
        """
<div class="insights-footer">
<h2>📋 El Playbook de CR7 en YouTube</h2>
</div>
""",
        unsafe_allow_html=True,
    )

    ins1, ins2, ins3 = st.columns(3)
    with ins1:
        st.markdown(
            """
            <div class="insight-card">
            <h4>🥇 Formato Rey</h4>
            <p>Los <strong>videos largos</strong> generan casi el doble de vistas que los Shorts.
            La audiencia de CR7 busca contenido premium, no píldoras rápidas.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with ins2:
        st.markdown(
            """
            <div class="insight-card">
            <h4>🗓️ Cadencia > Viralidad</h4>
            <p>El hype decae (-0.49), pero no se desploma. <strong>La clave es la
            consistencia:</strong> publicar regularmente mantiene el canal siempre
            en la zona caliente del algoritmo.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with ins3:
        st.markdown(
            """
            <div class="insight-card">
            <h4>⏱️ La Fórmula Mágica</h4>
            <p><strong>10-30 minutos</strong> es el rango dorado. Suficiente profundidad
            para enganchar, lo bastante contenido para no saturar. 11.6M de vistas
            no mienten.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
