import streamlit as st
import pandas as pd
import plotly.express as px

# CONFIG
st.set_page_config(page_title="Dashboard Panen Rempah", layout="wide")

# ======================
# 🎨 SAGE THEME STYLE
# ======================
st.markdown("""
<style>

/* BACKGROUND */
.stApp {
    background: linear-gradient(135deg, #aba784, #636b54);
}

/* CONTAINER */
.block-container {
    padding-top: 1rem;
    padding-bottom: 0rem;
}

/* KPI CARD */
div[data-testid="stMetric"] {
    background-color: #ffffff;
    padding: 16px;
    border-radius: 14px;
    border-left: 6px solid #8da98d;
    box-shadow: 0 4px 12px rgba(0,0,0,0.04);
}

/* TITLE */
h1 {
    color: #5f7a61;
}

/* SUBTITLE */
h2, h3 {
    color: #6b8f71;
}

/* DATAFRAME */
[data-testid="stDataFrame"] {
    background-color: white;
    border-radius: 12px;
}

/* SELECTBOX */
div[data-baseweb="select"] {
    background-color: white;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ======================
# DATA DUMMY
# ======================
data_db = {
    "LEMBATA": {
        "2026": {
            "Padi": [120,150,180,200,210,220,230,240,250,260,270,300],
            "Kokoa": [80,90,100,120,130,140,150,155,160,170,180,200],
            "Jagung": [60,70,80,100,110,120,130,135,140,150,160,180],
        }
    },
    "RUTENG": {
        "2026": {
            "Padi": [90,110,130,150,160,170,180,190,200,210,220,240],
            "Kokoa": [60,70,80,90,100,110,120,125,130,140,150,170],
            "Jagung": [40,50,60,70,80,90,100,105,110,120,130,140],
        }
    }
}

bulan = ["Jan","Feb","Mar","Apr","Mei","Jun","Jul","Agu","Sep","Okt","Nov","Des"]

# ======================
# HEADER
# ======================
col1, col2, col3, col4 = st.columns([2,1,1,1])

with col1:
    st.title("🌾 Dashboard Panen Rempah")

with col2:
    program = st.selectbox("Program", list(data_db.keys()))

with col3:
    tahun = st.selectbox("Tahun", list(data_db[program].keys()))

with col4:
    produk = st.selectbox("Produk", list(data_db[program][tahun].keys()))

# ======================
# HITUNGAN
# ======================
produksi = data_db[program][tahun][produk]
total_panen = sum(produksi)
anggaran = total_panen * 15000
luas_lahan = total_panen / 20
produktivitas = total_panen / luas_lahan

# ======================
# KPI
# ======================
k1, k2, k3, k4 = st.columns(4)

k1.metric("Anggaran", f"Rp {anggaran:,.0f}")
k2.metric("Total Panen", f"{total_panen} Kg")
k3.metric("Luas Lahan", f"{luas_lahan:.1f} Ha")
k4.metric("Produktivitas", f"{produktivitas:.1f} Kg/Ha")

# ======================
# CHART ROW
# ======================
c1, c2, c3 = st.columns(3)

# ===== BAR PRODUKSI =====
with c1:
    st.subheader("Produksi Bulanan")

    df = pd.DataFrame({
        "Bulan": bulan,
        "Produksi": produksi
    })

    fig_bar = px.bar(
        df,
        x="Bulan",
        y="Produksi",
        color_discrete_sequence=["#8da98d"]
    )

    fig_bar.update_layout(
        height=260,
        margin=dict(t=30, b=0),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

    st.plotly_chart(fig_bar, use_container_width=True)

# ===== PIE =====
with c2:
    st.subheader("Komposisi Produk")

    pie_df = pd.DataFrame({
        "Produk": ["Padi","Kokoa","Jagung"],
        "Nilai": [
            sum(data_db[program][tahun]["Padi"]),
            sum(data_db[program][tahun]["Kokoa"]),
            sum(data_db[program][tahun]["Jagung"])
        ]
    })

    fig_pie = px.pie(
        pie_df,
        names="Produk",
        values="Nilai",
        hole=0.5,
        color_discrete_sequence=["#8da98d", "#a3b8a3", "#c7d9c7"]
    )

    fig_pie.update_layout(
        height=260,
        margin=dict(t=30, b=0),
        paper_bgcolor='rgba(0,0,0,0)'
    )

    st.plotly_chart(fig_pie, use_container_width=True)

# ===== PERBANDINGAN =====
with c3:
    st.subheader("Perbandingan Produk")

    compare_df = pd.DataFrame({
        "Produk": ["Padi","Kokoa","Jagung"],
        "Total": [
            sum(data_db[program][tahun]["Padi"]),
            sum(data_db[program][tahun]["Kokoa"]),
            sum(data_db[program][tahun]["Jagung"])
        ]
    })

    fig_compare = px.bar(
        compare_df,
        x="Produk",
        y="Total",
        color="Produk",
        color_discrete_sequence=["#8da98d", "#a3b8a3", "#c7d9c7"]
    )

    fig_compare.update_layout(
        height=260,
        margin=dict(t=30, b=0),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )

    st.plotly_chart(fig_compare, use_container_width=True)

# ======================
# WILAYAH
# ======================
st.subheader("Distribusi Wilayah Desa")

wilayah_df = pd.DataFrame({
    "Wilayah": ["Desa A","Desa B","Desa C","Desa D"],
    "Hasil (Kg)": [total_panen*0.3, total_panen*0.25, total_panen*0.2, total_panen*0.25],
    "Petani": [120,95,80,60]
})

st.dataframe(wilayah_df, height=220, use_container_width=True)
