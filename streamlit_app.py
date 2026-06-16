import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Tirel Isotopen-Rayleigh-Fraktionierung", layout="wide")

st.markdown(
    """
    <style>
    body {
        background-color: #ffe4ec;
        color: #000000;
    }
    .stApp, .main, .block-container {
        background-color: #ffe4ec;
        color: #000000;
    }
    .css-18e3th9 h1, .css-10trblm, .css-1d391kg {
        color: #000000;
    }
    .stTitle, .css-1v0mbdj h1, .css-1tsvksn {
        color: #000000;
    }
    h1 {
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-weight: 700;
    }
    .stMarkdown h1 {
        color: #000000;
    }
    .stSlider label, .stSelectbox label, .stMetric label {
        color: #000000 !important;
    }
    .stMetric {
        color: #000000 !important;
    }
    div[data-testid="metric-container"] {
        color: #000000 !important;
    }
    .metric {
        color: #000000 !important;
    }
    p, label, div {
        color: #000000 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("# Tirel Isotopen-Rayleigh-Fraktionierung")

st.write(
    """
    Diese App zeigt die Rayleigh-Isotopenfraktionierung nach dem Tirel-Modell.
    Stelle den Ausgangswert, den Fraktionierungsfaktor und den verbliebenen Anteil ein.
    Anschließend siehst du den isotopengeführten Verlauf und ein interaktives Kreislaufdiagramm.
    """
)

st.header("1. Rayleigh-Verlauf")

gnip_examples = {
    "Typisches Regenwasser (GNIP)": -8.5,
    "Feuchtes Klima / starke Verdunstung": -12.0,
    "Mäßiger Niederschlag": -6.5,
    "Leichtes Regenwasser": -10.0,
}

col1, col2 = st.columns([2, 1])
with col2:
    selected_precip = st.selectbox(
        "Beispiel aus GNIP-Niederschlagdaten wählen",
        list(gnip_examples.keys()),
        index=0,
    )
    delta0_default = gnip_examples[selected_precip]
    delta0 = st.slider("Anfangswert δ₀ (‰)", -25.0, 0.0, delta0_default, step=0.5)
    alpha = st.slider("Fraktionierungsfaktor α", 1.000, 1.020, 1.005, step=0.001)
    f_wert = st.slider("Verbleibender Anteil f", 0.01, 1.0, 0.5, step=0.01)
    st.markdown("---")
    st.metric("Aktueller δ-Wert", f"{((delta0 + 1000) * f_wert ** (alpha - 1) - 1000):.2f} ‰")
    st.write(
        "Die hier verwendeten Startwerte sind beispielhaft und orientieren sich an typischen "
        "GNIP-Niederschlagswerten für Regenwasser. Für echte GNIP-Daten muss eine entsprechende Datei "
        "heruntergeladen und in die App geladen werden."
    )
    st.caption(
        "Datenquelle: IAEA/WMO Global Network of Isotopes in Precipitation (GNIP). "
        "Accessible at: https://nucleus.iaea.org/wiser"
    )

with col1:
    f = np.linspace(0.01, 1.0, 200)
    delta = (delta0 + 1000) * f ** (alpha - 1) - 1000

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(f, delta, color="#1f77b4", linewidth=2)
    ax.axvline(f_wert, color="#ff7f0e", linestyle="--", label=f"Aktueller Anteil f={f_wert:.2f}")
    ax.set_xlabel("Verbleibender Anteil f", color="black")
    ax.set_ylabel("δ (‰)", color="black")
    ax.set_title("Rayleigh-Isotopenverlauf", color="black")
    ax.tick_params(colors="black")
    ax.grid(alpha=0.3)
    legend = ax.legend()
    for text in legend.get_texts():
        text.set_color("black")
    legend.get_frame().set_facecolor("white")
    legend.get_frame().set_edgecolor("black")
    st.pyplot(fig)

st.markdown(
    "### Erklärung der Rayleigh-Parameter\n"
    "- **Anfangswert δ₀**: Der isotopische Ausgangswert des Reservoirs, bevor Material entfernt wird. "
    "Er gibt an, wie schwer oder leicht das Wasser zu Beginn ist.\n"
    "- **Fraktionierungsfaktor α**: Beschreibt, wie stark sich die Isotopenzusammensetzung zwischen Produkt "
    "und Restreservoir unterscheidet. Ein höherer α-Wert bedeutet stärkere fraktionierende Trennung.\n"
    "- **Verbleibender Anteil f**: Der Anteil des Wassers, der nach dem Entfernen eines Teils noch im Reservoir bleibt. "
    "Wenn f kleiner wird, werden die Isotopenwerte im Restreservoir stärker verändert.\n\n"
    "### Fraktionierung im Wasserkreislauf\n"
    "Fraktionierung tritt überall dort auf, wo Wasserphasenumwandlungen passieren: bei Verdunstung, Kondensation und "
    "Niederschlag. Leichte Isotope (^16O) bevorzugen die Gasphase, schwere Isotope (^18O) bleiben eher in der Flüssigphase. "
    "Das bedeutet im Wasserkreislauf: Verdunstung macht das Verdunstungsprodukt leicht, Kondensation und Niederschlag sorgen "
    "für weiter differenzierte isotopische Signale, und Grundwasser/Abfluss zeigen gemischte oder geglättete Werte."
)

st.header("2. Interaktiver Kreislauf")

st.write(
    "Wähle eine Station, um zu sehen, wie sich dort die Isotopenfraktionierung auswirkt."
)

stations = {
    "Verdunstung": (
        "# 1. Verdunstung (Evaporation)\n\n"
        "### Prozess:\n"
        "Wasser geht von flüssig → gasförmig.\n\n"
        "### Isotopen-Effekt:\n"
        "- Leichte Isotope (^16O) verdampfen leichter.\n"
        "- Dampf wird isotopisch leicht.\n"
        "- Restwasser wird schwerer (höheres δ¹⁸O).\n\n"
        "### Ergebnis:\n"
        "- Atmosphäre: leicht (niedrige δ¹⁸O).\n"
        "- Ozean/See: wird schwerer.\n\n"
        "👉 Hier entsteht oft eine Rayleigh-Fraktionierung."
    ),
    "Kondensation": (
        "# ☁️ 2. Kondensation (Condensation)\n\n"
        "### Prozess:\n"
        "Wasserdampf wird zu Wolken / Tropfen.\n\n"
        "### Effekt:\n"
        "- Schwere Isotope (^18O) kondensieren zuerst.\n"
        "- Regen wird zunehmend leichter, je weiter die Luftmasse zieht.\n\n"
        "### Ergebnis:\n"
        "- frühe Niederschläge: relativ schwer.\n"
        "- spätere / weiter entfernte: sehr leicht.\n\n"
        "👉 Ursache für den latitudinal effect (Pole sind isotopisch leicht)."
    ),
    "Niederschlag": (
        "# 🌧 3. Niederschlag (Precipitation)\n\n"
        "### Prozess:\n"
        "Regen, Schnee, Hagel fällt aus Wolken.\n\n"
        "### Isotopensignatur:\n"
        "- abhängig von Temperatur.\n"
        "- abhängig von Entfernung zur Quelle.\n\n"
        "Typisch:\n"
        "- warm: weniger negativ δ¹⁸O.\n"
        "- kalt: stark negativ δ¹⁸O.\n\n"
        "👉 Wichtigster Klimaindikator!"
    ),
    "Versickerung": (
        "# 🌱 4. Versickerung (Infiltration)\n\n"
        "### Prozess:\n"
        "Wasser gelangt in den Boden.\n\n"
        "### Isotopen-Effekt:\n"
        "- kaum Fraktionierung!\n"
        "- Isotopenwert bleibt fast gleich.\n\n"
        "👉 Das ist wichtig:\n"
        "> Grundwasser = ‚eingefrorenes Niederschlags-Signal‘"
    ),
    "Grundwasser": (
        "# 🧊 5. Grundwasser (Groundwater)\n\n"
        "### Eigenschaften:\n"
        "- Mischung aus vielen Niederschlagsereignissen.\n"
        "- zeitlich geglättet.\n\n"
        "### Isotopenverhalten:\n"
        "- stabil.\n"
        "- kaum saisonale Schwankungen.\n\n"
        "👉 Sehr wichtig für Hydrologie."
    ),
    "Abfluss / Sammlung": (
        "# 🌊 6. Abfluss / Sammlung (Runoff)\n\n"
        "### Prozess:\n"
        "Flüsse sammeln Wasser aus: Regen, Grundwasser und Oberflächenabfluss.\n\n"
        "### Isotopen-Effekt:\n"
        "- Mischung vieler Quellen.\n"
        "- schwankende δ¹⁸O-Werte.\n\n"
        "👉 Flüsse = ‚gemischtes Signal‘."
    ),
}

selected_station = st.radio("Station wählen", list(stations.keys()), index=0, horizontal=True)

fig2, ax2 = plt.subplots(figsize=(8, 8))
ax2.set_xlim(-1.6, 1.6)
ax2.set_ylim(-1.6, 1.6)
ax2.axis("off")

positions = {
    "Verdunstung": (-1.2, 0.5),
    "Kondensation": (0, 1.3),
    "Niederschlag": (1.2, 0.5),
    "Abfluss / Sammlung": (1.3, -0.4),
    "Grundwasser": (0, -1.3),
    "Versickerung": (-1.3, -0.4),
}

for name, (x, y) in positions.items():
    selected = name == selected_station
    color = "#ff7f0e" if selected else "#1f77b4"
    label = name.replace(" / ", "\n/ ")
    ax2.text(
        x,
        y,
        label,
        ha="center",
        va="center",
        fontsize=9,
        weight="bold",
        color="black",
        bbox={
            "boxstyle": "round,pad=0.45",
            "facecolor": color,
            "edgecolor": "k",
            "linewidth": 1,
            "alpha": 0.95,
        },
    )

delta_labels = {
    ("Verdunstung", "Kondensation"): "δ¹⁸O: -5‰ → -8‰",
    ("Kondensation", "Niederschlag"): "δ¹⁸O: -8‰ → -10‰",
    ("Niederschlag", "Abfluss / Sammlung"): "δ¹⁸O: -10‰ → -12‰",
    ("Abfluss / Sammlung", "Versickerung"): "δ¹⁸O: -12‰ → -14‰",
    ("Versickerung", "Grundwasser"): "δ¹⁸O: -14‰ → -13‰",
    ("Grundwasser", "Verdunstung"): "δ¹⁸O: -13‰ → -5‰",
}
paths = [
    ("Verdunstung", "Kondensation"),
    ("Kondensation", "Niederschlag"),
    ("Niederschlag", "Abfluss / Sammlung"),
    ("Abfluss / Sammlung", "Versickerung"),
    ("Versickerung", "Grundwasser"),
    ("Grundwasser", "Verdunstung"),
]
curve_rads = {
    ("Grundwasser", "Verdunstung"): 0.3,
    ("Abfluss / Sammlung", "Versickerung"): -0.2,
    ("Verdunstung", "Kondensation"): 0.0,
    ("Kondensation", "Niederschlag"): 0.0,
    ("Niederschlag", "Abfluss / Sammlung"): 0.0,
    ("Versickerung", "Grundwasser"): 0.0,
}
box_radius = 0.25
for src, dst in paths:
    x0, y0 = positions[src]
    x1, y1 = positions[dst]
    rad = curve_rads.get((src, dst), 0.0)

    dx = x1 - x0
    dy = y1 - y0
    dist = np.hypot(dx, dy)
    start_x = x0 + (dx / dist) * box_radius
    start_y = y0 + (dy / dist) * box_radius
    end_x = x1 - (dx / dist) * box_radius
    end_y = y1 - (dy / dist) * box_radius

    ax2.annotate(
        "",
        xy=(end_x, end_y),
        xytext=(start_x, start_y),
        arrowprops={
            "arrowstyle": "-|>",
            "color": "#444444",
            "linewidth": 2.4,
            "shrinkA": 0,
            "shrinkB": 0,
            "mutation_scale": 20,
            "connectionstyle": f"arc3,rad={rad}",
        },
    )
    mid_x = start_x + (end_x - start_x) * 0.5
    mid_y = start_y + (end_y - start_y) * 0.5
    label = delta_labels.get((src, dst), "")
    if label:
        ax2.text(mid_x, mid_y, label, ha="center", va="center", fontsize=8, color="#333333", bbox={"boxstyle": "round,pad=0.2", "facecolor": "white", "alpha": 0.8, "edgecolor": "none"})

ax2.set_title("Tirel Wasserkreislauf")

col3, col4 = st.columns([1, 1])
with col3:
    st.pyplot(fig2)
with col4:
    st.subheader(selected_station)
    st.write(stations[selected_station])
    st.info("Klicke eine Station an, um den erklärenden Text dazu zu sehen.")

st.write("---")
st.write(
    "Nutze diese App, um die Dynamik von δ-Werten im Tirel-Rayleigh-Modell zu verstehen. "
    "Verändere die Stellschrauben und beobachte, wie sich der Verlauf und die Stationen verhalten."
)
