import streamlit as st
import pandas as pd
import plotly.express as px
import base64
from pathlib import Path
import streamlit.components.v1 as components
import base64
from pathlib import Path


def get_base64_image(image_path):
    path = Path(image_path)
    if not path.exists():
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()
        
pattern_base64 = get_base64_image("Dokumentasi/Pattern PI.png")

# CONFIG
st.set_page_config(page_title="TAJUMASE", layout="wide")

if pattern_base64:
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(135deg, #e6efe9, #f4f7f5);
        }}

        .custom-pattern-bg {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            pointer-events: none;
            background-image:
                linear-gradient(rgba(230,239,233,0.78), rgba(244,247,245,0.82)),
                url("data:image/png;base64,{pattern_base64}");
            background-repeat: repeat;
            background-size: auto, 260px;
            background-position: center, top left;
            opacity: 0.35;
        }}

        .block-container {{
            padding-top: 1rem;
            padding-bottom: 0rem;
        }}

        div[data-testid="stMetric"] {{
            background-color: rgba(255,255,255,0.94);
            padding: 16px;
            border-radius: 14px;
            border-left: 6px solid #8da98d;
            box-shadow: 0 4px 12px rgba(0,0,0,0.04);
        }}

        h1 {{
            color: #5f7a61;
        }}

        h2, h3 {{
            color: #6b8f71;
        }}

        [data-testid="stDataFrame"] {{
            background-color: rgba(255,255,255,0.94);
            border-radius: 12px;
        }}

        div[data-baseweb="select"] {{
            background-color: rgba(255,255,255,0.95);
            border-radius: 10px;
        }}
        </style>

        <div class="custom-pattern-bg"></div>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(135deg, #e6efe9, #f4f7f5);
        }
        </style>
        """,
        unsafe_allow_html=True
    )
# ======================
# 🎨 SAGE THEME STYLE
# ======================


st.markdown(f"""
<style>

/* BACKGROUND */
.stApp {{
    background:
        linear-gradient(rgba(230, 239, 233, 0.92), rgba(244, 247, 245, 0.94)),
        url("{pattern_bg}");
    background-size: cover, 340px;
    background-repeat: no-repeat, repeat;
    background-position: center, top left;
    background-attachment: fixed, fixed;
}}

/* CONTAINER */
.block-container {{
    padding-top: 1rem;
    padding-bottom: 0rem;
}}

/* KPI CARD */
div[data-testid="stMetric"] {{
    background-color: rgba(255,255,255,0.92);
    padding: 16px;
    border-radius: 14px;
    border-left: 6px solid #8da98d;
    box-shadow: 0 4px 12px rgba(0,0,0,0.04);
}}

/* TITLE */
h1 {{
    color: #5f7a61;
}}

/* SUBTITLE */
h2, h3 {{
    color: #6b8f71;
}}

/* DATAFRAME */
[data-testid="stDataFrame"] {{
    background-color: rgba(255,255,255,0.92);
    border-radius: 12px;
}}

/* SELECTBOX */
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
df_doc = df_filtered.copy()

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
    "Luas_Lahan":"sum",
    "Pupuk Phonska":"sum",
    "Pupuk Nitrea":"sum",
    "Pupuk Urea":"sum"
})

st.dataframe(wilayah_df, height=220, use_container_width=True, hide_index=True)

# ======================
# DOKUMENTASI (SWIPE VERSION)
# ======================
st.markdown("## 📸 Dokumentasi")

# DATA DOKUMENTASI
data_dokumentasi = pd.DataFrame([
    {
        "caption": "Panen Wilayah A",
        "file": "Dokumentasi/contoh 1.png",
        "Program": "Lembata",
        "tanggal": "2025-01-12"
    },
    {
        "file": "Dokumentasi/contoh 2.png",
        "Program": "Lembata",
        "tanggal": "2025-02-15",
        "caption": "Distribusi Hasil"
    },
    {
        "file": "Dokumentasi/contoh 4.png",
        "Program": "Ruteng",
        "tanggal": "2025-03-20",
        "caption": "Aktivitas Petani"
    },
    {
        "file": "Dokumentasi/Contoh 5.png",
        "Program": "Sulteng",
        "tanggal": "2025-01-12",
        "caption": "Petani Sulteng"
    },
    {
        "file": "Dokumentasi/Contoh 6.png",
        "Program": "Giripurno",
        "tanggal": "2025-04-15",
        "caption": "Giripurno Farm"
    },
    {
        "file": "Dokumentasi/Contoh 7.png",
        "Program": "Sumut",
        "tanggal": "2025-03-20",
        "caption": "Sumatera Sejahtera"
    }
])

# ======================
# PREP DATA (FIX FINAL)
# ======================
data_dokumentasi["tanggal"] = pd.to_datetime(data_dokumentasi["tanggal"])
data_dokumentasi["Tahun"] = data_dokumentasi["tanggal"].dt.year.astype(int)

