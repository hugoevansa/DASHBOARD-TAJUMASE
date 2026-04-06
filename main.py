import streamlit as st
import pandas as pd
import plotly.express as px
import base64
from pathlib import Path
import streamlit.components.v1 as components

# CONFIG
st.set_page_config(page_title="TAJUMASE", layout="wide")

# ======================
# 🎨 SAGE THEME STYLE
# ======================
def image_to_base64_local(image_path):
    path = Path(image_path)
    if not path.exists():
        return ""
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    ext = path.suffix.lower().replace(".", "")
    if ext == "jpg":
        ext = "jpeg"
    return f"data:image/{ext};base64,{encoded}"

pattern_bg = image_to_base64_local("Dokumentasi/Pattern PI.png")

st.markdown(f"""
<style>
.stApp {{
    background:
        linear-gradient(rgba(230, 239, 233, 0.92), rgba(244, 247, 245, 0.94)),
        url("{pattern_bg}");
    background-size: cover, 340px;
    background-repeat: no-repeat, repeat;
    background-position: center, top left;
    background-attachment: fixed, fixed;
}}

.block-container {{
    padding-top: 1rem;
    padding-bottom: 0rem;
}}

div[data-testid="stMetric"] {{
    background-color: rgba(255,255,255,0.92);
    padding: 16px;
    border-radius: 14px;
    border-left: 6px solid #8da98d;
    box-shadow: 0 4px 12px rgba(0,0,0,0.04);
}}

h1 {{ color: #5f7a61; }}
h2, h3 {{ color: #6b8f71; }}

[data-testid="stDataFrame"] {{
    background-color: rgba(255,255,255,0.92);
    border-radius: 12px;
}}

div[data-baseweb="select"] {{
    background-color: rgba(255,255,255,0.95);
    border-radius: 10px;
}}
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
    st.title("TAJUMASE")

# ======================
# FILTER PROGRAM
# ======================
with col2:
    program_list = ["Semua Program"] + list(df["Program"].dropna().unique())
    program = st.selectbox("Program", program_list)

if program != "Semua Program":
    df_filtered = df[df["Program"] == program]
else:
    df_filtered = df.copy()

# ======================
# FILTER TAHUN (FIXED)
# ======================
with col3:
    tahun_list = ["Semua Tahun"] + sorted(df_filtered["Tahun"].dropna().unique())
    tahun = st.selectbox("Tahun", tahun_list, index=0)

if tahun != "Semua Tahun":
    df_filtered = df_filtered[df_filtered["Tahun"] == tahun]

df_doc = df_filtered.copy()

# ======================
# SIMPAN UNTUK PIE & COMPARE
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
# CHART
# ======================
c1, c2, c3 = st.columns(3)

with c1:
    st.subheader("Produksi Bulanan")
    bulanan = df_filtered.groupby("Bulan", as_index=False)["Produksi"].sum()
    fig_bar = px.bar(bulanan, x="Bulan", y="Produksi",
                     color_discrete_sequence=["#8da98d"])
    fig_bar.update_layout(height=260, margin=dict(t=30,b=0),
                          plot_bgcolor='rgba(0,0,0,0)',
                          paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_bar, use_container_width=True)

with c2:
    st.subheader("Komposisi Produk")
    pie_df = df_compare.groupby("Produk", as_index=False)["Produksi"].sum()
    fig_pie = px.pie(pie_df, names="Produk", values="Produksi", hole=0.5,
                     color_discrete_sequence=["#8da98d","#a3b8a3","#c7d9c7"])
    fig_pie.update_layout(height=260, margin=dict(t=30,b=0),
                          paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_pie, use_container_width=True)

with c3:
    st.subheader("Perbandingan Produk")
    compare_df = df_compare.groupby("Produk", as_index=False)["Produksi"].sum()
    fig_compare = px.bar(compare_df, x="Produk", y="Produksi",
                         color="Produk",
                         color_discrete_sequence=["#8da98d","#a3b8a3","#c7d9c7"])
    fig_compare.update_layout(height=260, margin=dict(t=30,b=0),
                              plot_bgcolor='rgba(0,0,0,0)',
                              paper_bgcolor='rgba(0,0,0,0)',
                              showlegend=False)
    st.plotly_chart(fig_compare, use_container_width=True)

# ======================
# WILAYAH
# ======================
st.subheader("Distribusi Wilayah Desa")

wilayah_df = df_filtered.groupby("Wilayah", as_index=False).agg({
    "Produksi":"sum",
    "Petani":"sum",
    "Luas_Lahan":"sum",
    "Pupuk Phonska":"sum",
    "Pupuk Nitrea":"sum",
    "Pupuk Urea":"sum"
})

st.dataframe(wilayah_df, height=220, use_container_width=True, hide_index=True)

# ======================
# DOKUMENTASI
# ======================
st.markdown("## 📸 Dokumentasi")

data_dokumentasi = pd.DataFrame([
    {"caption":"Panen Wilayah A","file":"Dokumentasi/contoh 1.png","Program":"Lembata","tanggal":"2025-01-12"},
    {"file":"Dokumentasi/contoh 2.png","Program":"Lembata","tanggal":"2025-02-15","caption":"Distribusi Hasil"},
    {"file":"Dokumentasi/contoh 4.png","Program":"Ruteng","tanggal":"2025-03-20","caption":"Aktivitas Petani"},
    {"file":"Dokumentasi/Contoh 5.png","Program":"Sulteng","tanggal":"2025-01-12","caption":"Petani Sulteng"},
    {"file":"Dokumentasi/Contoh 6.png","Program":"Giripurno","tanggal":"2025-04-15","caption":"Giripurno Farm"},
    {"file":"Dokumentasi/Contoh 7.png","Program":"Sumut","tanggal":"2025-03-20","caption":"Sumatera Sejahtera"}
])

data_dokumentasi["tanggal"] = pd.to_datetime(data_dokumentasi["tanggal"])
data_dokumentasi["Tahun"] = data_dokumentasi["tanggal"].dt.year.astype(int)

df_doc["Program"] = df_doc["Program"].astype(str).str.lower().str.strip()
data_dokumentasi["Program"] = data_dokumentasi["Program"].astype(str).str.lower().str.strip()

program_aktif = df_doc["Program"].unique()

# 🔥 FIX FILTER DOKUMENTASI
if tahun != "Semua Tahun":
    doc_filtered = data_dokumentasi[
        (data_dokumentasi["Program"].isin(program_aktif)) &
        (data_dokumentasi["Tahun"] == int(tahun))
    ].copy()
else:
    doc_filtered = data_dokumentasi[
        (data_dokumentasi["Program"].isin(program_aktif))
    ].copy()

def image_to_base64(path):
    p = Path(path)
    if not p.exists():
        return None
    return f"data:image/png;base64,{base64.b64encode(open(p,'rb').read()).decode()}"

if doc_filtered.empty:
    st.info("Tidak ada dokumentasi untuk filter ini")
else:
    cards_html = ""
    for _, row in doc_filtered.iterrows():
        img = image_to_base64(row["file"])
        if not img:
            continue
        tanggal_label = row["tanggal"].strftime("%d %b %Y")
        cards_html += f"""
        <div class="doc-card">
            <div class="doc-caption">{row["caption"]}</div>
            <div class="doc-image-wrap">
                <img src="{img}" class="doc-image"/>
                <div class="doc-date">{tanggal_label}</div>
            </div>
        </div>
        """

    components.html(f"""
    <div style="display:flex;overflow-x:auto;gap:20px;">
    {cards_html}
    </div>
    """, height=320)
