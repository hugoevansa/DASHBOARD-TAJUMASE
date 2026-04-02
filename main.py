import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# CONFIG
st.set_page_config(page_title="Dashboard Panen Rempah", layout="wide")

# ======================
# HEADER FILTER
# ======================
st.title("Dashboard Program Panen Rempah 🌾")

col1, col2, col3 = st.columns(3)

with col1:
    program = st.selectbox("Program", ["LEMBATA", "RUTENG"])

with col2:
    tahun = st.selectbox("Tahun", ["2026", "2025", "2024"])

with col3:
    produk = st.selectbox("Produk", ["Padi", "Kokoa", "Jagung"])

st.divider()

# ======================
# KPI CARDS
# ======================
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpi1.metric("Anggaran Dikeluarkan", "Rp. 301.242.589")
kpi2.metric("Total Panen", "2045 Kg")
kpi3.metric("Luas Lahan", "120 Ha")
kpi4.metric("Produktivitas", "17 Kg/Ha")

st.divider()

# ======================
# TABLE + PIE CHART
# ======================
left, right = st.columns([2,1])

# Data panen per wilayah / metode
data = pd.DataFrame({
    "Wilayah": ["Desa A", "Desa B", "Desa C", "Desa D"],
    "Hasil Panen (Kg)": [800, 500, 400, 345],
    "Petani Terlibat": [120, 95, 80, 60],
    "Luas Lahan (Ha)": [40, 30, 25, 25],
    "Produktivitas (Kg/Ha)": [20, 16.6, 16, 13.8]
})

with left:
    st.subheader(f"Distribusi Panen - {program}")
    st.dataframe(data, use_container_width=True)

# PIE CHART (komposisi produk)
with right:
    st.subheader("Proporsi Jenis Panen")

    pie_data = pd.DataFrame({
        "Jenis": ["Padi", "Kokoa", "Jagung"],
        "Persentase": [50, 30, 20]
    })

    fig, ax = plt.subplots()
    ax.pie(
        pie_data["Persentase"],
        labels=pie_data["Jenis"],
        autopct='%1.1f%%'
    )
    ax.set_ylabel("")

    st.pyplot(fig)

st.divider()

# ======================
# LINE CHARTS
# ======================
st.subheader("Tren Produksi Panen")

dates = pd.date_range(start="2024-01-01", periods=100)

def generate_series(base):
    return base + np.random.randn(100) * base * 0.05

chart1, chart2, chart3, chart4 = st.columns(4)

with chart1:
    st.caption("Produksi Panen (Kg)")
    df = pd.DataFrame({
        "Tanggal": dates,
        "LEMBATA": generate_series(2000),
        "RUTENG": generate_series(1500)
    })
    st.line_chart(df.set_index("Tanggal"))

with chart2:
    st.caption("Jumlah Petani")
    df = pd.DataFrame({
        "Tanggal": dates,
        "LEMBATA": generate_series(120),
        "RUTENG": generate_series(90)
    })
    st.line_chart(df.set_index("Tanggal"))

with chart3:
    st.caption("Luas Lahan (Ha)")
    df = pd.DataFrame({
        "Tanggal": dates,
        "LEMBATA": generate_series(100),
        "RUTENG": generate_series(80)
    })
    st.line_chart(df.set_index("Tanggal"))

with chart4:
    st.caption("Produktivitas (Kg/Ha)")
    df = pd.DataFrame({
        "Tanggal": dates,
        "LEMBATA": generate_series(18),
        "RUTENG": generate_series(15)
    })
    st.line_chart(df.set_index("Tanggal"))