# 🔥 NORMALISASI KEDUANYA (WAJIB!)
df_doc = df_doc.copy()
df_doc["Program"] = df_doc["Program"].astype(str).str.lower().str.strip()
data_dokumentasi["Program"] = data_dokumentasi["Program"].astype(str).str.lower().str.strip()

# ======================
# FILTER SESUAI PROGRAM + TAHUN (TANPA PRODUK)
# ======================
program_aktif = df_doc["Program"].unique()

doc_filtered = data_dokumentasi[
    (data_dokumentasi["Program"].isin(program_aktif)) &
    (data_dokumentasi["Tahun"] == int(tahun))
].copy()

# ======================
# HELPER: IMAGE TO BASE64
# ======================
def image_to_base64(image_path):
    path = Path(image_path)
    if not path.exists():
        return None
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    ext = path.suffix.lower().replace(".", "")
    if ext == "jpg":
        ext = "jpeg"
    return f"data:image/{ext};base64,{encoded}"

# ======================
# RENDER CAROUSEL
# ======================
if doc_filtered.empty:
    st.info("Tidak ada dokumentasi untuk filter ini")
else:
    cards_html = ""

    for _, row in doc_filtered.iterrows():
        img_src = image_to_base64(row["file"])

        if img_src is None:
            continue

        tanggal_label = row["tanggal"].strftime("%d %b %Y")

        cards_html += f"""
        <div class="doc-card">
            <div class="doc-caption">{row["caption"]}</div>
        
            <div class="doc-image-wrap">
                <img src="{img_src}" class="doc-image"/>
                <div class="doc-date">{tanggal_label}</div>
            </div>
        </div>
        """
    if cards_html.strip() == "":
        st.warning("File gambar dokumentasi tidak ditemukan. Pastikan path file benar.")
    else:
        carousel_html = f"""
        <style>
            .netflix-wrap {{
                position: relative;
                width: 100%;
                padding: 8px 0 16px 0;
            }}

            .netflix-track {{
                display: flex;
                gap: 20px;
                overflow-x: auto;
                scroll-behavior: smooth;
                scrollbar-width: none;
                padding: 6px 8px 14px 8px;
            }}

            .netflix-track::-webkit-scrollbar {{
                display: none;
            }}

            .doc-card {{
                flex: 0 0 32%;
                min-width: 320px;
                max-width: 420px;
                transition: transform 0.35s ease, box-shadow 0.35s ease;
            }}

            .doc-card:hover {{
                transform: scale(1.03);
            }}

            .doc-image-wrap {{
                position: relative;
                border-radius: 18px;
                overflow: hidden;
                box-shadow: 0 10px 24px rgba(0,0,0,0.10);
                background: #fff;
            }}

            .doc-image {{
                width: 100%;
                height: 240px;
                object-fit: cover;
                display: block;
            }}

            .doc-date {{
                position: absolute;
                right: 12px;
                bottom: 12px;
                background: rgba(0,0,0,0.65);
                color: #fff;
                padding: 6px 10px;
                border-radius: 10px;
                font-size: 12px;
                font-weight: 600;
            }}

            .doc-caption {{
                margin-top: 12px;
                font-size: 18px;
                font-weight: 700;
                color: #2f3e34;
                padding-left: 2px;
            }}

            .nav-btn {{
                position: absolute;
                top: 40%;
                transform: translateY(-50%);
                z-index: 10;
                width: 46px;
                height: 46px;
                border: none;
                border-radius: 999px;
                background: rgba(40, 40, 40, 0.70);
                color: white;
                font-size: 26px;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: all 0.25s ease;
                backdrop-filter: blur(4px);
            }}

            .nav-btn:hover {{
                background: rgba(20, 20, 20, 0.90);
                transform: translateY(-50%) scale(1.08);
            }}

            .nav-left {{
                left: 0;
            }}

            .nav-right {{
                right: 0;
            }}

        </style>

        <div class="netflix-wrap">
            <button class="nav-btn nav-left" onclick="scrollDocs(-1)">&#10094;</button>
            <button class="nav-btn nav-right" onclick="scrollDocs(1)">&#10095;</button>

            <div class="netflix-track" id="docs-track">
                {cards_html}
            </div>
        </div>

        <script>
            function scrollDocs(direction) {{
                const track = document.getElementById("docs-track");
                const card = track.querySelector(".doc-card");
                if (!card) return;

                const style = window.getComputedStyle(track);
                const gap = parseInt(style.columnGap || style.gap || 20);
                const scrollAmount = card.offsetWidth + gap;

                track.scrollBy({{
                    left: direction * scrollAmount,
                    behavior: "smooth"
                }});
            }}
        </script>
        """

        components.html(carousel_html, height=380)
