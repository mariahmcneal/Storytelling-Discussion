import streamlit as st
import altair as alt
import pandas as pd
import numpy as np

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="The Antibiotic Divide",
    page_icon="🔬",
    layout="wide",
)

# ── Data ─────────────────────────────────────────────────────────────────────
data = [
    {"Bacteria":"Aerobacter aerogenes","Penicillin":870,"Streptomycin":1,"Neomycin":1.6,"Gram_Staining":"negative","Genus":"other"},
    {"Bacteria":"Bacillus anthracis","Penicillin":0.001,"Streptomycin":0.01,"Neomycin":0.007,"Gram_Staining":"positive","Genus":"other"},
    {"Bacteria":"Brucella abortus","Penicillin":1,"Streptomycin":2,"Neomycin":0.02,"Gram_Staining":"negative","Genus":"other"},
    {"Bacteria":"Diplococcus pneumoniae","Penicillin":0.005,"Streptomycin":11,"Neomycin":10,"Gram_Staining":"positive","Genus":"other"},
    {"Bacteria":"Escherichia coli","Penicillin":100,"Streptomycin":0.4,"Neomycin":0.1,"Gram_Staining":"negative","Genus":"other"},
    {"Bacteria":"Klebsiella pneumoniae","Penicillin":850,"Streptomycin":1.2,"Neomycin":1,"Gram_Staining":"negative","Genus":"other"},
    {"Bacteria":"Mycobacterium tuberculosis","Penicillin":800,"Streptomycin":5,"Neomycin":2,"Gram_Staining":"negative","Genus":"other"},
    {"Bacteria":"Proteus vulgaris","Penicillin":3,"Streptomycin":0.1,"Neomycin":0.1,"Gram_Staining":"negative","Genus":"other"},
    {"Bacteria":"Pseudomonas aeruginosa","Penicillin":850,"Streptomycin":2,"Neomycin":0.4,"Gram_Staining":"negative","Genus":"other"},
    {"Bacteria":"Salmonella (Eberthella) typhosa","Penicillin":1,"Streptomycin":0.4,"Neomycin":0.008,"Gram_Staining":"negative","Genus":"Salmonella"},
    {"Bacteria":"Salmonella schottmuelleri","Penicillin":10,"Streptomycin":0.8,"Neomycin":0.09,"Gram_Staining":"negative","Genus":"Salmonella"},
    {"Bacteria":"Staphylococcus albus","Penicillin":0.007,"Streptomycin":0.1,"Neomycin":0.001,"Gram_Staining":"positive","Genus":"Staphylococcus"},
    {"Bacteria":"Staphylococcus aureus","Penicillin":0.03,"Streptomycin":0.03,"Neomycin":0.001,"Gram_Staining":"positive","Genus":"Staphylococcus"},
    {"Bacteria":"Streptococcus fecalis","Penicillin":1,"Streptomycin":1,"Neomycin":0.1,"Gram_Staining":"positive","Genus":"Streptococcus"},
    {"Bacteria":"Streptococcus hemolyticus","Penicillin":0.001,"Streptomycin":14,"Neomycin":10,"Gram_Staining":"positive","Genus":"Streptococcus"},
    {"Bacteria":"Streptococcus viridans","Penicillin":0.005,"Streptomycin":10,"Neomycin":40,"Gram_Staining":"positive","Genus":"Streptococcus"},
]
df = pd.DataFrame(data)

# Short bacteria names for display
short_names = {
    "Aerobacter aerogenes": "A. aerogenes",
    "Bacillus anthracis": "B. anthracis",
    "Brucella abortus": "B. abortus",
    "Diplococcus pneumoniae": "D. pneumoniae",
    "Escherichia coli": "E. coli",
    "Klebsiella pneumoniae": "K. pneumoniae",
    "Mycobacterium tuberculosis": "M. tuberculosis",
    "Proteus vulgaris": "P. vulgaris",
    "Pseudomonas aeruginosa": "P. aeruginosa",
    "Salmonella (Eberthella) typhosa": "S. typhosa",
    "Salmonella schottmuelleri": "S. schottmuelleri",
    "Staphylococcus albus": "S. albus",
    "Staphylococcus aureus": "S. aureus",
    "Streptococcus fecalis": "S. fecalis",
    "Streptococcus hemolyticus": "S. hemolyticus",
    "Streptococcus viridans": "S. viridans",
}
df["Short"] = df["Bacteria"].map(short_names)

