import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# CONFIG
st.set_page_config(page_title="Dashboard Panen Rempah", layout="wide")

# ======================
# STYLE (BIAR COMPACT)
# ======================
st.markdown("""
<style>
.block-container {
    padding-top: 1rem;
    padding-bottom: 0rem;
}
</style>
""", unsafe_allow_html=True)

# ======================
# DUMMY DATABASE
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
with st.container():
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
# DATA
# ======================
produksi = data_db[program][tahun][produk]

total_panen = sum(produksi)
anggaran = total_panen * 15000
luas_lahan = total_panen / 20
produktivitas = total_panen / luas_lahan

# ======================
# KPI (1 BARIS)
# ======================
with st.container():
    k1, k2, k3, k4 = st.columns(4)

    k1.metric("Anggaran", f"Rp {anggaran:,.0f}")
    k2.metric("Total Panen", f"{total_panen} Kg")
    k3.metric("Luas Lahan", f"{luas_lahan:.1f} Ha")
    k4.metric("Produktivitas", f"{produktivitas:.1f} Kg/Ha")

# ======================
# ROW 1 (TABLE + PIE)
# ======================
with st.container():
    c1, c2 = st.columns([2,1])

    # TABLE
    with c1:
        wilayah_df = pd.DataFrame({
            "Wilayah": ["Desa A","Desa B","Desa C","Desa D"],
            "Hasil (Kg)": [total_panen*0.3, total_panen*0.25, total_panen*0.2, total_panen*0.25],
            "Petani": [120,95,80,60]
        })
        st.dataframe(wilayah_df, height=250, use_container_width=True)

    # PIE
    with c2:
        pie_df = pd.DataFrame({
            "Produk": ["Padi","Kokoa","Jagung"],
            "Nilai": [
                sum(data_db[program][tahun]["Padi"]),
                sum(data_db[program][tahun]["Kokoa"]),
                sum(data_db[program][tahun]["Jagung"])
            ]
        })

        fig, ax = plt.subplots(figsize=(4,4))
        ax.pie(pie_df["Nilai"], labels=pie_df["Produk"], autopct='%1.1f%%')
        ax.set_title("Komposisi")

        st.pyplot(fig)

# ======================
# ROW 2 (SEMUA CHART SEJAJAR)
# ======================
with st.container():
    c1, c2, c3 = st.columns(3)

    # PRODUKSI BULANAN
    with c1:
        df = pd.DataFrame({
            "Bulan": bulan,
            "Produksi": produksi
        })
        st.subheader("Produksi Bulanan")
        st.bar_chart(df.set_index("Bulan"), height=250)

    # PERBANDINGAN PRODUK
    with c2:
        compare_df = pd.DataFrame({
            "Produk": ["Padi","Kokoa","Jagung"],
            "Total": [
                sum(data_db[program][tahun]["Padi"]),
                sum(data_db[program][tahun]["Kokoa"]),
                sum(data_db[program][tahun]["Jagung"])
            ]
        })
        st.subheader("Perbandingan Produk")
        st.bar_chart(compare_df.set_index("Produk"), height=250)

    # EFISIENSI
    with c3:
        efisiensi_df = pd.DataFrame({
            "Produk": ["Padi","Kokoa","Jagung"],
            "Efisiensi": [20,15,12]
        })
        st.subheader("Efisiensi")
        st.bar_chart(efisiensi_df.set_index("Produk"), height=250)
