import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
from streamlit_option_menu import option_menu

# ─── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DataMap Maroc",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CUSTOM CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&family=IBM+Plex+Sans:wght@300;400;500&display=swap');

:root {
    --bg:       #0b0f1a;
    --surface:  #111827;
    --surface2: #1a2236;
    --accent:   #f97316;
    --accent2:  #fb923c;
    --gold:     #fbbf24;
    --text:     #e2e8f0;
    --muted:    #64748b;
    --border:   #1e2d45;
    --green:    #34d399;
    --blue:     #60a5fa;
}
html, body, [class*="css"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'IBM Plex Sans', sans-serif;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { 
    padding-top: 1.5rem !important;
}

[data-testid="stSidebar"] {
    display: none; !important;
}
[data-testid="stSidebar"] * { display: none; !important; }
            
.topbar-divider {
    width: 2px;
    height: 38px;
    background: var(--border);
    flex-shrink: 0;
}


.hero-wrap {
    background: linear-gradient(135deg,#0f172a 0%, #1a2236 60%, #0f2030 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 3.5rem 3rem 2.5rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-wrap::before {
    content:'';
    position:absolute; top:-80px; right:-80px;
    width:320px; height:320px;
    background:radial-gradient(circle,rgba(249,115,22,.15) 0%,transparent 70%);
    border-radius:50%;
}
.hero-tag {
    font-family:'Space Mono',monospace;
    font-size:.7rem; letter-spacing:.2em; text-transform:uppercase;
    color:var(--accent);
    background:rgba(249,115,22,.12);
    border:1px solid rgba(249,115,22,.3);
    display:inline-block; padding:4px 12px; border-radius:999px; margin-bottom:1.2rem;
}
.hero-title {
    font-family:'Syne',sans-serif;
    font-size:clamp(2.2rem,4vw,3.4rem); font-weight:800; line-height:1.08;
    margin:0 0 1rem;
    background:linear-gradient(135deg,#f97316,#fbbf24 60%,#fb923c);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
}
.hero-sub {
    font-size:1.1rem; color:#94a3b8; max-width:600px; line-height:1.7; margin-bottom:2rem;
}
.hero-stats { display:flex; gap:2.5rem; flex-wrap:wrap; }
.stat-pill  { display:flex; flex-direction:column; }
.stat-num   { font-family:'Syne',sans-serif; font-size:1.8rem; font-weight:800; color:var(--accent); }
.stat-label { font-family:'Space Mono',monospace; font-size:.65rem; text-transform:uppercase; letter-spacing:.1em; color:var(--muted); }

.sec-header {
    font-family:'Syne',sans-serif; font-size:1.2rem; font-weight:700;
    color:var(--text); border-left:3px solid var(--accent);
    padding-left:.85rem; margin:2.2rem 0 1rem;
}

.def-card {
    background:var(--surface2); border:1px solid var(--border);
    border-top:3px solid var(--accent); border-radius:12px;
    padding:1.5rem 1.8rem; margin-bottom:1.5rem;
}
.def-title { font-family:'Syne',sans-serif; font-size:1.6rem; font-weight:800; color:var(--accent); margin-bottom:.4rem; }
.def-text  { color:#94a3b8; line-height:1.8; font-size:.95rem; }

.metric-tile {
    background:var(--surface2); border:1px solid var(--border);
    border-radius:10px; padding:1.1rem 1.4rem;
}
.metric-val { font-family:'Syne',sans-serif; font-size:1.7rem; font-weight:800; color:var(--gold); }
.metric-lbl { font-family:'Space Mono',monospace; font-size:.62rem; text-transform:uppercase; letter-spacing:.1em; color:var(--muted); margin-top:2px; }

.raw-card {
    background:var(--surface2); border:1px solid var(--border);
    border-radius:10px; padding:1.2rem 1.5rem; margin-bottom:.9rem;
    border-left:3px solid var(--blue);
}
.raw-job  { font-family:'Syne',sans-serif; font-weight:700; font-size:1rem; color:var(--blue); }
.raw-co   { color:var(--gold); font-size:.85rem; margin:2px 0 6px; }
.raw-meta { font-family:'Space Mono',monospace; font-size:.72rem; color:var(--muted); }
.chip-wrap { display:flex; flex-wrap:wrap; gap:6px; margin-top:8px; }
.chip {
    background:rgba(249,115,22,.1); border:1px solid rgba(249,115,22,.3);
    color:var(--accent2); font-family:'Space Mono',monospace;
    font-size:.68rem; padding:3px 10px; border-radius:999px; letter-spacing:.03em;
}

.about-card {
    background:var(--surface2); border:1px solid var(--border);
    border-radius:12px; padding:1.8rem; line-height:1.9; color:#94a3b8; font-size:.93rem;
}
.sb-logo    { font-family:'Syne',sans-serif; font-size: 1.2rem; font-weight:800; color:var(--accent); letter-spacing: -.02em; margin-bottom:.3rem; }
.sb-tagline { font-family:'Space Mono',monospace; font-size:.55rem; color:var(--muted); text-transform:uppercase; letter-spacing:.12em; margin-bottom:1.5rem; padding-bottom:1.2rem; border-bottom:1px solid var(--border); }
hr { border-color: var(--border) !important; margin: 1.5rem 0; }

.stSelectbox > div > div, .stMultiSelect > div > div {
    background:var(--surface2) !important; border-color:var(--border) !important; color:var(--text) !important;
}
div[data-baseweb="select"] * { background:var(--surface2) !important; color:var(--text) !important; }
</style>
""", unsafe_allow_html=True)

# ─── CONSTANTS ─────────────────────────────────────────────────────────────────
SKILL_COLS = [
    'R','Python','SAS','Scala','Spark','Hadoop','Kafka','Snowflake',
    'AWS','Azure','Kubernetes/Docker','Terraform','TensorFlow','PyTorch',
    'OpenAI API','Airflow/Kubeflow','ML/DL','SQL','NoSQL','Excel','PowerBI','Tableau'
]
ACCENT  = "#f97316"
GOLD    = "#fbbf24"
BLUE    = "#60a5fa"
GREEN   = "#34d399"
TEXT    = "#b5bcc5"
MUTED   = "#64748b"
PALETTE = [ACCENT, GOLD, BLUE, GREEN, "#c084fc", "#f472b6", "#38bdf8", "#a3e635"]

# ─── JOB GROUPING ──────────────────────────────────────────────────────────────
JOB_GROUPS = {
    "Data Scientist":   ["Data Scientist", "Data Scientist/ML Engineer", "Data Science Engineer", "Data & IA"],
    "Data Engineer":    ["Data Engineer", "Big Data Engineer", "Ingénieur Big Data", "DataOps Engineer",
                         "Data Engineer & Analyst", "Cloud Data Engineer SQL GCP"],
    "Data Analyst":     ["Data Analyst"],
    "ML / AI Engineer": ["ML Engineer", "AI Engineer", "ML/AI Engineer", "MLOps Engineer",
                         "Cloud DevOps / MLOps Engineer"],
    "Cloud / DevOps":   ["DevOps Engineer", "DevOps / SRE Engineer", "Ingénieur DevOps", "AWS DevOps Engineer",
                         "Cloud Architect", "Ingénieur Cloud", "Ingénieur Cloud GCP", "Ingénieur Cloud Azure",
                         "Ingénieur Cloud AWS", "Ingénieur Cloud Multi-cloud", "Azure Cloud Architect",
                         "AWS Cloud Architect", "DevSecOps Cloud Architect", "Consultant Azure",
                         "Ingénieur Support Google Workspace"],
    "Data Architect":   ["Data Architect", "Architecte Cloud Data/Big Data", "Architecte Data Azure"],
}

def group_title(title):
    for group, members in JOB_GROUPS.items():
        if title in members:
            return group
    return "Autre"

# ─── JOB DEFINITIONS ──────────────────────────────────────────────────────────
JOB_DEFS = {
    "Data Scientist": (
        "Le Data Scientist extrait de la valeur à partir de données complexes en combinant "
        "statistiques, machine learning et storytelling. Au Maroc, c'est l'un des profils les plus "
        "recherchés — notamment dans l'industrie (OCP, AGC), la finance et les ESN. "
        "Il construit des modèles prédictifs, analyse des tendances et aide à la prise de décision stratégique. "
        "Python et SQL sont quasi-obligatoires, avec une forte demande pour ML/DL."
    ),
    "Data Engineer": (
        "Le Data Engineer conçoit et maintient les pipelines qui alimentent les équipes data en données "
        "fiables et accessibles. Au Maroc, c'est la famille la plus représentée dans le dataset — preuve que "
        "les entreprises bâtissent d'abord leur infrastructure avant d'embaucher des Scientists. "
        "Il maîtrise Spark, SQL, Kafka, Airflow, et les plateformes cloud (AWS, Azure, GCP). "
        "Très présent dans les ESN comme SQLI, Devoteam et Novancy."
    ),
    "Data Analyst": (
        "Le Data Analyst transforme les données brutes en insights actionnables via des tableaux de bord "
        "et des analyses statistiques. C'est souvent le premier rôle data accessible aux jeunes diplômés. "
        "Au Maroc, PowerBI, Tableau et Excel sont les outils stars. "
        "Très demandé dans les banques, assurances et retail — un excellent point d'entrée dans la data."
    ),
    "ML / AI Engineer": (
        "Le ML/AI Engineer met en production les modèles IA et les rend robustes, scalables et maintenables. "
        "Il maîtrise le MLOps (Docker, Kubernetes, MLflow) et les frameworks deep learning (TensorFlow, PyTorch). "
        "Avec l'essor de l'IA générative, l'OpenAI API devient un skill différenciateur. "
        "Profil rare mais très bien valorisé au Maroc — souvent recruté par des startups ou des multinationales tech."
    ),
    "Cloud / DevOps": (
        "Le Cloud/DevOps Engineer déploie, automatise et sécurise l'infrastructure technique. "
        "Au Maroc, AWS et Azure dominent le marché cloud. Ce profil est de plus en plus demandé "
        "au croisement du Cloud et de la Data (MLOps, DataOps). "
        "Kubernetes/Docker et Terraform sont les outils clés. Fortement présent dans les ESN et cabinets conseil. "
        "C'est une famille large : de l'ingénieur DevOps pur au Cloud Architect en passant par le DevSecOps."
    ),
    "Data Architect": (
        "Le Data Architect définit la vision technique globale de l'infrastructure data d'une organisation : "
        "modélisation, gouvernance, sécurité et scalabilité. "
        "Rôle senior généralement requis après 7+ ans d'expérience. "
        "Très bien rémunéré, souvent au confluent du Cloud (Azure, AWS) et de la Data Engineering. "
        "Peu d'offres au Maroc — mais les profils qualifiés sont très rares et donc très valorisés."
    ),
}

# ─── PLOTLY LAYOUT ─────────────────────────────────────────────────────────────
def plotly_layout(title=""):
    return dict(
        title=dict(text=title, font=dict(family="Syne", size=14, color=TEXT)),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="IBM Plex Sans", color=TEXT),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT)),
        margin=dict(t=45, b=30, l=20, r=20),
        xaxis=dict(gridcolor="#1e2d45", linecolor="#1e2d45", tickfont=dict(color=MUTED)),
        yaxis=dict(gridcolor="#1e2d45", linecolor="#1e2d45", tickfont=dict(color=MUTED)),
    )

# ─── LOAD DATA ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_excel("Data_Job.xlsx")
    df["City"] = df["City"].str.strip().replace({"Kénitra": "Kenitra"})
    df["Work Mode"] = df["Work Mode"].str.strip()
    df["Job Family"] = df["Job Title"].apply(group_title)
    return df

df = load_data()


logo_col, div_col, nav_col = st.columns([2, 0.05, 5])

with logo_col:
    st.markdown(
        '<div class="sb-logo">DataMap Maroc </div>'
        '<div class="sb-tagline">Explorer · Analyser · S\'orienter</small></div>',
        unsafe_allow_html=True,
    )

with div_col:
    st.markdown('<div class="topbar-divider"></div>', unsafe_allow_html=True)

with nav_col:
    page = option_menu(
        menu_title=None,
        options=["Accueil", "Explorer un Metier", "A propos"],
        icons=["house-fill", "bar-chart-line-fill", "info-circle-fill"],
        orientation="horizontal",
        styles={
            "container": {
                "padding": "0 !important",
                "background-color": "transparent !important",
                "margin": "0 !important",
            },
            "nav": {
                "background-color": "transparent !important",
                "padding": "0 !important",
            },
            "nav-link": {
                "font-family": "IBM Plex Sans, sans-serif",
                "font-size": "0.85rem",
                "color": "#64748b",
                "padding": "6px 16px",
                "border-radius": "8px",
                "background-color": "transparent",
                "white-space": "nowrap",
                "border": "1.5px solid #1e2d45 !important"
            },
            "nav-link-selected": {
                "background-color": "rgba(249,115,22,0.15)",
                "color": "#f97316",
                "font-weight": "600",
            },
            "icon": {"font-size": "0.78rem"},
        },
    )

st.markdown('</div>', unsafe_allow_html=True)  


# ══════════════════════════════════════════════════════════════════════════════
# PAGE : ACCUEIL
# ══════════════════════════════════════════════════════════════════════════════
if "Accueil" in page:

    n_jobs   = len(df)
    n_cities = df["City"].nunique()
    n_titles = df["Job Title"].nunique()

    st.markdown(f"""
    <div class="hero-wrap">
        <div class="hero-tag">🇲🇦 Data Jobs · Maroc 2026</div>
        <h1 class="hero-title">Ton guide pour<br>décrypter les métiers data<br>au Maroc.</h1>
        <p class="hero-sub">
            Tu étudies la data science et tu veux savoir quels métiers existent vraiment au Maroc,
            quelles compétences sont demandées, dans quelles villes et à quel niveau ?
            Ce dashboard répond à tout ça avec des données réelles collectées sur le marché marocain.
        </p>
        <div class="hero-stats">
            <div class="stat-pill">
                <span class="stat-num">{n_jobs}</span>
                <span class="stat-label">Offres analysées</span>
            </div>
            <div class="stat-pill">
                <span class="stat-num">{n_titles}</span>
                <span class="stat-label">Intitulés distincts</span>
            </div>
            <div class="stat-pill">
                <span class="stat-num">{n_cities}</span>
                <span class="stat-label">Villes couvertes</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE : EXPLORER UN MÉTIER
# ══════════════════════════════════════════════════════════════════════════════
elif "Explorer" in page:
    # ─── FILTRES  ───────────────────────────────
    col1, col2, col3 = st.columns(3)

    with col1:
        families = list(JOB_GROUPS.keys())
        selected_family = st.selectbox(
            "Famille métier", 
            families,
            index=None,
            placeholder="Choisir un métiers"
        )

    with col2:
        cities = ["Toutes les villes"] + sorted(df["City"].unique().tolist())
        selected_city = st.selectbox("Ville", cities)

    with col3:
        levels = ["Tous niveaux"] + sorted(df["Experience Level"].unique().tolist())
        selected_level = st.selectbox("Niveau d'expérience", levels)

    show_raw = st.checkbox("📄 Afficher exemples dataset")

# ─── FILTRAGE ───────────────────────────────────────────────
    filtered = df[df["Job Family"] == selected_family].copy()
    if selected_city != "Toutes les villes":
        filtered = filtered[filtered["City"] == selected_city]
    if selected_level != "Tous niveaux":
        filtered = filtered[filtered["Experience Level"] == selected_level]
    
    definition = JOB_DEFS.get(selected_family,
        f"Exploration des offres marocaines pour la famille : {selected_family}.")

    st.markdown(f"""
        <div class="def-card">
        <div class="def-title">{selected_family}</div>
        <div class="def-text">{definition}</div>
    </div>
    """, unsafe_allow_html=True)

    if filtered.empty:
        st.warning("Aucune offre disponible pour cette combinaison de filtres.")
        st.stop()

    # Métriques
    count     = len(filtered)
    top_city  = filtered["City"].value_counts().idxmax()
    top_level = filtered["Experience Level"].value_counts().idxmax()
    top_mode  = filtered["Work Mode"].value_counts().idxmax()

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f'<div class="metric-tile"><div class="metric-val">{count}</div><div class="metric-lbl">Offres dans le dataset</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="metric-tile"><div class="metric-val">{top_city}</div><div class="metric-lbl">Ville principale</div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="metric-tile"><div class="metric-val">{top_level}</div><div class="metric-lbl">Niveau le + demandé</div></div>', unsafe_allow_html=True)
    with m4:
        st.markdown(f'<div class="metric-tile"><div class="metric-val">{top_mode}</div><div class="metric-lbl">Mode de travail dominant</div></div>', unsafe_allow_html=True)

    st.markdown("")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="sec-header">Répartition géographique</div>', unsafe_allow_html=True)
        city_c = filtered["City"].value_counts().reset_index()
        city_c.columns = ["Ville","Offres"]
        fig = px.pie(city_c, names="Ville", values="Offres",
                     color_discrete_sequence=PALETTE, hole=0.45)
        fig.update_layout(**plotly_layout())
        fig.update_traces(textfont_color=TEXT)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="sec-header">Niveau d\'expérience requis</div>', unsafe_allow_html=True)
        lv = filtered["Experience Level"].value_counts().reset_index()
        lv.columns = ["Niveau","Count"]
        order = ["Junior","Mid","Senior"]
        lv["Niveau"] = pd.Categorical(lv["Niveau"], categories=order, ordered=True)
        lv = lv.sort_values("Niveau")
        fig2 = px.bar(lv, x="Niveau", y="Count",
                      color="Niveau", color_discrete_sequence=[GREEN, GOLD, ACCENT])
        fig2.update_layout(**plotly_layout(), showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    # Skills bar + radar
    st.markdown('<div class="sec-header">Compétences demandées dans cette famille</div>', unsafe_allow_html=True)
    skill_data = {col: int(filtered[col].sum()) for col in SKILL_COLS if col in filtered.columns}
    skill_data = {k: v for k, v in skill_data.items() if v > 0}
    sk_df = pd.DataFrame(
        sorted(skill_data.items(), key=lambda x: x[1], reverse=True),
        columns=["Skill","Offres"]
    )

    col3, col4 = st.columns([3, 2])
    with col3:
        fig3 = px.bar(sk_df, x="Offres", y="Skill", orientation="h",
                      color="Offres",
                      color_continuous_scale=[[0,"#1a2236"],[0.4,BLUE],[1,ACCENT]])
        fig3.update_layout(**plotly_layout())
        fig3.update_coloraxes(showscale=False)
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        top8 = sk_df.head(8)
        if len(top8) >= 3:
            fig_radar = go.Figure(go.Scatterpolar(
                r=top8["Offres"].tolist() + [top8["Offres"].iloc[0]],
                theta=top8["Skill"].tolist() + [top8["Skill"].iloc[0]],
                fill='toself',
                fillcolor="rgba(249,115,22,0.15)",
                line=dict(color=ACCENT, width=2),
            ))
            fig_radar.update_layout(
                polar=dict(
                    bgcolor="rgba(0,0,0,0)",
                    radialaxis=dict(visible=True, showticklabels=False,
                                   gridcolor="#1e2d45", linecolor="#1e2d45"),
                    angularaxis=dict(tickfont=dict(size=10, color=TEXT), gridcolor="#1e2d45"),
                ),
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(family="IBM Plex Sans", color=TEXT),
                showlegend=False,
                margin=dict(t=30, b=30, l=50, r=50),
            )
            st.plotly_chart(fig_radar, use_container_width=True)

    col5, col6 = st.columns(2)
    with col5:
        st.markdown('<div class="sec-header">Mode de travail</div>', unsafe_allow_html=True)
        wm = filtered["Work Mode"].value_counts().reset_index()
        wm.columns = ["Mode","Count"]
        fig5 = px.bar(wm, x="Mode", y="Count",
                      color="Mode", color_discrete_sequence=PALETTE)
        fig5.update_layout(**plotly_layout(), showlegend=False)
        st.plotly_chart(fig5, use_container_width=True)

    with col6:
        st.markdown('<div class="sec-header">Intitulés de postes réels dans le dataset</div>', unsafe_allow_html=True)
        titles_c = filtered["Job Title"].value_counts().reset_index()
        titles_c.columns = ["Intitulé","Count"]
        fig6 = px.bar(titles_c, x="Count", y="Intitulé", orientation="h",
                      color="Count", color_continuous_scale=[[0,"#1a2236"],[1,GOLD]])
        fig6.update_layout(**plotly_layout())
        fig6.update_coloraxes(showscale=False)
        st.plotly_chart(fig6, use_container_width=True)

    # Heatmap skills × niveau
    st.markdown('<div class="sec-header">Skills demandées par niveau d\'expérience</div>', unsafe_allow_html=True)
    avail_skills = [c for c in SKILL_COLS if c in filtered.columns]
    skill_by_level = filtered.groupby("Experience Level")[avail_skills].sum()
    skill_by_level = skill_by_level.loc[:, skill_by_level.sum() > 0]
    if not skill_by_level.empty and len(skill_by_level) > 1:
        fig7 = px.imshow(
            skill_by_level,
            color_continuous_scale=[[0,"#0b0f1a"],[0.5,"#1e3a5f"],[1,ACCENT]],
            aspect="auto",
            labels=dict(x="Skill", y="Niveau", color="Offres"),
        )
        fig7.update_layout(**plotly_layout())
        fig7.update_xaxes(tickangle=-35)
        st.plotly_chart(fig7, use_container_width=True)
    elif not skill_by_level.empty:
        st.info("Sélectionne plusieurs niveaux d'expérience pour afficher le heatmap comparatif.")

    # Raw data examples
    if show_raw:
        st.markdown('<div class="sec-header">📋 Exemples d\'offres dans le dataset</div>', unsafe_allow_html=True)
        sample = filtered.sample(min(4, len(filtered)), random_state=42)
        for _, row in sample.iterrows():
            skills_present = [col for col in SKILL_COLS if col in row and row[col] == 1]
            chips_html = "".join(f'<span class="chip">{s}</span>' for s in skills_present)
            chip_block = f'<div class="chip-wrap">{chips_html}</div>' if chips_html else ""

            st.markdown(f"""
            <div class="raw-card">
                <div class="raw-job">{row['Job Title']}</div>
                <div class="raw-co">🏢 {row.get('Company','—')} · 📍 {row.get('City','—')}</div>
                <div class="raw-meta">
                    🎯 {row.get('Experience Level','—')} &nbsp;|&nbsp;
                    🌐 {row.get('Work Mode','—')} &nbsp;|&nbsp;
                    🗂 {row.get('Job Family','—')}
                </div>
                {chip_block}
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE : À PROPOS
# ══════════════════════════════════════════════════════════════════════════════
elif "propos" in page:

    st.markdown('<div class="sec-header">À propos de DataMap Maroc</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="about-card">
        <p>
        <strong style="color:#f97316;">DataMap Maroc</strong> est un outil d'exploration des métiers de la data
        au Maroc, conçu par et pour des étudiants en data science. Il centralise les informations
        issues d'offres d'emploi réelles — compétences, villes, niveaux d'expérience, modes de travail —
        pour aider à mieux s'orienter dans l'écosystème data marocain.
        </p>
        <p>
        📊 <strong style="color:#60a5fa;">Ce que tu peux faire ici :</strong><br>
        Explorer les familles de métiers (Data Scientist, Data Engineer, ML/AI Engineer...),
        comprendre les compétences les plus demandées grâce aux graphiques et au radar,
        voir la répartition géographique, et consulter des exemples concrets du dataset.
        </p>
        <p>
        🗂️ <strong style="color:#60a5fa;">Le dataset :</strong><br>
        <strong style="color:#e2e8f0;">{len(df)} offres</strong> collectées et annotées manuellement
        depuis des plateformes d'emploi marocaines. Chaque offre est taggée avec les skills requises
        (Python, SQL, Spark, PowerBI, etc.), le niveau d'expérience (Junior / Mid / Senior),
        la ville et le mode de travail.
        </p>
        <p>
        🏙️ <strong style="color:#60a5fa;">Couverture géographique :</strong><br>
        {df['City'].nunique()} villes représentées. Casablanca concentre la majorité des offres,
        suivie de Rabat. Les opportunités hors axes sont encore rares mais en croissance.
        </p>
        <p>
        🚀 <strong style="color:#60a5fa;">Comment utiliser l'app :</strong><br>
        Utilise la sidebar pour filtrer par famille de métier, ville et niveau d'expérience.
        Active "Afficher des exemples" pour voir des offres réelles avec les skills demandées.
        Explore le heatmap Skills × Niveau pour savoir quoi apprendre en priorité selon ton profil.
        </p>
        <p style="color:#64748b;font-size:.82rem;margin-top:1.5rem;">
        💡 Built with Streamlit · Plotly · Pandas &nbsp;|&nbsp; Made with ❤️ in Morocco 🇲🇦
        </p>
    </div>
    """, unsafe_allow_html=True)