# Melt to long form
df_long = df.melt(
    id_vars=["Bacteria", "Short", "Gram_Staining", "Genus"],
    value_vars=["Penicillin", "Streptomycin", "Neomycin"],
    var_name="Antibiotic",
    value_name="MIC",
)
df_long["log_MIC"] = np.log10(df_long["MIC"])
df_long["Effective"] = df_long["MIC"] <= 1  # MIC ≤ 1 = clinically effective threshold

# ── Colour palette ────────────────────────────────────────────────────────────
POS_COLOR   = "#2E86AB"   # teal-blue  → Gram-positive
NEG_COLOR   = "#E84855"   # crimson    → Gram-negative
PEN_COLOR   = "#F4A261"   # amber      → Penicillin
STR_COLOR   = "#2A9D8F"   # jade       → Streptomycin
NEO_COLOR   = "#9B72CF"   # violet     → Neomycin
BG          = "#0F1117"
CARD_BG     = "#1A1D27"
TEXT        = "#E8EAF0"
MUTED       = "#8B90A0"

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

  html, body, [data-testid="stAppViewContainer"] {{
    background-color: {BG};
    color: {TEXT};
  }}
  [data-testid="stAppViewContainer"] {{ padding: 0; }}
  [data-testid="block-container"] {{ padding: 2rem 3rem 4rem; max-width: 1200px; margin: 0 auto; }}

  h1, h2, h3 {{ font-family: 'Playfair Display', serif; color: {TEXT}; }}
  p, li, div {{ font-family: 'Inter', sans-serif; }}

  .hero {{ border-bottom: 2px solid {NEG_COLOR}; padding-bottom: 1.5rem; margin-bottom: 2rem; }}
  .hero-eyebrow {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.18em;
    color: {NEG_COLOR};
    text-transform: uppercase;
    margin-bottom: 0.5rem;
  }}
  .hero-title {{
    font-family: 'Playfair Display', serif;
    font-size: clamp(2.4rem, 5vw, 4rem);
    font-weight: 900;
    line-height: 1.1;
    color: {TEXT};
    margin: 0.25rem 0 1rem;
  }}
  .hero-title span {{ color: {NEG_COLOR}; }}
  .hero-deck {{
    font-family: 'Inter', sans-serif;
    font-size: 1.1rem;
    font-weight: 300;
    color: {MUTED};
    max-width: 680px;
    line-height: 1.7;
  }}

  .stat-row {{ display: flex; gap: 1.5rem; margin: 1.5rem 0; flex-wrap: wrap; }}
  .stat-card {{
    background: {CARD_BG};
    border-left: 3px solid {NEG_COLOR};
    padding: 1rem 1.4rem;
    flex: 1;
    min-width: 160px;
    border-radius: 0 6px 6px 0;
  }}
  .stat-number {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 2rem;
    font-weight: 500;
    color: {TEXT};
    line-height: 1;
  }}
  .stat-label {{
    font-size: 0.78rem;
    color: {MUTED};
    margin-top: 0.3rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
  }}

  .section-header {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    color: {POS_COLOR};
    text-transform: uppercase;
    margin-bottom: 0.3rem;
    margin-top: 2.5rem;
  }}
  .section-title {{
    font-family: 'Playfair Display', serif;
    font-size: 1.7rem;
    font-weight: 700;
    color: {TEXT};
    margin: 0 0 0.6rem;
  }}
  .section-body {{
    font-family: 'Inter', sans-serif;
    font-size: 0.97rem;
    color: {MUTED};
    line-height: 1.75;
    max-width: 780px;
    margin-bottom: 1.2rem;
  }}

  .annotation-box {{
    background: {CARD_BG};
    border: 1px solid #2a2d3e;
    border-left: 3px solid {POS_COLOR};
    border-radius: 0 8px 8px 0;
    padding: 1rem 1.4rem;
    margin: 1.2rem 0;
    font-size: 0.9rem;
    color: {MUTED};
    line-height: 1.65;
  }}
  .annotation-box strong {{ color: {TEXT}; }}

  .pullquote {{
    border-left: 4px solid {NEG_COLOR};
    margin: 2rem 0;
    padding: 0.8rem 1.6rem;
    font-family: 'Playfair Display', serif;
    font-size: 1.25rem;
    color: {TEXT};
    font-style: italic;
    line-height: 1.5;
  }}

  .legend-row {{ display: flex; gap: 1.5rem; flex-wrap: wrap; margin: 0.5rem 0 1rem; }}
  .legend-item {{ display: flex; align-items: center; gap: 0.4rem; font-size: 0.82rem; color: {MUTED}; }}
  .legend-dot {{ width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }}

  .takeaway {{
    background: {CARD_BG};
    border-radius: 10px;
    padding: 1.6rem 2rem;
    margin-top: 2rem;
  }}
  .takeaway h3 {{ margin-top: 0; font-size: 1.2rem; }}
  .takeaway ul {{ padding-left: 1.2rem; }}
  .takeaway li {{ color: {MUTED}; margin-bottom: 0.5rem; font-size: 0.93rem; line-height: 1.6; }}
  .takeaway li strong {{ color: {TEXT}; }}

  [data-testid="stHorizontalBlock"] {{ gap: 2rem; }}
  .stSelectbox label {{ color: {MUTED} !important; font-size: 0.82rem !important; }}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# HERO
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
  <div class="hero-eyebrow">🔬 Burtin's Antibiotic Dataset · 1951 · Data Story</div>
  <h1 class="hero-title">The Antibiotic <span>Divide</span></h1>
  <p class="hero-deck">
    In 1951, Will Burtin visualized a quiet truth hiding in clinical data: a bacterium's cell-wall type
    predicts, with striking consistency, which antibiotic will defeat it — and which will fail completely.
    Seventy years later, the pattern is still a masterclass in targeted medicine.
  </p>
