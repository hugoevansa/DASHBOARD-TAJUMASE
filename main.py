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
# LOAD DATA
# ======================
df = pd.read_excel("data_panen_dummy.xlsx")

# ======================
# HEADER + FILTER
# ======================
col1, col2, col3, col4 = st.columns([2,1,1,1])

with col1:
    st.title("🌾 Dashboard Panen Rempah")

# ======================
# FILTER PROGRAM (MAIN FILTER)
# ======================
with col2:
    program_list = ["Semua Program"] + list(df["Program"].dropna().unique())
    program = st.selectbox("Program", program_list)

if program != "Semua Program":
    df_filtered = df[df["Program"] == program]
else:
    df_filtered = df.copy()

# ======================
# FILTER TAHUN
# ======================
with col3:
    tahun = st.selectbox("Tahun", sorted(df_filtered["Tahun"].dropna().unique()))

df_filtered = df_filtered[df_filtered["Tahun"] == tahun]

# ======================
# SIMPAN DATA UNTUK PERBANDINGAN (PENTING)
# ======================
df_compare = df_filtered.copy()

# ======================
# FILTER PRODUK
# ======================
with col4:
    produk_list = ["Semua Produk"] + list(df_filtered["Produk"].dropna().unique())
    produk = st.selectbox("Produk", produk_list)

if produk != "Semua Produk":
    df_filtered = df_filtered[df_filtered["Produk"] == produk]

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
anggaran = df_filtered["Anggaran"].sum()
luas_lahan = df_filtered["Luas_Lahan"].sum()
produktivitas = total_panen / luas_lahan if luas_lahan != 0 else 0

k1, k2, k3, k4 = st.columns(4)

k1.metric("Anggaran", f"Rp {anggaran:,.0f}")
k2.metric("Total Panen", f"{total_panen:,.0f} Kg")
k3.metric("Luas Lahan", f"{luas_lahan:.1f} Ha")
k4.metric("Produktivitas", f"{produktivitas:.1f} Kg/Ha")

# ======================
# CHART ROW
# ======================
c1, c2, c3 = st.columns(3)

# ===== BAR BULANAN (ikut produk) =====
with c1:
    st.subheader("Produksi Bulanan")

    bulanan = df_filtered.groupby("Bulan", as_index=False)["Produksi"].sum()

    fig_bar = px.bar(
        bulanan,
        x="Bulan",
        y="Produksi",
        color_discrete_sequence=["#8da98d"]
    )

    fig_bar.update_layout(
        height=260,
        margin=dict(t=30, b=0),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        hovermode="x unified"
    )

    st.plotly_chart(fig_bar, use_container_width=True)

# ===== PIE (tidak ikut filter produk) =====
with c2:
    st.subheader("Komposisi Produk")

    pie_df = df_compare.groupby("Produk", as_index=False)["Produksi"].sum()

    fig_pie = px.pie(
        pie_df,
        names="Produk",
        values="Produksi",
        hole=0.5,
        color_discrete_sequence=["#8da98d","#a3b8a3","#c7d9c7"]
    )

    fig_pie.update_layout(
        height=260,
        margin=dict(t=30, b=0),
        paper_bgcolor='rgba(0,0,0,0)'
    )

    st.plotly_chart(fig_pie, use_container_width=True)

# ===== PERBANDINGAN (tidak ikut filter produk) =====
with c3:
    st.subheader("Perbandingan Produk")

    compare_df = df_compare.groupby("Produk", as_index=False)["Produksi"].sum()

    fig_compare = px.bar(
        compare_df,
        x="Produk",
        y="Produksi",
        color="Produk",
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
    "Produksi":"sum",
    "Petani":"sum",
    "Luas_Lahan":"sum"
})

st.dataframe(wilayah_df, height=220, use_container_width=True)

# ======================
# 📸 DOKUMENTASI LAPANGAN
# ======================
st.markdown("---")
st.subheader("📸 Dokumentasi Kegiatan")

# CONTAINER
with st.container():

    col1, col2 = st.columns([1,2])

    # ===== UPLOAD FOTO =====
    with col1:
        uploaded_file = st.file_uploader(
            "Upload Foto Dokumentasi",
            type=["jpg", "jpeg", "png"]
        )

        tanggal = st.date_input("Tanggal Dokumentasi")

    # ===== CAPTION + PREVIEW =====
    with col2:
        caption = st.text_area(
            "Deskripsi / Caption",
            placeholder="Contoh: Kegiatan panen padi di Desa Sukamaju dengan hasil meningkat 20% dibanding bulan lalu..."
        )

        # PREVIEW GAMBAR
        if uploaded_file is not None:
            st.image(uploaded_file, caption=caption if caption else "Preview Gambar", use_container_width=True)
        else:
            st.info("Belum ada gambar diupload")

    # ===== INFO TAMBAHAN =====
    if uploaded_file is not None:
        st.success(f"📅 Tanggal: {tanggal}")
