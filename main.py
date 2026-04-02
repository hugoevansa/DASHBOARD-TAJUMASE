import streamlit as st
import pandas as pd
import plotly.express as px

# CONFIG
st.set_page_config(page_title="Dashboard Panen Rempah", layout="wide")

# ======================
# 🎨 SAGE THEME STYLE (AMBIL DARI KODINGAN 1)
# ======================
st.markdown("""
<style>

/* BACKGROUND */
.stApp {
    background: linear-gradient(135deg, #e6efe9, #f4f7f5);
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
# LOAD DATA (LOGIC KODINGAN 2)
# ======================
df = pd.read_excel("data_panen_dummy.xlsx")

# ======================
# HEADER + FILTER
# ======================
col1, col2, col3, col4 = st.columns([2,1,1,1])

with col1:
    st.title("🌾 Dashboard Panen Rempah")

# FILTER Wilayah
with col2:
    Wilayah = st.selectbox("Wilayah", df["Wilayah"].dropna().unique())

df_filtered = df[df["Wilayah"] == Wilayah]

# FILTER TAHUN
with col3:
    tahun = st.selectbox("Tahun", sorted(df_filtered["Tahun"].dropna().unique()))

df_filtered = df_filtered[df_filtered["Tahun"] == tahun]

# FILTER Komoditas
with col4:
    Komoditas = st.selectbox("Komoditas", df_filtered["Komoditas"].dropna().unique())

df_filtered = df_filtered[df_filtered["Komoditas"] == Komoditas]

# ======================
# HANDLE DATA KOSONG
# ======================
if df_filtered.empty:
    st.warning("Data tidak tersedia untuk filter ini")
    st.stop()

# ======================
# KPI
# ======================
total_panen = df_filtered["Produksi"].sum()
anggaran = total_panen * 15000
luas_lahan = df_filtered["Luas_Lahan"].sum()

Produktivitas = total_panen / luas_lahan if luas_lahan != 0 else 0

k1, k2, k3, k4 = st.columns(4)

k1.metric("Anggaran", f"Rp {anggaran:,.0f}")
k2.metric("Total Panen", f"{total_panen:,.0f} Kg")
k3.metric("Luas Lahan", f"{luas_lahan:.1f} Ha")
k4.metric("Produktivitas", f"{Produktivitas:.1f} Kg/Ha")

# ======================
# CHART ROW
# ======================
c1, c2, c3 = st.columns(3)

# ===== BAR BULANAN =====
with c1:
    st.subheader("Komoditas Bulanan")

    bulanan = df_filtered.groupby("Bulan", as_index=False)["Komoditas"].sum()

    fig_bar = px.bar(
        bulanan,
        x="Bulan",
        y="Komoditas",
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
    st.subheader("Komposisi Komoditas")

    pie_df = df.groupby("Komoditas", as_index=False)["Komoditas"].sum()

    fig_pie = px.pie(
        pie_df,
        names="Komoditas",
        values="Komoditas",
        hole=0.5,
        color_discrete_sequence=["#8da98d","#a3b8a3","#c7d9c7"]
    )

    fig_pie.update_layout(
        height=260,
        margin=dict(t=30, b=0),
        paper_bgcolor='rgba(0,0,0,0)'
    )

    st.plotly_chart(fig_pie, use_container_width=True)

# ===== PERBANDINGAN =====
with c3:
    st.subheader("Perbandingan Komoditas")

    compare_df = df.groupby("Komoditas", as_index=False)["Komoditas"].sum()

    fig_compare = px.bar(
        compare_df,
        x="Komoditas",
        y="Komoditas",
        color="Komoditas",
        color_discrete_sequence=["#8da98d","#a3b8a3","#c7d9c7"]
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

wilayah_df = df_filtered.groupby("Wilayah", as_index=False).agg({
    "Komoditas":"sum",
    "Petani":"sum",
    "Luas_Lahan":"sum"
})

st.dataframe(wilayah_df, height=220, use_container_width=True)