</div>
""", unsafe_allow_html=True)

# Stat cards
pos_pen = df[df["Gram_Staining"]=="positive"]["Penicillin"]
neg_pen = df[df["Gram_Staining"]=="negative"]["Penicillin"]
pen_effective_pos = (pos_pen <= 1).sum()
pen_effective_neg = (neg_pen <= 1).sum()

st.markdown(f"""
<div class="stat-row">
  <div class="stat-card">
    <div class="stat-number">{pen_effective_pos}/7</div>
    <div class="stat-label">Gram-positive bacteria defeated by Penicillin (MIC ≤ 1)</div>
  </div>
  <div class="stat-card" style="border-color:{POS_COLOR}">
    <div class="stat-number">{pen_effective_neg}/9</div>
    <div class="stat-label">Gram-negative bacteria defeated by Penicillin (MIC ≤ 1)</div>
  </div>
  <div class="stat-card" style="border-color:{NEO_COLOR}">
    <div class="stat-number">870×</div>
    <div class="stat-label">More Penicillin needed for A. aerogenes vs B. anthracis</div>
  </div>
  <div class="stat-card" style="border-color:{STR_COLOR}">
    <div class="stat-number">16</div>
    <div class="stat-label">Bacterial species · 3 antibiotics · 1 dividing line</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — The Gram Divide (heatmap)
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">Chapter 01</div>', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">One Cell Wall Changes Everything</h2>', unsafe_allow_html=True)
st.markdown("""
<p class="section-body">
  Bacteria are classified by their cell-wall structure: <strong style="color:#2E86AB">Gram-positive</strong>
  bacteria have a thick peptidoglycan wall; <strong style="color:#E84855">Gram-negative</strong> bacteria
  wrap an outer lipid membrane around a thinner wall. This structural difference — invisible to the naked eye —
  determines which antibiotics can penetrate the cell and which are turned away at the door.
  The heatmap below makes this pattern unmistakable. <em>Lower MIC = more effective.</em>
</p>
""", unsafe_allow_html=True)

# Sort bacteria: positives first, then negatives; within each group by penicillin MIC
df_sorted = df.sort_values(["Gram_Staining","Penicillin"], ascending=[False, True])
bacteria_order = df_sorted["Short"].tolist()

heatmap_data = df_long.copy()

# Threshold line annotation data
threshold_line = pd.DataFrame({"MIC_threshold": [0]})  # log10(1) = 0

color_scale = alt.Scale(
    scheme="redyellowblue",
    reverse=True,
    domain=[-3, 3]
)

gram_colors = alt.condition(
    alt.datum.Gram_Staining == "positive",
    alt.value(POS_COLOR),
    alt.value(NEG_COLOR)
)

