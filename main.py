import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# CONFIG
st.set_page_config(page_title="Dashboard Panen Rempah", layout="wide")

# ======================
# DUMMY DATABASE
# ======================
data_db = {
    "LEMBATA": {
        "2026": {
            "Padi": [120, 150, 180, 200, 210, 220, 230, 240, 250, 260, 270, 300],
            "Kokoa": [80, 90, 100, 120, 130, 140, 150, 155, 160, 170, 180, 200],
            "Jagung": [60, 70, 80, 100, 110, 120, 130, 135, 140, 150, 160, 180],
        },
        "2025": {
            "Padi": [100,120,140,160,170,180,190,200,210,220,230,250],
            "Kokoa": [70,80,90,100,110,120,130,135,140,150,160,180],
            "Jagung": [50,60,70,80,90,100,110,115,120,130,140,150],
        }
    },
    "RUTENG": {
        "2026": {
            "Padi": [90,110,130,150,160,170,180,190,200,210,220,240],
            "Kokoa": [60,70,80,90,100,110,120,125,130,140,150,170],
            "Jagung": [40,50,60,70,80,90,100,105,110,120,130,140],
        },
        "2025": {
            "Padi": [80,100,120,140,150,160,170,180,190,200,210,230],
            "Kokoa": [50,60,70,80,90,100,110,115,120,130,140,160],
            "Jagung": [30,40,50,60,70,80,90,95,100,110,120,130],
        }
    }
}

bulan = ["Jan","Feb","Mar","Apr","Mei","Jun","Jul","Agu","Sep","Okt","Nov","Des"]

# ======================
# HEADER
# ======================
st.title("Dashboard Program Panen Rempah 🌾")

col1, col2, col3 = st.columns(3)

with col1:
    program = st.selectbox("Program", list(data_db.keys()))

with col2:
    tahun = st.selectbox("Tahun", list(data_db[program].keys()))

with col3:
    produk = st.selectbox("Produk", list(data_db[program][tahun].keys()))

st.divider()

# ======================
# DATA AKTIF
# ======================
produksi = data_db[program][tahun][produk]

total_panen = sum(produksi)
anggaran = total_panen * 15000  # dummy harga per kg
luas_lahan = total_panen / 20   # asumsi produktivitas
produktivitas = total_panen / luas_lahan

# ======================
# KPI
# ======================
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpi1.metric("Anggaran Dikeluarkan", f"Rp {anggaran:,.0f}")
kpi2.metric("Total Panen", f"{total_panen} Kg")
kpi3.metric("Luas Lahan", f"{luas_lahan:.1f} Ha")
kpi4.metric("Produktivitas", f"{produktivitas:.1f} Kg/Ha")

st.divider()

# ======================
# TABLE + PIE
# ======================
left, right = st.columns([2,1])

# tabel wilayah dummy
wilayah_df = pd.DataFrame({
    "Wilayah": ["Desa A", "Desa B", "Desa C", "Desa D"],
    "Hasil (Kg)": [total_panen*0.3, total_panen*0.25, total_panen*0.2, total_panen*0.25],
    "Petani": [120, 95, 80, 60]
})

with left:
    st.subheader("Distribusi Wilayah")
    st.dataframe(wilayah_df, use_container_width=True)

# pie produk
with right:
    st.subheader("Komposisi Produk")

    pie_df = pd.DataFrame({
        "Produk": ["Padi","Kokoa","Jagung"],
        "Nilai": [
            sum(data_db[program][tahun]["Padi"]),
            sum(data_db[program][tahun]["Kokoa"]),
            sum(data_db[program][tahun]["Jagung"])
        ]
    })

    fig, ax = plt.subplots()
    ax.pie(pie_df["Nilai"], labels=pie_df["Produk"], autopct='%1.1f%%')
    st.pyplot(fig)

st.divider()

# ======================
# CHART UTAMA (DIGANTI)
# ======================
st.subheader("Produksi Bulanan (Kg)")

df_chart = pd.DataFrame({
    "Bulan": bulan,
    produk: produksi
})

st.bar_chart(df_chart.set_index("Bulan"))

# ======================
# CHART TAMBAHAN
# ======================
c1, c2 = st.columns(2)

# perbandingan produk
with c1:
    st.subheader("Perbandingan Antar Produk")

    compare_df = pd.DataFrame({
        "Produk": ["Padi","Kokoa","Jagung"],
        "Total": [
            sum(data_db[program][tahun]["Padi"]),
            sum(data_db[program][tahun]["Kokoa"]),
            sum(data_db[program][tahun]["Jagung"])
        ]
    })

    st.bar_chart(compare_df.set_index("Produk"))

# efisiensi
with c2:
    st.subheader("Efisiensi Produksi (Kg/Ha)")

    efisiensi_df = pd.DataFrame({
        "Produk": ["Padi","Kokoa","Jagung"],
        "Efisiensi": [20, 15, 12]
    })

    st.bar_chart(efisiensi_df.set_index("Produk"))
