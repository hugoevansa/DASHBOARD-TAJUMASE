import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard Panen Rempah", layout="wide")

# ======================
# STYLE COMPACT + CARD
# ======================
st.markdown("""
<style>
.block-container {
    padding-top: 1rem;
    padding-bottom: 0rem;
}
div[data-testid="stMetric"] {
    background-color: #f9fafb;
    padding: 10px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ======================
# DATA
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
# ROW CHART (SERAGAM)
# ======================
c1, c2, c3 = st.columns(3)

# ===== 1. PRODUKSI =====
with c1:
    st.subheader("Produksi Bulanan")

    df = pd.DataFrame({
        "Bulan": bulan,
        "Produksi": produksi
    })

    st.bar_chart(df.set_index("Bulan"), height=220)

# ===== 2. PIE =====
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

    fig, ax = plt.subplots(figsize=(3,3))  # kecil & kotak
    ax.pie(pie_df["Nilai"], labels=pie_df["Produk"], autopct='%1.1f%%')
    ax.set_aspect('equal')

    st.pyplot(fig)

# ===== 3. PERBANDINGAN =====
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

    st.bar_chart(compare_df.set_index("Produk"), height=220)

# ======================
# WILAYAH (PINDAH KE BAWAH FULL WIDTH)
# ======================
st.subheader("Distribusi Wilayah Desa")

wilayah_df = pd.DataFrame({
    "Wilayah": ["Desa A","Desa B","Desa C","Desa D"],
    "Hasil (Kg)": [total_panen*0.3, total_panen*0.25, total_panen*0.2, total_panen*0.25],
    "Petani": [120,95,80,60]
})

st.dataframe(wilayah_df, height=200, use_container_width=True)