heatmap = alt.Chart(heatmap_data).mark_rect(
    stroke="#0F1117", strokeWidth=1.5
).encode(
    x=alt.X("Antibiotic:N",
            sort=["Penicillin","Streptomycin","Neomycin"],
            axis=alt.Axis(labelColor=TEXT, titleColor=MUTED, labelFontSize=12,
                          labelFont="Inter", title=None, orient="top",
                          labelAngle=0)),
    y=alt.Y("Short:N",
            sort=bacteria_order,
            axis=alt.Axis(labelColor=TEXT, titleColor=MUTED,
                          labelFontSize=11, labelFont="Inter", title=None)),
    color=alt.Color("log_MIC:Q",
                    scale=color_scale,
                    legend=alt.Legend(title="log₁₀(MIC)  ◀ effective · resistant ▶",
                                      titleColor=MUTED, labelColor=MUTED,
                                      titleFont="Inter", labelFont="JetBrains Mono",
                                      orient="bottom", gradientLength=200)),
    tooltip=[
        alt.Tooltip("Bacteria:N", title="Species"),
        alt.Tooltip("Gram_Staining:N", title="Gram"),
        alt.Tooltip("Antibiotic:N"),
        alt.Tooltip("MIC:Q", format=".3f", title="MIC (µg/mL)"),
    ]
).properties(
    width=520, height=420,
    background="transparent"
).configure_view(strokeWidth=0)

# Gram staining stripe (colored Y-axis labels via a side chart)
gram_stripe = alt.Chart(df_sorted[["Short","Gram_Staining"]].drop_duplicates()).mark_rect(
    width=12
).encode(
    y=alt.Y("Short:N", sort=bacteria_order,
            axis=alt.Axis(labels=False, ticks=False, title=None)),
    color=alt.Color("Gram_Staining:N",
                    scale=alt.Scale(domain=["positive","negative"],
                                    range=[POS_COLOR, NEG_COLOR]),
                    legend=alt.Legend(title="Gram staining",
                                      titleColor=MUTED, labelColor=MUTED,
                                      titleFont="Inter", labelFont="Inter",
                                      orient="bottom")),
    tooltip=[alt.Tooltip("Gram_Staining:N", title="Gram staining")]
).properties(width=14, height=420, background="transparent").configure_view(strokeWidth=0)

col1, col2 = st.columns([1, 14])
with col1:
    st.altair_chart(gram_stripe, use_container_width=False)
with col2:
    st.altair_chart(heatmap, use_container_width=False)

