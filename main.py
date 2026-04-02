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
# DOKUMENTASI (SWIPE VERSION)
# ======================
st.markdown("## 📸 Dokumentasi")

# DATA DOKUMENTASI
data_dokumentasi = pd.DataFrame({
    "file": [
        "Dokumentasi/contoh 1.png",
        "Dokumentasi/contoh 2.png",
        "Dokumentasi/contoh 4.png",
        "Dokumentasi/Contoh 5.png",
        "Dokumentasi/Contoh 6.png",
        "Dokumentasi/Contoh 7.png"
    ],
    "Program": ["Lembata", "Lembata", "Ruteng", "Sulteng", "Giripurno", "Sumut"],
    "tanggal": ["2025-01-12", "2025-02-15", "2025-03-20", "2025-01-12", "2025-04-15", "2025-03-20"],
    "caption": [
        "Panen Wilayah A",
        "Distribusi Hasil",
        "Aktivitas Petani",
        "Petani Sulteng",
        "Giripurno Farm",
        "Sumatera Sejahtera"
    ]
})

# ======================
# PREP DATA (TAHUN)
# ======================
data_dokumentasi["tanggal"] = pd.to_datetime(data_dokumentasi["tanggal"])
data_dokumentasi["Tahun"] = data_dokumentasi["tanggal"].dt.year.astype(int)

# ======================
# NORMALISASI
# ======================
df_filtered = df_filtered.copy()
df_filtered["Program"] = df_filtered["Program"].astype(str).str.lower().str.strip()
data_dokumentasi["Program"] = data_dokumentasi["Program"].astype(str).str.lower().str.strip()

# ======================
# FILTER PROGRAM + TAHUN
# ======================
wilayah_aktif = df_filtered["Program"].unique()

doc_filtered = data_dokumentasi[
    (data_dokumentasi["Program"].isin(wilayah_aktif)) &
    (data_dokumentasi["Tahun"] == tahun)
]

# ======================
# CSS
# ======================
st.markdown("""
<style>
.wrapper {
    position: relative;
}
.date-badge {
    position: absolute;
    bottom: 10px;
    right: 12px;
    background: rgba(0,0,0,0.6);
    color: white;
    padding: 4px 10px;
    border-radius: 8px;
    font-size: 12px;
}
</style>
""", unsafe_allow_html=True)

# ======================
# DISPLAY SWIPE
# ======================
if doc_filtered.empty:
    st.info("Tidak ada dokumentasi untuk filter ini")
else:
    total_docs = len(doc_filtered)

    # FIX ERROR SLIDER
    if total_docs <= 3:
        start_idx = 0
    else:
        start_idx = st.slider(
            "",
            0,
            total_docs - 3,
            0,
            label_visibility="collapsed"
        )

    visible_docs = doc_filtered.iloc[start_idx:start_idx+3]

    cols = st.columns(3)

    for i in range(3):
        with cols[i]:
            if i < len(visible_docs):
                r = visible_docs.iloc[i]

                st.markdown(f"**{r['caption']}**")

                st.markdown('<div class="wrapper">', unsafe_allow_html=True)
                st.image(r["file"], use_container_width=True)

                st.markdown(
                    f'<div class="date-badge">{r["tanggal"].strftime("%d %b %Y")}</div>',
                    unsafe_allow_html=True
                )
                st.markdown('</div>', unsafe_allow_html=True)

            else:
                st.empty()

    # FIX 3 KOLOM
    cols = st.columns(3)

    for i in range(3):
        with cols[i]:
            if i < len(visible_docs):
                r = visible_docs.iloc[i]

                # JUDUL
                st.markdown(f"**{r['caption']}**")

                # IMAGE + BADGE
                st.markdown('<div class="wrapper">', unsafe_allow_html=True)
                st.image(r["file"], use_container_width=True)

                st.markdown(
                    f'<div class="date-badge">{r["tanggal"].strftime("%d %b %Y")}</div>',
                    unsafe_allow_html=True
                )
                st.markdown('</div>', unsafe_allow_html=True)

            else:
                st.empty()
