import streamlit as st
import altair as alt
import pandas as pd
import numpy as np

st.set_page_config(page_title="One Test for Three Drugs", layout="centered")

# ── Data ─────────────────────────────────────────────────────────────────────
data = [
    {"Bacteria":"Aerobacter aerogenes","Penicillin":870,"Streptomycin":1,"Neomycin":1.6,"Gram_Staining":"negative"},
    {"Bacteria":"Bacillus anthracis","Penicillin":0.001,"Streptomycin":0.01,"Neomycin":0.007,"Gram_Staining":"positive"},
    {"Bacteria":"Brucella abortus","Penicillin":1,"Streptomycin":2,"Neomycin":0.02,"Gram_Staining":"negative"},
    {"Bacteria":"Diplococcus pneumoniae","Penicillin":0.005,"Streptomycin":11,"Neomycin":10,"Gram_Staining":"positive"},
    {"Bacteria":"Escherichia coli","Penicillin":100,"Streptomycin":0.4,"Neomycin":0.1,"Gram_Staining":"negative"},
    {"Bacteria":"Klebsiella pneumoniae","Penicillin":850,"Streptomycin":1.2,"Neomycin":1,"Gram_Staining":"negative"},
    {"Bacteria":"Mycobacterium tuberculosis","Penicillin":800,"Streptomycin":5,"Neomycin":2,"Gram_Staining":"negative"},
    {"Bacteria":"Proteus vulgaris","Penicillin":3,"Streptomycin":0.1,"Neomycin":0.1,"Gram_Staining":"negative"},
    {"Bacteria":"Pseudomonas aeruginosa","Penicillin":850,"Streptomycin":2,"Neomycin":0.4,"Gram_Staining":"negative"},
    {"Bacteria":"Salmonella (Eberthella) typhosa","Penicillin":1,"Streptomycin":0.4,"Neomycin":0.008,"Gram_Staining":"negative"},
    {"Bacteria":"Salmonella schottmuelleri","Penicillin":10,"Streptomycin":0.8,"Neomycin":0.09,"Gram_Staining":"negative"},
    {"Bacteria":"Staphylococcus albus","Penicillin":0.007,"Streptomycin":0.1,"Neomycin":0.001,"Gram_Staining":"positive"},
    {"Bacteria":"Staphylococcus aureus","Penicillin":0.03,"Streptomycin":0.03,"Neomycin":0.001,"Gram_Staining":"positive"},
    {"Bacteria":"Streptococcus fecalis","Penicillin":1,"Streptomycin":1,"Neomycin":0.1,"Gram_Staining":"positive"},
    {"Bacteria":"Streptococcus hemolyticus","Penicillin":0.001,"Streptomycin":14,"Neomycin":10,"Gram_Staining":"positive"},
    {"Bacteria":"Streptococcus viridans","Penicillin":0.005,"Streptomycin":10,"Neomycin":40,"Gram_Staining":"positive"},
]
df = pd.DataFrame(data)

short_names = {
    "Aerobacter aerogenes": "A. aerogenes","Bacillus anthracis": "B. anthracis",
    "Brucella abortus": "B. abortus","Diplococcus pneumoniae": "D. pneumoniae",
    "Escherichia coli": "E. coli","Klebsiella pneumoniae": "K. pneumoniae",
    "Mycobacterium tuberculosis": "M. tuberculosis","Proteus vulgaris": "P. vulgaris",
    "Pseudomonas aeruginosa": "P. aeruginosa","Salmonella (Eberthella) typhosa": "S. typhosa",
    "Salmonella schottmuelleri": "S. schottmuelleri","Staphylococcus albus": "S. albus",
    "Staphylococcus aureus": "S. aureus","Streptococcus fecalis": "S. fecalis",
    "Streptococcus hemolyticus": "S. hemolyticus","Streptococcus viridans": "S. viridans",
}
df["Short"] = df["Bacteria"].map(short_names)

