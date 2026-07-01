import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(page_title="Isotopen Rayleigh Fraktionierung", layout="wide")

# App nur auf Deutsch
st.session_state.language = "DE"

# Übersetzungen für DE/EN (kurz gehalten)
TRANSLATIONS = {
    "DE": {
        "title": "Isotopen Rayleigh Fraktionierung",
        "welcome_html": """
        <div style=\"background: linear-gradient(180deg, #fff0f6 0%, #ffe4f0 100%) !important; border: 3px solid #ff69b4 !important; border-radius: 16px; padding: 22px; margin: 20px 0; box-shadow: 0 18px 35px rgba(255, 105, 180, 0.15), 0 6px 18px rgba(0, 0, 0, 0.08);\">
            <p style=\"color: #000000; line-height: 1.8; font-size: 16px;\">🌍 <strong>Willkommen!</strong> Diese App visualisiert die <strong>Rayleigh-Isotopenfraktionierung</strong> anhand realer Niederschlagsdaten des <strong>Global Network of Isotopes in Precipitation (GNIP)</strong> der IAEA.</p>
            <p style=\"color: #000000; line-height: 1.8;\">Experimentiere interaktiv mit dem Modell: Stelle den Ausgangswert, den Fraktionierungsfaktor und den verbliebenen Anteil ein und beobachte in Echtzeit, wie sich die Isotopenzusammensetzung verändert.</p>
            <p style=\"color: #000000; line-height: 1.8;\">Visualisiere den komplexen Wasserkreislauf mit unserem interaktiven Diagramm und verstehe, warum Niederschlag in verschiedenen Klimazonen unterschiedliche isotopische Signaturen hat – ein Schlüssel zur Wassermarkierung in der modernen Hydrologie und Klimatologie.</p>
        </div>
        """,
        "expander1_title": "Was ist Rayleigh-Fraktionierung?",
        "expander1_html": None,
        "expander2_title": "Grundlagen",
        "header1": "1. Rayleigh-Verlauf",
        "select_gnip": "Beispiel aus GNIP-Niederschlagdaten wählen",
        "slider_delta0": "Anfangswert δ₀ (‰)",
        "slider_alpha": "Fraktionierungsfaktor α",
        "slider_f": "Verbleibender Anteil f",
        "metric_current_delta": "Aktueller δ-Wert",
    },
    "EN": {
        "title": "Isotope Rayleigh Fractionation",
        "welcome_html": """
        <div style=\"background: linear-gradient(180deg, #fff0f6 0%, #ffe4f0 100%) !important; border: 3px solid #ff69b4 !important; border-radius: 16px; padding: 22px; margin: 20px 0; box-shadow: 0 18px 35px rgba(255, 105, 180, 0.15), 0 6px 18px rgba(0, 0, 0, 0.08);\">
            <p style=\"color: #000000; line-height: 1.8; font-size: 16px;\">🌍 <strong>Welcome!</strong> This app visualizes <strong>Rayleigh isotope fractionation</strong> using precipitation data from the <strong>Global Network of Isotopes in Precipitation (GNIP)</strong> by the IAEA.</p>
            <p style=\"color: #000000; line-height: 1.8;\">Interactively change the initial value, fractionation factor and remaining fraction to see how isotope composition evolves in real time.</p>
            <p style=\"color: #000000; line-height: 1.8;\">Visualize the water cycle and understand why precipitation shows different isotopic signatures across climates — a key for hydrology and climate studies.</p>
        </div>
        """,
        "expander1_title": "What is Rayleigh fractionation?",
        "expander1_html": None,
        "expander2_title": "Basics",
        "header1": "1. Rayleigh curve",
        "select_gnip": "Choose GNIP precipitation example",
        "slider_delta0": "Initial δ₀ (‰)",
        "slider_alpha": "Fractionation factor α",
        "slider_f": "Remaining fraction f",
        "metric_current_delta": "Current δ value",
    },
}

# Shortcut to current language map
T = TRANSLATIONS.get(st.session_state.language, TRANSLATIONS["DE"])