st.markdown(f"""
<div class="annotation-box">
  <strong>How to read this:</strong> Each cell shows the Minimum Inhibitory Concentration (MIC) for one
  bacteria–antibiotic pair on a log scale. <strong style="color:#6ecff6">Blue = low MIC = effective.</strong>
  <strong style="color:#e84855">Red = high MIC = resistant.</strong>
  The colored stripe on the left encodes Gram staining —
  <strong style="color:{POS_COLOR}">teal = Gram-positive</strong>,
  <strong style="color:{NEG_COLOR}">red = Gram-negative</strong>.
  Notice how the Penicillin column is almost entirely blue for Gram-positive species and red for Gram-negative.
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — Penicillin's bias
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">Chapter 02</div>', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">Penicillin: A Drug Built for One Side</h2>', unsafe_allow_html=True)
st.markdown(f"""
<p class="section-body">
  Penicillin works by attacking peptidoglycan — the substance that makes up the thick wall of
  Gram-positive bacteria. Against Gram-negative species, whose outer membrane acts as a shield,
  it is often thousands of times less effective. The dot plot below compares MIC values across
  Gram staining groups for each antibiotic. Select an antibiotic to focus the story.
</p>
""", unsafe_allow_html=True)

antibiotic_choice = st.selectbox(
    "Focus on antibiotic:",
    ["Penicillin", "Streptomycin", "Neomycin"],
    index=0
)

focus_data = df_long[df_long["Antibiotic"] == antibiotic_choice].copy()

dot_base = alt.Chart(focus_data)

dots = dot_base.mark_circle(size=130, opacity=0.9).encode(
    x=alt.X("Gram_Staining:N",
             axis=alt.Axis(labelColor=TEXT, titleColor=MUTED, labelFont="Inter",
                           title="Gram Staining", labelFontSize=13),
             scale=alt.Scale(padding=0.6)),
    y=alt.Y("log_MIC:Q",
            axis=alt.Axis(labelColor=MUTED, titleColor=MUTED, labelFont="JetBrains Mono",
                          title="log₁₀(MIC) — lower = more effective",
                          gridColor="#2a2d3e"),
            scale=alt.Scale(domain=[-3.5, 3.2])),
    color=alt.Color("Gram_Staining:N",
                    scale=alt.Scale(domain=["positive","negative"],
                                    range=[POS_COLOR, NEG_COLOR]),
                    legend=None),
    tooltip=[
        alt.Tooltip("Short:N", title="Species"),
        alt.Tooltip("MIC:Q", format=".4f", title="MIC (µg/mL)"),
        alt.Tooltip("Gram_Staining:N", title="Gram"),
    ]
)

# Threshold line at log10(1) = 0
threshold = alt.Chart(pd.DataFrame({"y": [0]})).mark_rule(
    color="#F4A261", strokeDash=[6, 3], strokeWidth=1.5
).encode(y="y:Q")

threshold_label = alt.Chart(pd.DataFrame({
    "y": [0.15], "x": ["negative"], "label": ["← MIC = 1  (clinical threshold)"]
})).mark_text(
    align="left", dx=5, color="#F4A261",
    font="JetBrains Mono", fontSize=10
).encode(x="x:N", y="y:Q", text="label:N")

dot_chart = (dots + threshold + threshold_label).properties(
    width=380, height=360,
    background="transparent",
    title=alt.TitleParams(
        text=f"{antibiotic_choice}: MIC by Gram Staining",
        color=TEXT, font="Playfair Display", fontSize=16,
        subtitle="Orange line = MIC of 1 µg/mL (practical effectiveness threshold)",
        subtitleColor=MUTED, subtitleFont="Inter", subtitleFontSize=11
    )
).configure_view(strokeWidth=0, fill="transparent").configure_axis(
    gridColor="#1e2130", domainColor="#2a2d3e", tickColor="#2a2d3e"
)

col_dot, col_note = st.columns([1, 1])
with col_dot:
    st.altair_chart(dot_chart, use_container_width=False)
with col_note:
    if antibiotic_choice == "Penicillin":
        st.markdown(f"""
<div class="annotation-box" style="margin-top:3rem">
  <strong>Penicillin's split is stark.</strong> Every Gram-positive species clusters
  <em>below</em> the threshold line — most with MIC values below 0.05 µg/mL.
  Meanwhile, five Gram-negative species require over 100 µg/mL, with three
  (A. aerogenes, K. pneumoniae, P. aeruginosa) exceeding 800 µg/mL.
  That's a <strong>5–6 orders of magnitude</strong> difference in the same drug.
</div>
<div class="pullquote">
  "Gram-negative bacteria simply shrug off Penicillin — the outer membrane
   keeps it from reaching its target."
</div>
""", unsafe_allow_html=True)
    elif antibiotic_choice == "Streptomycin":
        st.markdown(f"""
<div class="annotation-box" style="margin-top:3rem">
  <strong>Streptomycin is more balanced.</strong> Unlike Penicillin, it doesn't rely on
  cell-wall disruption — it inhibits protein synthesis by targeting bacterial ribosomes,
  which exist in both Gram types. Still, some Gram-positive Streptococci (MIC 10–14)
  resist it strongly.
</div>
<div class="pullquote">
  "Streptomycin crosses the Gram divide, but no antibiotic is truly universal."
</div>
""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
<div class="annotation-box" style="margin-top:3rem">
  <strong>Neomycin is the most broadly effective</strong> antibiotic in this dataset.
  The majority of bacteria — both Gram-positive and Gram-negative — fall below or near
  the MIC = 1 threshold. S. viridans (MIC = 40) is the notable outlier.
</div>
<div class="pullquote">
  "Neomycin's broad spectrum makes it powerful — but also increases the risk of
   disrupting beneficial bacteria."
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — Head-to-head comparison
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">Chapter 03</div>', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">Choosing the Right Weapon</h2>', unsafe_allow_html=True)
st.markdown("""
<p class="section-body">
  If you knew a patient had a bacterial infection but not which species, and you only knew whether
  the bacterium was Gram-positive or Gram-negative, which antibiotic would you choose?
  The grouped bar chart below shows the median MIC for each antibiotic split by Gram type —
  a clinician's quick-read summary.
</p>
""", unsafe_allow_html=True)

summary = df_long.groupby(["Gram_Staining","Antibiotic"])["MIC"].median().reset_index()
summary.columns = ["Gram_Staining","Antibiotic","Median_MIC"]
summary["log_Median"] = np.log10(summary["Median_MIC"])
summary["label"] = summary["Median_MIC"].apply(lambda x: f"{x:.3f}")

ab_colors = alt.Scale(
    domain=["Penicillin","Streptomycin","Neomycin"],
    range=[PEN_COLOR, STR_COLOR, NEO_COLOR]
)

bar = alt.Chart(summary).mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3).encode(
    x=alt.X("Antibiotic:N",
            axis=alt.Axis(labelColor=TEXT, labelFont="Inter", title=None,
                          labelAngle=0, labelFontSize=11)),
    y=alt.Y("log_Median:Q",
            axis=alt.Axis(labelColor=MUTED, titleColor=MUTED, labelFont="JetBrains Mono",
                          title="Median log₁₀(MIC) — lower = more effective",
                          gridColor="#2a2d3e")),
    color=alt.Color("Antibiotic:N", scale=ab_colors,
                    legend=alt.Legend(orient="top", titleColor=MUTED,
                                      labelColor=MUTED, labelFont="Inter",
                                      title="Antibiotic")),
    column=alt.Column("Gram_Staining:N",
                      header=alt.Header(
                          titleColor=MUTED, labelColor=TEXT,
                          labelFont="Playfair Display", labelFontSize=14,
                          title="Gram Staining"
                      )),
    tooltip=[
        alt.Tooltip("Antibiotic:N"),
        alt.Tooltip("Gram_Staining:N", title="Gram"),
        alt.Tooltip("label:N", title="Median MIC (µg/mL)"),
    ]
).properties(
    width=220, height=280,
    background="transparent",
    title=alt.TitleParams(
        text="Median MIC by Antibiotic & Gram Staining",
        color=TEXT, font="Playfair Display", fontSize=16,
        subtitle="Lower bars = more effective at lower doses",
        subtitleColor=MUTED, subtitleFont="Inter", subtitleFontSize=11
    )
).configure_view(stroke=None, fill="transparent").configure_axis(
    gridColor="#1e2130", domainColor="#2a2d3e", tickColor="#2a2d3e"
)

