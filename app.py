import streamlit as st
import numpy as np
import math
import matplotlib.pyplot as plt

st.set_page_config(page_title="CNT Explorer 2.0", layout="wide")

st.title("🧬 CNT Explorer 2.0 — Advanced Nano Device Visualizer")
st.write("A fully interactive learning simulator for **Carbon Nanotubes**, built only with physics — no datasets or ML models.")

# =========================
# SIDEBAR INPUTS
# =========================
st.sidebar.header("CNT Design Inputs")

n = st.sidebar.number_input("Chirality n", min_value=1, max_value=200, value=12)
m = st.sidebar.number_input("Chirality m", min_value=0, max_value=200, value=6)

a = 0.246  # nm lattice constant

diameter = (a / math.pi) * math.sqrt(n**2 + n*m + m**2)
metallic = ((n - m) % 3 == 0)
bandgap = 0 if metallic else 0.7 / diameter

st.subheader("📌 CNT Structure Summary")
c1, c2, c3 = st.columns(3)
c1.metric("Diameter (nm)", round(diameter, 4))
c2.metric("Type", "Metallic" if metallic else "Semiconducting")
c3.metric("Bandgap (eV)", round(bandgap, 4))

st.markdown("---")

# =========================
# BAND STRUCTURE
# =========================
st.subheader("📈 Band Structure Approximation")

k = np.linspace(-3, 3, 400)
if metallic:
    E = 0.2 * k
else:
    E = np.sqrt((bandgap/2)**2 + (0.25 * k**2))

fig1, ax1 = plt.subplots()
ax1.plot(k, E)
ax1.plot(k, -E)
ax1.set_xlabel("k (a.u.)")
ax1.set_ylabel("Energy (eV)")
ax1.set_title("CNT Band Structure (Simplified)")
st.pyplot(fig1)

st.markdown("---")

# =========================
# CNT-FET SIMULATOR
# =========================
st.subheader("⚡ CNT-FET Current Estimator (Ballistic Approximation)")

Vg = st.slider("Gate Voltage (V)", 0.0, 2.0, 1.0, 0.1)
Vd = st.slider("Drain Voltage (V)", 0.0, 2.0, 1.0, 0.1)

beta = 10e-6
Vt = bandgap / 2
Id = max(0, beta * (Vg - Vt) * Vd)

st.write(f"**Estimated Drain Current:** {Id:.6f} A")

st.markdown("---")

# =========================
# HEAT MAP — CHIRALITY VS BANDGAP
# =========================
st.subheader("🌈 Chirality Explorer (n,m → Bandgap Map)")

size = st.slider("Grid Size", 10, 40, 20)

grid = np.zeros((size, size))
for i in range(size):
    for j in range(size):
        d = (a / math.pi) * math.sqrt(i**2 + i*j + j**2) if (i + j) > 0 else 0.0001
        if ((i - j) % 3) == 0:
            grid[i, j] = 0
        else:
            grid[i, j] = 0.7 / d

fig2, ax2 = plt.subplots()
cax = ax2.imshow(grid, origin="lower")
ax2.set_title("Bandgap Heatmap (n vs m)")
ax2.set_xlabel("m")
ax2.set_ylabel("n")
fig2.colorbar(cax, label="Bandgap (eV)")
st.pyplot(fig2)

st.markdown("---")

# =========================
# CNT INTERCONNECT RESISTANCE
# =========================
st.subheader("🔌 CNT Interconnect Resistance Estimator")

length_um = st.slider("Length (µm)", 0.1, 20.0, 5.0)
rho = 1e-6  # approx resistivity (ohm·cm)
length_cm = length_um * 1e-4
R = rho * (length_cm / (diameter * 1e-7))

st.write(f"**Estimated Resistance:** {R:.2f} Ω")

st.markdown("---")

# =========================
# CNT VS SILICON MOSFET
# =========================
st.subheader("📊 CNT-FET vs Silicon MOSFET (Qualitative)")

V = np.linspace(0, 2, 50)
Id_cnt = beta * (V - Vt)
Id_cnt[Id_cnt < 0] = 0

mu = 200e-4
Cox = 1e-3
WoverL = 10
Id_si = mu * Cox * WoverL * (V**2)

fig3, ax3 = plt.subplots()
ax3.plot(V, Id_cnt, label="CNT-FET")
ax3.plot(V, Id_si, label="Silicon MOSFET")
ax3.set_xlabel("Gate Voltage (V)")
ax3.set_ylabel("Drain Current (A)")
ax3.legend()
ax3.set_title("Comparison (Conceptual)")
st.pyplot(fig3)

st.markdown("---")

# =========================
# SYNTHESIS RULE ENGINE
# =========================
st.subheader("🧪 Synthesis Recommendation (Rule-Based)")

if diameter < 1:
    st.info("🔬 Prefer **Laser Ablation / Arc Discharge** — smaller diameter SWCNTs.")
elif diameter < 2:
    st.info("⚗️ Prefer **CVD / PECVD** for alignment + chirality tuning.")
else:
    st.info("🧵 Prefer **Fiber / MWCNT growth techniques** for mechanical stability.")

st.markdown("---")

st.subheader("📚 Learning Notes")

with st.expander("Chirality & Electronic Type"):
    st.write("""(n,m) defines whether CNT behaves as **metal** or **semiconductor**.
If (n − m) mod 3 = 0 → Metallic, else → Semiconducting.""")

with st.expander("Ballistic Transport"):
    st.write("Electrons move with minimal scattering, enabling ultra-high current densities.")

with st.expander("Why CNT Interconnects matter"):
    st.write("CNTs can replace copper due to lower electromigration and high current capacity.")