st.markdown(
    """
    <style>
    body {
        background-color: #f3e2c7;
        color: #000000;
    }
    .stApp, .main, .block-container {
        background-color: #f3e2c7;
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
    .stSelectbox > div > div {
        border: 2px solid #ff69b4 !important;
        border-radius: 8px;
        background-color: white !important;
        color: #000000 !important;
    }
    /* Ensure dropdown and option items are white with black text */
    .stSelectbox,
    .stSelectbox select,
    .stSelectbox div[role="listbox"],
    .stSelectbox .css-1hwfws3,
    .stSelectbox .css-1hwfws3 div[role="option"] {
        background-color: white !important;
        color: #000000 !important;
    }
    /* Style expander containers with black border */
    .streamlit-expanderContent {
        border: 3px solid black !important;
        border-radius: 16px;
    }
    [data-testid="stExpander"] {
        border: 3px solid black !important;
        border-radius: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown(f'<h1 style="text-decoration: underline; margin: 0;">{T["title"]}</h1>', unsafe_allow_html=True)

st.markdown(T["welcome_html"], unsafe_allow_html=True)

with st.expander("Was ist Rayleigh-Fraktionierung?"):
    st.markdown(
        """
        <div style="
            background: linear-gradient(180deg, #ffe4f0 0%, #ffd1e6 100%) !important;
            border: 3px solid black !important;
            border-radius: 16px;
            padding: 22px;
            margin: 20px 0;
            box-shadow: 0 18px 35px rgba(255, 105, 180, 0.18), 0 6px 18px rgba(0, 0, 0, 0.08);
            transform: perspective(800px) rotateX(2deg);
            transform-origin: top center;
        ">
            <p style="color: #000000; line-height: 1.6;">
            Die Rayleigh-Fraktionierung ist ein mathematisches Modell, das beschreibt, wie sich die Zusammensetzung eines Systems mit mehreren Phasen ändert, wenn eine Phase kontinuierlich entfernt wird – beispielsweise durch fraktionierte Destillation.
            </p>
            <p style="color: #000000; line-height: 1.6;">
            Besonders relevant ist dieses Prinzip in der Isotopengeochemie, Hydrologie und Meteorologie, wo es die isotopische Differenzierung von Wasser während Kondensationsprozessen erklärt.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with st.expander("Grundlagen"):
    st.markdown(
        """
        <div style="
            background: linear-gradient(180deg, #ffe4f0 0%, #ffd1e6 100%) !important;
            border: 3px solid black !important;
            border-radius: 16px;
            padding: 22px;
            margin: 20px 0;
            box-shadow: 0 18px 35px rgba(255, 105, 180, 0.18), 0 6px 18px rgba(0, 0, 0, 0.08);
            transform: perspective(800px) rotateX(2deg);
            transform-origin: top center;
        ">
            <ul style="color: #000000; line-height: 1.6; margin-top: 0; padding-left: 18px;">
                <li>Ein System enthält Moleküle mit unterschiedlichen Isotopen, z. B. <strong>¹⁸O/¹⁶O in Wasser</strong> oder <strong>³⁴S/³²S in Sulfat</strong>.</li>
                <li>Eine Phase wird selektiv entfernt, z. B. durch Kondensation von Wasserdampf, während die verbleibende Phase ihre isotopische Zusammensetzung ändert.</li>
                <li>Der Fraktionierungsfaktor <strong>α</strong> beschreibt, wie stark sich die Isotope zwischen den beiden Reservoirs unterscheiden.</li>
                <li>Bei <strong>α = 1,03</strong> verbleibt das schwerere Isotop (z. B. ¹⁸O) bevorzugt in der flüssigen Phase, während das leichtere Isotop (¹⁶O) bevorzugt verdampft.</li>
                <li>Der Fraktionierungsfaktor wird als konstant während des Prozesses angenommen.</li>
            </ul>
            <p style="color: #000000; line-height: 1.6; font-weight: bold;">
            Formel der Rayleigh-Fraktionierung
            </p>
            <p style="color: #000000; line-height: 1.6;">
            Die Rayleigh-Gleichung beschreibt das Verhältnis der verbleibenden Phase als Funktion des verbleibenden Anteils <strong>f</strong> und des Fraktionierungsfaktors <strong>α</strong>:
            </p>
            <p style="color: #000000; line-height: 1.6; font-size: 1.05em;">
            <strong>R = R₀ × f<sup>α−1</sup></strong>
            </p>
            <p style="color: #000000; line-height: 1.6;">
            Dabei ist <strong>R</strong> das aktuelle Isotopenverhältnis in der verbleibenden Phase, <strong>R₀</strong> das Anfangsverhältnis, <strong>f</strong> der Anteil der verbleibenden Substanz und <strong>α</strong> der Fraktionierungsfaktor.
            </p>
            <p style="color: #000000; line-height: 1.6; font-weight: bold;">
            Mathematische Berechnung:
            </p>
            <ul style="color: #000000; line-height: 1.6; margin-top: 8px;">
                <li><strong>Schritt 1:</strong> Berechne den Exponenten: <strong>α − 1</strong></li>
                <li><strong>Schritt 2:</strong> Erhebe <strong>f</strong> (den verbleibenden Anteil) zur Potenz (α − 1): <strong>f<sup>α−1</sup></strong></li>
                <li><strong>Schritt 3:</strong> Multipliziere mit dem Anfangsverhältnis: <strong>R = R₀ × f<sup>α−1</sup></strong></li>
            </ul>
            <p style="color: #000000; line-height: 1.6; font-weight: bold;">
            Beispiel Berechnung:
            </p>
            <p style="color: #000000; line-height: 1.6;">
            Mit R₀ = 0,002 (Anfangswert), α = 1,005 und f = 0,5 (50% verbleibend):
            </p>
            <ul style="color: #000000; line-height: 1.6; margin-top: 8px;">
                <li>α − 1 = 1,005 − 1 = 0,005</li>
                <li>f<sup>α−1</sup> = 0,5<sup>0,005</sup> ≈ 0,9965</li>
                <li>R = 0,002 × 0,9965 ≈ 0,001993</li>
            </ul>
            <p style="color: #000000; line-height: 1.6; font-weight: bold;">
            &#128161; Zum Merken!<br>
            Je mehr Material entfernt wird, desto stärker verändert sich die isotopische Zusammensetzung der verbleibenden Phase.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<div style='height:80px;'></div>", unsafe_allow_html=True)


st.header("1. Rayleigh-Verlauf")

st.markdown("### Rayleigh-Fraktionierung: Formeln")
st.markdown("**Verdunstung**")
st.markdown("- Isotopenverhältnis der verbleibenden Flüssigkeit:")
st.latex(r"R_l = R_{l0} \cdot f^{\alpha - 1}")
st.markdown("- Isotopenverhältnis des aktuell verdampfenden Gases:")
st.latex(r"R_v = \alpha \cdot R_l = \alpha \cdot R_{l0} \cdot f^{\alpha - 1}")
st.markdown("- Isotopenverhältnis des bisher verdampften Gases:")
st.latex(r"\overline{R_v} = R_{l0} \cdot \frac{1 - f^{\alpha}}{1 - f}")

st.markdown("**Kondensation**")
st.markdown("- Isotopenverhältnis der verbleibenden Gasphase:")
st.latex(r"R_v = R_{v0} \cdot f^{\alpha-1}")
st.markdown("- Isotopenverhältnis der aktuell kondensierenden Flüssigkeit:")
st.latex(r"R_l = R_{v0} \cdot \alpha \cdot f^{\alpha-1}")
st.markdown("- Isotopenverhältnis der bisher kondensierten Flüssigkeit:")
st.latex(r"\overline{R_l} = R_{v0} \cdot \frac{1 - f^{\alpha}}{1 - f}")

st.markdown("**Variablen**")
st.markdown("- $R_{l0}$ = anfängliches Isotopenverhältnis der Flüssigkeit")
st.markdown("- $R_{v0}$ = anfängliches Isotopenverhältnis der Gasphase")
st.markdown("- $R_l$ = Isotopenverhältnis der aktuellen Flüssigkeit")
st.markdown("- $R_v$ = Isotopenverhältnis der aktuellen Gasphase")
st.markdown("- $\overline{R}$ = mittleres Isotopenverhältnis des bereits gebildeten Produkts")
st.markdown("- $f$ = verbleibender Anteil der Ausgangsphase")
st.markdown("- $\alpha$ = Gleichgewichts-Fraktionierungsfaktor")

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

    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(f, delta, color="#1f77b4", linewidth=2)
    ax.axvline(f_wert, color="#ff7f0e", linestyle="--", label=f"Aktueller Anteil f={f_wert:.2f}")
    ax.set_xlabel("Verbleibender Anteil f", color="black")
    ax.set_ylabel("δ (‰)", color="black")
    ax.set_title("Rayleigh-Isotopenverlauf", color="black")
    ax.set_ylim(-40, 10)
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
    "Wenn f kleiner wird, werden die Isotopenwerte im Restreservoir stärker verändert.\n"
    "- **Aktueller δ-Wert**: Zeigt die **isotopische Zusammensetzung der verbleibenden Probe** nach der Rayleigh-Fraktionierung. "
    "Der Wert wird in **Promille (‰)** angegeben, relativ zum SMOW-Standard. "
    "**δ < 0 ‰** bedeutet, die Probe ist isotopisch **leicht** (weniger ¹⁸O). **δ > 0 ‰** bedeutet isotopisch **schwer** (mehr ¹⁸O). "
    "Je stärker die Fraktionierung (niedriger f und höher α), desto größer die Abweichung vom Ausgangswert.\n\n"
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
        "### Formeln:\n"
        "- **Isotopenverhältnis der verbleibenden Flüssigkeit:**\n"
        "  R_l = R_{l0} \cdot f^{\alpha - 1}\n"
        "- **Isotopenverhältnis des momentan verdampfenden Gases:**\n"
        "  R_v = α \cdot R_l = α \cdot R_{l0} \cdot f^{\alpha - 1}\n"
        "- **Mittleres Isotopenverhältnis des bereits verdampften Gases:**\n"
        "  \overline{R_v} = R_{l0} \cdot \frac{1 - f^{\alpha}}{1 - f}\n\n"
        "### Ergebnis:\n"
        "- Atmosphäre: leicht (niedrige δ¹⁸O).\n"
        "- Ozean/See: wird schwerer.\n\n"
        "### Bedeutung der Variablen:\n"
        "- R_{l0}: anfängliches Isotopenverhältnis der Flüssigkeit.\n"
        "- R_l: aktuelles Isotopenverhältnis der verbleibenden Flüssigkeit.\n"
        "- R_v: Isotopenverhältnis des aktuell verdampfenden Gases.\n"
        "- \overline{R_v}: mittleres Isotopenverhältnis des bereits verdampften Gases.\n"
        "- f: verbleibender Anteil der Flüssigkeit.\n"
        "- \alpha: Gleichgewichts-Fraktionierungsfaktor.\n\n"
        "👉 Hier entsteht oft eine Rayleigh-Fraktionierung."
    ),
    "Kondensation": (
        "# ☁️ 2. Kondensation (Condensation)\n\n"
        "### Prozess:\n"
        "Wasserdampf wird zu Wolken / Tropfen.\n\n"
        "### Effekt:\n"
        "- Schwere Isotope (^18O) kondensieren zuerst.\n"
        "- Regen wird zunehmend leichter, je weiter die Luftmasse zieht.\n\n"
        "### Formeln:\n"
        "- **Isotopenverhältnis der verbleibenden Gasphase:**\n"
        "  R_v = R_{v0} \cdot f^{\alpha-1}\n"
        "- **Isotopenverhältnis der aktuell kondensierenden Flüssigkeit:**\n"
        "  R_l = R_{v0} \cdot \alpha \cdot f^{\alpha-1}\n"
        "- **Mittleres Isotopenverhältnis der bereits kondensierten Flüssigkeit:**\n"
        "  \overline{R_l} = R_{v0} \cdot \frac{1 - f^{\alpha}}{1 - f}\n\n"
        "### Ergebnis:\n"
        "- frühe Niederschläge: relativ schwer.\n"
        "- spätere / weiter entfernte: sehr leicht.\n\n"
        "### Bedeutung der Variablen:\n"
        "- R_{v0}: anfängliches Isotopenverhältnis der Gasphase.\n"
        "- R_v: aktuelles Isotopenverhältnis der verbleibenden Gasphase.\n"
        "- R_l: Isotopenverhältnis der aktuell kondensierenden Flüssigkeit.\n"
        "- \overline{R_l}: mittleres Isotopenverhältnis der bereits kondensierten Flüssigkeit.\n"
        "- f: verbleibender Anteil der Gasphase.\n"
        "- \alpha: Gleichgewichts-Fraktionierungsfaktor.\n\n"
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
    "Daten-Upload": (
        "# 📤 7. δ¹⁸O Daten-Upload\n\n"
        "### Prozess:\n"
        "Lade eine CSV- oder Excel-Datei mit δ¹⁸O-Werten hoch.\n\n"
        "### Auswertung:\n"
        "- Die App erkennt mögliche δ¹⁸O-Spalten.\n"
        "- Du kannst die X-Achse wählen (Index, Probe oder Datum).\n"
        "- Ein Diagramm zeigt die Messwerte.\n\n"
        "### Ergebnis:\n"
        "- Plott der δ¹⁸O-Werte.\n"
        "- Statistische Zusammenfassung der Messwerte."
    ),
}

selected_station = st.radio("Station wählen", list(stations.keys()), index=0, horizontal=True)

st.subheader(selected_station)
if selected_station == "Daten-Upload":
    st.write(stations[selected_station])
    st.markdown(
        "Lade eine Datei mit δ¹⁸O-Werten hoch. Erlaubte Formate: CSV, XLSX, XLS."
    )
    isotope_file = st.file_uploader(
        "δ¹⁸O Datei hochladen", type=["csv", "xlsx", "xls"]
    )

    if isotope_file is not None:
        try:
            if isotope_file.name.lower().endswith((".xls", ".xlsx")):
                df = pd.read_excel(isotope_file)
            else:
                df = pd.read_csv(isotope_file)

            candidate_columns = [
                c
                for c in df.columns
                if c.lower().replace(" ", "").replace("_", "")
                in (
                    "d18o",
                    "delta18o",
                    "delta_18o",
                    "delta18",
                    "δ18o",
                    "d18",
                )
                and pd.api.types.is_numeric_dtype(df[c])
            ]
            if not candidate_columns:
                candidate_columns = [
                    c
                    for c in df.columns
                    if any(
                        key in c.lower()
                        for key in ["18o", "d18o", "delta", "δ18"]
                    )
                    and pd.api.types.is_numeric_dtype(df[c])
                ]
            if not candidate_columns:
                candidate_columns = [
                    c
                    for c in df.columns
                    if pd.api.types.is_numeric_dtype(df[c])
                ]

            if not candidate_columns:
                st.warning(
                    "In der Datei wurden keine numerischen Spalten gefunden. Bitte lade eine Datei mit δ¹⁸O-Werten hoch."
                )
            else:
                delta_col = st.selectbox(
                    "Wähle die δ¹⁸O-Spalte", candidate_columns, index=0
                )

                axis_columns = [
                    c
                    for c in df.columns
                    if c != delta_col
                    and (
                        pd.api.types.is_numeric_dtype(df[c])
                        or pd.api.types.is_datetime64_any_dtype(df[c])
                        or df[c].dtype == object
                    )
                ]
                x_axis_choice = st.selectbox(
                    "Wähle X-Achse", ["Index"] + axis_columns, index=0
                )

                if x_axis_choice == "Index":
                    x_values = np.arange(1, len(df) + 1)
                    x_label = "Probe"
                else:
                    x_values = df[x_axis_choice]
                    x_label = x_axis_choice

                y_values = pd.to_numeric(df[delta_col], errors="coerce")
                valid = ~y_values.isna()
                y_values = y_values[valid]
                x_values = x_values[valid]

                st.metric("Anzahl auswertbarer Werte", f"{len(y_values)}")
                st.write(
                    {
                        "Mittelwert (δ¹⁸O)": f"{y_values.mean():.2f} ‰",
                        "Median (δ¹⁸O)": f"{y_values.median():.2f} ‰",
                        "Minimum (δ¹⁸O)": f"{y_values.min():.2f} ‰",
                        "Maximum (δ¹⁸O)": f"{y_values.max():.2f} ‰",
                    }
                )

                fig_upload, ax_upload = plt.subplots(figsize=(6, 4))
                ax_upload.plot(x_values, y_values, marker="o", color="#1f77b4", linewidth=2)
                ax_upload.set_xlabel(x_label, color="black")
                ax_upload.set_ylabel("δ¹⁸O (‰)", color="black")
                ax_upload.set_title("Hochgeladene δ¹⁸O Werte", color="black")
                ax_upload.grid(alpha=0.3)
                ax_upload.tick_params(colors="black")
                st.pyplot(fig_upload)

                if x_axis_choice == "Index":
                    st.caption(
                        "Die Werte werden gegen die Probennummer aufgetragen."
                    )
                else:
                    st.caption(
                        "Die Werte werden gegen die gewählte X-Achse aufgetragen."
                    )
        except Exception as e:
            st.error(f"Fehler beim Einlesen der Datei: {e}")
    else:
        st.info(
            "Lade eine CSV- oder Excel-Datei hoch, die δ¹⁸O-Werte enthält."
        )
else:
    st.write(stations[selected_station])
    st.info("Klicke eine Station an, um den erklärenden Text dazu zu sehen.")

st.header("3. Schematische Darstellung: Wolken, Ozean, Land, Berge")
st.write("Erzeugt eine zweigeteilte Abbildung: oben ein schematisches Panel, unten ein δ¹⁸O vs. Höhe Plot (wie im Referenzbild).")

# GNIP data upload (optional)
st.markdown("**GNIP-Daten (optional):** Lade eine CSV aus der GNIP‑Datenbank hoch, um Niederschlags‑δ¹⁸O Werte zu verwenden.")
gnip_file = st.file_uploader("GNIP CSV hochladen (optional)", type=["csv"])  

# compute representative δ values: default from slider `delta0`, can be replaced by uploaded GNIP data
if gnip_file is not None:
    try:
        df = pd.read_csv(gnip_file)
        possible = [c for c in df.columns if c.lower() in ("d18o", "delta18o", "delta_18o", "d18oxy", "value", "d18")]
        if not possible:
            possible = [c for c in df.columns if any(s in c.lower() for s in ("18", "d")) and pd.api.types.is_numeric_dtype(df[c])]
        if possible:
            col = possible[0]
            rain_delta = float(df[col].dropna().astype(float).mean())
            sample_n = int(df[col].dropna().shape[0])
            st.success(f"GNIP-Daten gelesen — Mittelwert von '{col}': {rain_delta:.2f} ‰ (n={sample_n})")
        else:
            rain_delta = float(delta0)
            st.warning("Keine geeignete δ¹⁸O-Spalte in der CSV gefunden — verwende den gewählten Startwert.")
    except Exception as e:
        rain_delta = float(delta0)
        st.error(f"Fehler beim Einlesen der GNIP‑Datei: {e}")
else:
    rain_delta = float(delta0)

vapor_offset = st.slider("Angenommene Differenz: Dampf = Regen + offset (‰)", -1.0, 6.0, 3.0, step=0.1)
vapor_delta = rain_delta + float(vapor_offset)

st.markdown(
    f"""
    <div style="background-color: #ffe4f0; border: 2px solid #ff69b4; border-radius:8px; padding:12px;">
        <strong style="color:#000000">Default‑Schätzungen (automatisch berechnet)</strong>
        <ul style="color:#000000; margin-top:6px;">
            <li>Regen / Niederschlag: δ¹⁸O ≈ <strong>{rain_delta:.1f} ‰</strong></li>
            <li>Wasserdampf / Wolken: δ¹⁸O ≈ <strong>{vapor_delta:.1f} ‰</strong></li>
        </ul>
        <small style="color:#333333">Hinweis: Vereinfachte Visualisierung; GNIP oder fraktionierende Modelle liefern genauere Werte.</small>
    </div>
    """,
    unsafe_allow_html=True,
)

# Prepare reservoir labels (keep simple)
reservoirs = {
    "Ozean": {"delta": "~0 ‰", "text": "Ozean (Referenz)."},
    "Wolken": {"delta": f"~ {vapor_delta:.1f} ‰", "text": "Wolken / Wasserdampf."},
    "Landoberfläche": {"delta": f"~ {rain_delta:.1f} ‰", "text": "Oberflächenwasser."},
    "Gletscher / Berge": {"delta": "~ -15 ‰", "text": "Hohe Lagen: sehr negative δ¹⁸O-Werte."},
}

selected_res = st.radio("Reservoir wählen", list(reservoirs.keys()), index=0)

# Create two-panel figure: A = schematic, B = δ vs altitude
fig, (axA, axB) = plt.subplots(2, 1, figsize=(8, 10), gridspec_kw={"height_ratios": [2, 1]})

# --- Panel A: schematic ---
axA.axis("off")
axA.set_xlim(0, 100)
axA.set_ylim(0, 60)

# Ocean
ocean_w = 28
ocean_h = 14
ocean = plt.Rectangle((2, 2), ocean_w, ocean_h, facecolor="#4da6ff", edgecolor="k")
axA.add_patch(ocean)
axA.text(6, 9, f"Ozean\n{reservoirs['Ozean']['delta']}", color="white", weight="bold")

# Continent / land
land = plt.Rectangle((ocean_w + 6, 2), 34, 28, facecolor="#eaf7de", edgecolor="k")
axA.add_patch(land)

# Mountains (stylized)
mx0 = ocean_w + 14
mount_coords = [[mx0, 10], [mx0 + 12, 40], [mx0 + 24, 10], [mx0 + 36, 38], [mx0 + 50, 10]]
mountain = plt.Polygon(mount_coords, closed=True, facecolor="#bdbdbd", edgecolor="k")
axA.add_patch(mountain)
axA.text(mx0 + 30, 46, f"Gletscher / Berge\n{reservoirs['Gletscher / Berge']['delta']}", ha="center", weight="bold")

# Clouds (three, over ocean, land, mountains)
cloud_centers = [(12, 46), (40, 52), (70, 50)]
cloud_colors = ["#ffffff"] * 3
cloud_deltas = [vapor_delta + 1.0, vapor_delta, vapor_delta - 1.2]
for (cx, cy), dv in zip(cloud_centers, cloud_deltas):
    axA.add_patch(plt.Circle((cx - 3, cy), 4.0, facecolor="#f7f7f7", edgecolor="#666666"))
    axA.add_patch(plt.Circle((cx + 1, cy + 1.5), 5.0, facecolor="#f7f7f7", edgecolor="#666666"))
    axA.add_patch(plt.Circle((cx + 6, cy), 4.0, facecolor="#f7f7f7", edgecolor="#666666"))
    axA.text(cx + 1, cy + 7, f"δ¹⁸O: {dv:.1f} ‰", ha="center", weight="bold")

# Long arrows: evaporation (ocean -> clouds)
axA.annotate('', xy=(12, 42), xytext=(ocean_w + 1, ocean_h + 2), arrowprops=dict(arrowstyle='-|>', lw=2.4, color='#2b6ea3'))
axA.text(22, 34, 'Verdunstung', color='#2b6ea3')

# Condensation / precipitation arrows (clouds -> mountains / land)
axA.annotate('', xy=(mx0 + 18, 36), xytext=(40, 48), arrowprops=dict(arrowstyle='-|>', lw=2.4, color='#a33'))
axA.text(48, 44, 'Kondensation / Niederschlag', color='#a33')

# River / runoff from mountains to ocean
river_x = [mx0 + 40, mx0 + 18, ocean_w + 10]
river_y = [18, 14, 8]
axA.plot(river_x, river_y, color='#1f77b4', lw=2.5)
axA.text(mx0 + 28, 20, 'Abfluss', color='#003366')

# Colored markers along mountain slope (altitude points)
altitudes = [0, 1000, 2000, 3000, 4000, 5000]
# compute a decreasing δ profile from near sea level to high altitudes
delta_low = rain_delta
delta_high = -15.0
delta_profile = np.linspace(delta_low, delta_high, len(altitudes))
colors = ['#d62728', '#ff7f0e', '#ffbf00', '#2ca02c', '#98df8a', '#17becf']
mount_x_positions = [mx0 + 8, mx0 + 14, mx0 + 20, mx0 + 28, mx0 + 36, mx0 + 46]
mount_y_positions = [14, 18, 22, 28, 32, 36]
for x, y, dp, c in zip(mount_x_positions, mount_y_positions, delta_profile, colors):
    axA.scatter(x, y, s=120, color=c, edgecolor='k', zorder=5)
    axA.text(x + 3, y - 2, f"{dp:.1f} ‰", color='k')

# --- Panel B: δ vs Altitude ---
axB.set_xlabel('Altitude (m)')
axB.set_ylabel('δ¹⁸O (‰)')
axB.set_xlim(0, 5200)
axB.set_ylim(min(delta_profile) - 2, max(delta_profile) + 2)
axB.invert_yaxis()  # optional: show more negative downwards similar to many isotope plots
axB.plot(altitudes, delta_profile, color='#d95f02', lw=2)
for a, d, c in zip(altitudes, delta_profile, colors):
    axB.scatter(a, d, s=110, color=c, edgecolor='k')
    axB.text(a + 60, d, f"{d:.1f} ‰", va='center')
axB.set_title('δ¹⁸O vs. Altitude', weight='bold')
axB.grid(alpha=0.3)

st.pyplot(fig)

with st.expander('Details zum ausgewählten Reservoir'):
    st.subheader(selected_res)
    st.write(reservoirs[selected_res]['text'])

st.write('---')
st.write('Nutze diese Ansicht, um das Prinzip: Verdunstung → Kondensation → Niederschlag und Höhenabhängigkeit von δ¹⁸O zu veranschaulichen.')

st.header("4. Referenzabbildung: Schematische Nachbildung")
st.write("Nachbildung des hochgeladenen Referenzbilds: links ein schematisches Panel, rechts ein δ¹⁸O‑vs‑Höhe‑Diagramm.")

# Build reference-style figure similar to the uploaded image
fig4, (axL, axR) = plt.subplots(1, 2, figsize=(12, 5), gridspec_kw={"width_ratios": [1.2, 1]})

# Left: schematic (axL)
axL.axis('off')
axL.set_xlim(0, 100)
axL.set_ylim(0, 40)

# Ocean block
axL.add_patch(plt.Rectangle((0, 0), 24, 10, facecolor="#4da6ff", edgecolor='k'))
axL.text(4, 5, 'Ozean', color='white', weight='bold')

# Small evaporation arrows from ocean to left cloud
axL.annotate('', xy=(12, 24), xytext=(12, 12), arrowprops=dict(arrowstyle='-|>', color='#2b6ea3', lw=2))
axL.text(12, 21, 'Verdunstung', ha='center', color='#2b6ea3')

# Clouds
clouds = [(12, 28), (44, 32), (78, 34)]
cloud_labels = [f"δ¹⁸O: {vapor_delta + 1.0:.1f} ‰", f"δ¹⁸O: {vapor_delta:.1f} ‰", f"δ¹⁸O: {vapor_delta - 1.2:.1f} ‰"]
for (cx, cy), lab in zip(clouds, cloud_labels):
    axL.add_patch(plt.Circle((cx - 3, cy), 3.2, facecolor='#ffffff', edgecolor='#666666'))
    axL.add_patch(plt.Circle((cx, cy + 1.2), 3.8, facecolor='#ffffff', edgecolor='#666666'))
    axL.add_patch(plt.Circle((cx + 3, cy), 3.2, facecolor='#ffffff', edgecolor='#666666'))
    axL.text(cx + 1, cy + 5, lab, ha='center', weight='bold')

# Mountain slope with colored points
alts_ref = np.array([0, 1000, 2000, 3000, 4000])
d_ref = np.linspace(rain_delta, -14.0, alts_ref.size)
xs_ref = np.linspace(46, 92, alts_ref.size)
ys_ref = 6 + (alts_ref / 5000.0) * 28
colmap = plt.cm.viridis(np.linspace(0, 1, alts_ref.size))
for x, y, dv, cc in zip(xs_ref, ys_ref, d_ref, colmap):
    axL.scatter(x, y, s=140, color=cc, edgecolor='k')
    axL.text(x + 2, y - 1, f"{dv:.1f} ‰", color='k')

axL.text(4, 38, 'A', weight='bold')

# Right: δ vs altitude (axR) like panel B
axR.set_xlim(min(d_ref) - 2, max(d_ref) + 2)
axR.set_ylim(0, 5200)
axR.invert_yaxis()
axR.set_xlabel('δ¹⁸O (‰)')
axR.set_ylabel('Altitude (m)')
axR.set_title('δ¹⁸O vs. Höhe')
axR.plot(d_ref, alts_ref, color='#d62728', lw=2)
for dv, alt, cc in zip(d_ref, alts_ref, colmap):
    axR.scatter(dv, alt, color=cc, s=140, edgecolor='k')
    axR.text(dv + 0.4, alt, f"{dv:.1f} ‰", va='center')

axR.text(min(d_ref) - 1, -200, 'B', weight='bold')

st.pyplot(fig4)
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.header("📈 Interactive Rayleigh Fractionation")

st.write("""
Explore how the isotopic composition changes during Rayleigh fractionation.
Adjust the initial isotope value, the fractionation factor, and the remaining fraction.
""")

# -----------------------------
# Sidebar / Slider
# -----------------------------
delta0 = st.slider(
    "Initial δ18O value (‰)",
    min_value=-25.0,
    max_value=5.0,
    value=0.0,
    step=0.5
)

alpha = st.slider(
    "Fractionation factor α",
    min_value=1.000,
    max_value=1.020,
    value=1.009,
    step=0.001,
    format="%.3f"
)

f_current = st.slider(
    "Remaining fraction (f)",
    min_value=0.01,
    max_value=1.00,
    value=0.50,
    step=0.01
)

# -----------------------------
# Rayleigh calculation
# -----------------------------
f = np.linspace(0.01, 1, 200)

delta = (delta0 + 1000) * (f ** (alpha - 1)) - 1000

delta_current = (delta0 + 1000) * (f_current ** (alpha - 1)) - 1000

# -----------------------------
# Plot
# -----------------------------
fig, ax = plt.subplots(figsize=(8,5))

ax.plot(f, delta, linewidth=2, label="Rayleigh Curve")

ax.scatter(
    f_current,
    delta_current,
    color="red",
    s=80,
    label="Selected Point"
)

ax.set_xlabel("Remaining fraction (f)")
ax.set_ylabel("δ18O (‰)")
ax.set_title("Rayleigh Isotope Fractionation")

ax.grid(True)

ax.legend()

st.pyplot(fig)

# -----------------------------
# Display values
# -----------------------------
st.subheader("Current values")

col1, col2, col3 = st.columns(3)

col1.metric("Initial δ18O", f"{delta0:.2f} ‰")
col2.metric("Remaining fraction", f"{f_current:.2f}")
col3.metric("Calculated δ18O", f"{delta_current:.2f} ‰")

st.info(
"""
**Interpretation**

- When the remaining fraction (**f**) decreases, the remaining water becomes progressively isotopically enriched.
- The fractionation factor (**α**) controls how strongly the isotope composition changes.
- The red point represents the currently selected state.
"""
)
import streamlit as st

st.header("🌍 Interactive Hydrological Cycle")

st.write("Click on a reservoir to learn how isotope fractionation changes during the water cycle.")

# ------------------------------------
# Session State
# ------------------------------------

if "selected" not in st.session_state:
    st.session_state.selected = "Ocean"

# ------------------------------------
# Buttons
# ------------------------------------

col1, col2, col3 = st.columns([1,2,1])

with col2:

    if st.button("☁️ Atmosphere"):
        st.session_state.selected = "Atmosphere"

    if st.button("🌧 Precipitation"):
        st.session_state.selected = "Precipitation"

    if st.button("🏔 Infiltration"):
        st.session_state.selected = "Infiltration"

    if st.button("💧 Groundwater"):
        st.session_state.selected = "Groundwater"

    if st.button("🏞 Runoff"):
        st.session_state.selected = "Runoff"

    if st.button("🌊 Ocean"):
        st.session_state.selected = "Ocean"

    if st.button("☀️ Evaporation"):
        st.session_state.selected = "Evaporation"

# ------------------------------------
# Information
# ------------------------------------

st.divider()

reservoir = st.session_state.selected

if reservoir == "Ocean":

    st.subheader("🌊 Ocean")

    st.write("""
The ocean is the largest water reservoir on Earth.

Typical isotope composition:

- δ18O ≈ 0 ‰ (SMOW)
- Source for evaporation
- Heavy isotopes remain preferentially in the liquid
""")

elif reservoir == "Evaporation":

    st.subheader("☀️ Evaporation")

    st.write("""
During evaporation the lighter isotope (16O) enters the vapor phase more easily.

The remaining ocean water becomes relatively enriched in 18O.
""")

elif reservoir == "Atmosphere":

    st.subheader("☁️ Atmosphere")

    st.write("""
Water vapor is depleted in heavy isotopes compared to seawater.

Its isotope composition changes during transport.
""")

elif reservoir == "Precipitation":

    st.subheader("🌧 Precipitation")

    st.write("""
Rain removes heavy isotopes first.

Remaining vapor becomes progressively depleted following Rayleigh fractionation.
""")

elif reservoir == "Infiltration":

    st.subheader("🏔 Infiltration")

    st.write("""
Rainwater infiltrates into the soil.

The isotope signal is often preserved in groundwater.
""")

elif reservoir == "Groundwater":

    st.subheader("💧 Groundwater")

    st.write("""
Groundwater stores the isotopic signature of recharge.

These data are widely used in hydrogeology.
""")

elif reservoir == "Runoff":

    st.subheader("🏞 Runoff")

    st.write("""
Surface runoff transports water back into rivers and finally the ocean.

Depending on climate, isotope values may vary seasonally.
""")
with st.expander("📐 Show Rayleigh equations"):
    st.latex(r"R_l = R_{l0}f^{\alpha-1}")
    st.latex(r"R_v = \alpha R_{l0}f^{\alpha-1}")