st.altair_chart(bar, use_container_width=False)

st.markdown(f"""
<div class="annotation-box">
  <strong>Key read:</strong> For <strong style="color:{POS_COLOR}">Gram-positive</strong> infections,
  Penicillin's median MIC is dramatically lower than Streptomycin or Neomycin — it's the clear first choice.
  For <strong style="color:{NEG_COLOR}">Gram-negative</strong> infections, Penicillin's median MIC
  shoots up by orders of magnitude, while Neomycin and Streptomycin remain relatively low and stable.
  <strong>Gram staining is not just a microbiological detail — it's a treatment decision.</strong>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAKEAWAYS
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="takeaway">
  <h3>📋 What the Data Tells Us</h3>
  <ul>
    <li><strong>Gram staining predicts Penicillin outcomes almost perfectly.</strong>
        Every Gram-positive species in this dataset responds to Penicillin at MIC ≤ 1;
        most Gram-negative species require 10–870× higher concentrations.</li>
    <li><strong>Neomycin is the broadest-spectrum option</strong> of the three,
        working effectively against the widest range of species regardless of Gram type.</li>
    <li><strong>Streptomycin occupies the middle ground</strong> — more effective than
        Penicillin against Gram-negatives, but neither the most potent nor the broadest.</li>
    <li><strong>No antibiotic is universal.</strong> Even Neomycin struggles against
        S. viridans (MIC = 40). Targeted therapy beats broad-spectrum guessing.</li>
    <li><strong>Burtin's 1951 insight still holds:</strong> cell-wall architecture is the
        single most predictive feature of antibiotic susceptibility — a principle that
        guides empirical therapy to this day.</li>
  </ul>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown(f"""
<p style="font-family:'JetBrains Mono',monospace; font-size:0.7rem; color:{MUTED};
   margin-top:3rem; padding-top:1rem; border-top:1px solid #2a2d3e;">
  Data: Burtin (1951) via Vega Datasets · Visualization built with Altair + Streamlit ·
  MIC = Minimum Inhibitory Concentration (µg/mL) · Lower MIC = more effective antibiotic
</p>
""", unsafe_allow_html=True)
