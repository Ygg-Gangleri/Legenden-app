# 🎈 Blank app template

A simple Streamlit app template for you to modify!

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://blank-app-template.streamlit.app/)

### How to run it on your own machine

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run streamlit_app.py
   ```
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("🧪 Isotopen-Rayleigh-Fraktionierung")

st.write("""
Die Rayleigh-Fraktionierung beschreibt, wie sich die Isotopenzusammensetzung
eines Reservoirs verändert, wenn kontinuierlich Material entfernt wird.
""")

# Eingaben
delta0 = st.slider("Anfangswert δ₀ (‰)", -20.0, 20.0, -10.0)
alpha = st.slider("Fraktionierungsfaktor α", 1.000, 1.020, 1.005)

# Rechnung
f = np.linspace(0.01, 1.0, 200)
delta = (delta0 + 1000) * f**(alpha - 1) - 1000

# Plot
fig, ax = plt.subplots()
ax.plot(f, delta)
ax.set_xlabel("Verbleibender Anteil f")
ax.set_ylabel("δ (‰)")
ax.set_title("Rayleigh-Fraktionierung")

st.pyplot(fig)

# Aktueller Wert
f_wert = st.slider("Aktueller Zustand f", 0.01, 1.0, 0.5)
delta_now = (delta0 + 1000) * f_wert**(alpha - 1) - 1000

st.info(f"Aktueller δ-Wert: {delta_now:.2f} ‰")