df_long = df.melt(
    id_vars=["Bacteria", "Short", "Gram_Staining"],
    value_vars=["Penicillin", "Streptomycin", "Neomycin"],
    var_name="Antibiotic", value_name="MIC",
)
df_long["log_MIC"] = np.log10(df_long["MIC"])

POS_COLOR = "#2E86AB"
NEG_COLOR = "#E84855"
PEN_COLOR = "#F4A261"
STR_COLOR = "#2A9D8F"
NEO_COLOR = "#9B72CF"

# ── Simple CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  .tag {
    display: inline-block;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 2px 10px;
    border-radius: 20px;
    margin-bottom: 0.5rem;
  }
  .tag-pos { background: #dbeeff; color: #2E86AB; }
  .tag-neg { background: #fde8ea; color: #E84855; }
  .callout {
    background: #f8f9fb;
    border-left: 4px solid #2E86AB;
    border-radius: 0 6px 6px 0;
    padding: 0.9rem 1.2rem;
    margin: 1rem 0 1.5rem;
    font-size: 0.92rem;
    color: #444;
    line-height: 1.65;
  }
  .callout b { color: #111; }
  hr { border: none; border-top: 1px solid #e5e7eb; margin: 2rem 0; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════════
st.title("🔬 The Antibiotic Divide")
st.markdown("""
**Does a bacterium's cell-wall type predict which antibiotic will defeat it?**

The data reveals a strong pattern: **cell-wall type is a good predictor of Penicillin's effectiveness.**
""")

st.markdown("---")

# ═══════════════════════════════════════════════════════════════
# SECTION 1 — Bubble matrix
# ═══════════════════════════════════════════════════════════════
st.subheader("The Full Picture")
st.markdown("""
The chart below shows every bacteria–antibiotic combination as a **bubble**.
- **Color** shows Gram staining: blue = Gram-positive, red = Gram-negative
- **Size** shows MIC. A **smaller bubble means the antibiotic is more effective** (less drug needed)
- **Shape** separates the two Gram types for extra clarity

Hover over any bubble to see the exact MIC value.
""")

df_sorted = df.sort_values(["Gram_Staining", "Penicillin"], ascending=[False, True])
bacteria_order = df_sorted["Short"].tolist()

# Clip log_MIC for size encoding so outliers don't swamp the chart
df_long["log_MIC_clipped"] = df_long["log_MIC"].clip(-3, 3)
# Size: invert so small MIC = big bubble ... wait, we want SMALL bubble = resistant
# Actually: larger bubble = HIGHER MIC = more resistant (bad) — clearer visually
df_long["size_val"] = (df_long["log_MIC_clipped"] + 3)  # shift to 0–6 range

bubble = alt.Chart(df_long).mark_point(filled=True, opacity=0.82).encode(
    x=alt.X("Antibiotic:N",
            sort=["Penicillin", "Streptomycin", "Neomycin"],
            axis=alt.Axis(orient="top", labelAngle=0, labelFontSize=13,
                          title=None, labelFontWeight="bold")),
    y=alt.Y("Short:N", sort=bacteria_order,
            axis=alt.Axis(labelFontSize=11, title=None)),
    color=alt.Color("Gram_Staining:N",
                    scale=alt.Scale(domain=["positive", "negative"],
                                    range=[POS_COLOR, NEG_COLOR]),
                    legend=alt.Legend(title="Gram staining", orient="bottom",
                                      titleFontSize=10, labelFontSize=10)),
    shape=alt.Shape("Gram_Staining:N",
                    scale=alt.Scale(domain=["positive", "negative"],
                                    range=["circle", "square"]),
                    legend=None),
    size=alt.Size("size_val:Q",
                  scale=alt.Scale(range=[20, 900]),
                  legend=alt.Legend(
                      title="Bubble size = MIC (bigger = more resistant)",
                      orient="bottom", titleFontSize=9, labelFontSize=9,
                      values=[0, 2, 4, 6]
                  )),
    tooltip=[
        alt.Tooltip("Bacteria:N", title="Species"),
        alt.Tooltip("Gram_Staining:N", title="Gram staining"),
        alt.Tooltip("Antibiotic:N"),
        alt.Tooltip("MIC:Q", format=".4f", title="MIC (µg/mL)"),
    ]
).properties(width=480, height=420,
             title=alt.TitleParams(
                 text="Antibiotic Effectiveness Across 16 Bacteria",
                 fontSize=14,
                 subtitle="Smaller bubble = lower MIC = more effective antibiotic",
                 subtitleFontSize=10, subtitleColor="gray"
             ))

st.altair_chart(bubble, use_container_width=False)

st.markdown(f"""
<div class="callout">
  <b>What to notice:</b> Look at the <b>Penicillin column</b>.
  <b style="color:{POS_COLOR}">Gram-positive bacteria (blue circles)</b> all have tiny bubbles.
  Penicillin stops them at very low doses.
  <b style="color:{NEG_COLOR}">Gram-negative bacteria (red squares)</b> have large bubbles.
  Penicillin barely touches them even at high doses.
  Streptomycin and Neomycin show a much more mixed, balanced picture across both groups.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════════════
# SECTION 2 — Dot plot (interactive)
# ═══════════════════════════════════════════════════════════════
st.subheader("Compare Antibiotics")
st.markdown("""
Select an antibiotic below to see how its effectiveness breaks down by Gram staining.
The orange line marks **MIC = 1 µg/mL**,
dots below this line indicate the antibiotic works well.
""")

antibiotic_choice = st.selectbox("Select antibiotic:", ["Penicillin", "Streptomycin", "Neomycin"])
focus = df_long[df_long["Antibiotic"] == antibiotic_choice].copy()

dots = alt.Chart(focus).mark_circle(size=120, opacity=0.85).encode(
    x=alt.X("Gram_Staining:N",
            axis=alt.Axis(title="Gram Staining", labelFontSize=13),
            scale=alt.Scale(padding=0.7)),
    y=alt.Y("log_MIC:Q",
            scale=alt.Scale(domain=[-3.5, 3.2]),
            axis=alt.Axis(title="log₁₀(MIC) — lower = more effective", gridColor="#eee")),
    color=alt.Color("Gram_Staining:N",
                    scale=alt.Scale(domain=["positive","negative"], range=[POS_COLOR, NEG_COLOR]),
                    legend=None),
    tooltip=[
        alt.Tooltip("Short:N", title="Species"),
        alt.Tooltip("MIC:Q", format=".4f", title="MIC (µg/mL)"),
        alt.Tooltip("Gram_Staining:N", title="Gram"),
    ]
)

threshold = alt.Chart(pd.DataFrame({"y": [0]})).mark_rule(
    color=PEN_COLOR, strokeDash=[5, 3], strokeWidth=2
).encode(y="y:Q")

threshold_label = alt.Chart(pd.DataFrame({
    "y": [0.2], "x": ["negative"], "label": ["MIC = 1 (effectiveness threshold)"]
})).mark_text(align="left", dx=8, color=PEN_COLOR, fontSize=10).encode(
    x="x:N", y="y:Q", text="label:N"
)

dot_chart = (dots + threshold + threshold_label).properties(
    width=400, height=320,
    title=alt.TitleParams(
        text=f"{antibiotic_choice}: effectiveness by Gram staining",
        fontSize=14, subtitle="Hover over dots to see individual species",
        subtitleFontSize=10, subtitleColor="gray"
    )
)
st.altair_chart(dot_chart, use_container_width=False)

if antibiotic_choice == "Penicillin":
    st.markdown(f"""
<div class="callout">
  <b>Penicillin's split is dramatic.</b> All 7 Gram-positive species fall below the threshold,
  most needing less than 0.05 µg/mL. Three Gram-negative species (A. aerogenes, K. pneumoniae,
  P. aeruginosa) require over 800 µg/mL.
</div>""", unsafe_allow_html=True)
elif antibiotic_choice == "Streptomycin":
    st.markdown("""
<div class="callout">
  <b>Streptomycin is more balanced.</b> Most species of both types fall near or
  below the threshold, though some Streptococci (MIC 10–14) still resist it.
</div>""", unsafe_allow_html=True)
else:
    st.markdown("""
<div class="callout">
  <b>Neomycin is the broadest of the three.</b> The majority of bacteria on both sides of the
  Gram divide respond to low doses. The main exception is <i>S. viridans</i> (MIC = 40).
</div>""", unsafe_allow_html=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════════════
# SECTION 3 — Summary bar chart
# ═══════════════════════════════════════════════════════════════
st.subheader("Part 3 — The Bottom Line")
st.markdown("""
If you only knew a patient had a Gram-positive or Gram-negative infection, which antibiotic
would you reach for? The chart below shows the **median MIC** for each antibiotic, split by Gram type.
Lower is better.
""")

summary = df_long.groupby(["Gram_Staining","Antibiotic"])["MIC"].median().reset_index()
summary["log_Median"] = np.log10(summary["MIC"])
summary["MIC_label"] = summary["MIC"].apply(lambda x: f"{x:.3f} µg/mL")

ab_color_scale = alt.Scale(
    domain=["Penicillin","Streptomycin","Neomycin"],
    range=[PEN_COLOR, STR_COLOR, NEO_COLOR]
)

bars = alt.Chart(summary).mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3).encode(
    x=alt.X("Antibiotic:N", axis=alt.Axis(labelAngle=0, title=None, labelFontSize=11)),
    y=alt.Y("log_Median:Q",
            axis=alt.Axis(title="Median log₁₀(MIC) — lower = more effective", gridColor="#eee")),
    color=alt.Color("Antibiotic:N", scale=ab_color_scale,
                    legend=alt.Legend(orient="top", title="Antibiotic")),
    column=alt.Column("Gram_Staining:N",
                      header=alt.Header(title="Gram Staining", labelFontSize=13,
                                        titleFontSize=11, titleColor="gray")),
    tooltip=[
        alt.Tooltip("Antibiotic:N"),
        alt.Tooltip("Gram_Staining:N", title="Gram"),
        alt.Tooltip("MIC_label:N", title="Median MIC"),
    ]
).properties(
    width=200, height=260,
    title=alt.TitleParams(
        text="Median MIC by antibiotic and Gram staining",
        fontSize=14, subtitle="Lower bars = more effective",
        subtitleFontSize=10, subtitleColor="gray"
    )
)
st.altair_chart(bars, use_container_width=False)

st.markdown(f"""
<div class="callout">
  <b> Choose Penicillin for Gram-positive infections.</b> Its median MIC is lower than
  the other two antibiotics against Gram-positive bacteria.<br><br>
  <b> Choose Neomycin or StreptomycinFor Gram-negative infections.</b> Penicillin's median
  MIC goes up dramatically, while the other two stay low and stable.<br><br>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════════════
# KEY TAKEAWAYS
# ═══════════════════════════════════════════════════════════════
st.subheader("Key Takeaways")
st.markdown(f"""
- **Penicillin works almost exclusively on Gram-positive bacteria**
- **Neomycin is the broadest antibiotic** 
- **Streptomycin is more balanced than Penicillin, but not as broad as Neomycin**
- **No antibiotic is universal.** 


st.markdown("---")
st.markdown("""
<div class="callout" style="border-left-color: #9B72CF; font-size: 0.85rem;">
  <b>About this project</b><br>
  This data story was created in collaboration with <b>Claude (Anthropic)</b><br><br>
  <b>Data source:</b> Burtin, W. (1951). Antibiotic effectiveness data, reproduced via
  <a href="https://cdn.jsdelivr.net/npm/vega-datasets@1/data/burtin.json" target="_blank">Vega Datasets</a>.<br>
</div>
""", unsafe_allow_html=True)
