import streamlit as st
import pandas as pd
from src.analysis.shorts_vs_longs import analyze_engagement_by_type
from src.analysis.hype_decay import calculate_correlations
from src.analysis.sweet_spot import analyze_duration_segments


# ---------------------------------------------------------------------------
# CSS personalizado — estiliza las métricas y tarjetas de conclusión
# ---------------------------------------------------------------------------
st.markdown(
    """
<style>
/* Hero section */
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

/* KPI metric cards */
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

/* Conclusion callout boxes */
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

/* Sweet spot highlight */
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

/* Section headers */
.section-header {
    border-bottom: 2px solid #2a3040;
    padding-bottom: 0.5rem;
    margin-bottom: 1rem;
}
.section-header h2 {
    color: #e6b450;
}

/* Insights footer */
.insights-footer {
    background: linear-gradient(135deg, #1a1520 0%, #1f1a2a 100%);
    border: 1px solid #3a2a40;
    border-radius: 12px;
    padding: 2rem;
    margin-top: 3rem;
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
    with st.container():
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
median_engagement_global = df["engagement_rate"].median()

# H1 — Shorts vs Longs
summary_h1 = analyze_engagement_by_type(df)
long_row = summary_h1[summary_h1["video_type"] == "long"].iloc[0]
short_row = summary_h1[summary_h1["video_type"] == "short"].iloc[0]
long_views_m = long_row["mean_views"] / 1e6
short_views_m = short_row["mean_views"] / 1e6

# H2 — Hype Decay
corr_df = calculate_correlations(df)
corr_log = corr_df.loc[
    corr_df["metric"] == "log_viewCount", "pearson_correlation"
].values[0]
corr_engagement = corr_df.loc[
    corr_df["metric"] == "engagement_rate", "pearson_correlation"
].values[0]

# H3 — Sweet Spot
summary_h3 = analyze_duration_segments(df)
best_idx = summary_h3["mean_views"].idxmax()
best_segment = summary_h3.loc[best_idx]


# ═══════════════════════════════════════════════════════════════════════════
#  HERO SECTION
# ═══════════════════════════════════════════════════════════════════════════
st.markdown('<p class="hero-title">CR7 • YouTube Analytics</p>', unsafe_allow_html=True)
st.markdown(
    f'<p class="hero-subtitle">'
    f"Análisis de rendimiento del canal de Cristiano Ronaldo · "
    f"{total_videos} videos · Sep 2024 – Jun 2026"
    f"</p>",
    unsafe_allow_html=True,
)
st.markdown('<div class="hero-divider"></div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
#  KPI DASHBOARD ROW
# ═══════════════════════════════════════════════════════════════════════════
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
        delta="CR7 mantiene audiencia fiel",
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

st.divider()


# ═══════════════════════════════════════════════════════════════════════════
#  HIPÓTESIS 1 — SHORTS vs LONGS
# ═══════════════════════════════════════════════════════════════════════════
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

st.dataframe(summary_h1, use_container_width=True)

st.subheader("🔍 Explora las métricas por tipo de video")

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

st.divider()


# ═══════════════════════════════════════════════════════════════════════════
#  HIPÓTESIS 2 — EL DESGASTE DEL HYPE
# ═══════════════════════════════════════════════════════════════════════════
st.markdown(
    '<div class="section-header"><h2>📉 H2 · ¿Desgaste del Hype?</h2></div>',
    unsafe_allow_html=True,
)

col_intro2, _ = st.columns([3, 1])
with col_intro2:
    st.markdown(
        """
        En YouTube, el algoritmo castiga sin piedad: cuanto más viejo es un video,
        menos lo recomienda. Pero… ¿le aplica esa regla a  uno de los **canales más seguidos del mundo**?

        Medimos la **correlación de Pearson** entre los días transcurridos desde la
        publicación y el rendimiento actual (vistas y engagement).
        """
    )

st.table(corr_df)

st.subheader("🔍 Visualiza la tendencia")

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

st.divider()


# ═══════════════════════════════════════════════════════════════════════════
#  HIPÓTESIS 3 — EL PUNTO ÓPTIMO DE DURACIÓN
# ═══════════════════════════════════════════════════════════════════════════
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

st.dataframe(summary_h3, use_container_width=True)

st.subheader("🔍 Explora por métrica de vistas")

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
        f"más del doble que el siguiente rango (3-10m con "
        f"{summary_h3.loc[summary_h3['duration_segment'] == '3-10m', 'mean_views'].values[0] / 1e6:.1f}M). "
        f"Los videos ultra-cortos (0-3 min: "
        f"{summary_h3.loc[summary_h3['duration_segment'] == '0-3m', 'mean_views'].values[0] / 1e6:.1f}M) "
        f"y los maratónicos (60m+: "
        f"{summary_h3.loc[summary_h3['duration_segment'] == '60m+', 'mean_views'].values[0] / 1e6:.1f}M) "
        f"pierden tracción. "
        f"<strong>La estrategia ganadora es clara: contenido profundo y sustancioso, "
        f"pero sin estirarlo más de media hora.</strong>"
    ),
)

st.divider()


# ═══════════════════════════════════════════════════════════════════════════
#  FINAL INSIGHTS
# ═══════════════════════════════════════════════════════════════════════════
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
