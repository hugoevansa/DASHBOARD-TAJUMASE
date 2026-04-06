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

pattern_bg = image_to_base64_local("Pattern_PI.png")

st.markdown(f"""
<style>

/* BACKGROUND */
.stApp {{
    background-color: #f4f7f5;
    background-image: url("{pattern_bg}");
    background-size: 300px;
    background-repeat: repeat;
    background-attachment: fixed;
    background-blend-mode: luminosity;
    opacity-adjustment: none;
}}

/* OVERLAY TIPIS AGAR PATTERN TIDAK MENUTUPI KONTEN */
.stApp::before {{
    content: '';
    position: fixed;
    inset: 0;
    background: rgba(230, 239, 233, 0.90);
    pointer-events: none;
    z-index: 0;
}}

/* PASTIKAN SEMUA KONTEN DI ATAS OVERLAY */
.block-container {{
    position: relative;
    z-index: 1;
    padding-top: 1rem;
    padding-bottom: 0rem;
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
div[data-testid="stDataFrame"] {{
    background-color: rgba(255,255,255,0.92);
    border-radius: 12px;
}}

/* SELECTBOX */
div[data-baseweb="select"] {{
    background-color: rgba(255,255,255,0.95);
    border-radius: 10px;
}}

/* CHART CARD EFFECT */
div[data-testid="stPlotlyChart"] {{
    background-color: rgba(230, 239, 233, 0.60) !important;
    border-radius: 16px !important;
    padding: 12px !important;
    border: 1px solid rgba(141, 169, 141, 0.25) !important;
    box-shadow: 0 6px 18px rgba(0,0,0,0.08) !important;
    transition: all 0.25s ease;
}}

div[data-testid="stPlotlyChart"]:hover {{
    transform: translateY(-4px);
    box-shadow: 0 12px 28px rgba(0,0,0,0.12) !important;
}}

div[data-testid="column"] > div:has(div[data-testid="stPlotlyChart"]) {{
    padding: 6px;
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
    tahun_list = ["Semua Tahun"] + sorted(df_filtered["Tahun"].dropna().unique())
    tahun = st.selectbox("Tahun", tahun_list, index=0)  # default = Semua Tahun

if tahun != "Semua Tahun":
    df_filtered = df_filtered[df_filtered["Tahun"] == int(tahun)]

df_doc = df_filtered.copy()

# ======================
# SIMPAN DATA UNTUK PERBANDINGAN (PENTING)
# ======================
df_compare = df_filtered.copy()

# ======================
# FILTER KOMODITAS
# ======================
with col4:
    komoditas_list = ["Semua Komoditas"] + list(df_filtered["Komoditas"].dropna().unique())
    komoditas = st.selectbox("Komoditas", komoditas_list)

if komoditas != "Semua Komoditas":
    df_filtered = df_filtered[df_filtered["Komoditas"] == komoditas]

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

# ===== BAR BULANAN (ikut komoditas) =====
with c1:
    st.subheader("Produksi Bulanan")

    bulanan = df_filtered.groupby("Bulan", as_index=False)["Produksi"].sum()

    # ← Sort by urutan bulan Januari - Desember
    bulan_order = ["January","February","March","April","May","June",
                   "July","August","September","October","November","December"]
    bulanan["Bulan"] = pd.Categorical(bulanan["Bulan"], categories=bulan_order, ordered=True)
    bulanan = bulanan.sort_values("Bulan")

    fig_bar = px.bar(
        bulanan,
        x="Bulan",
        y="Produksi",
        color_discrete_sequence=["#8da98d"],
        category_orders={"Bulan": bulan_order}   # ← pastikan plotly ikut urutan ini
    )

    fig_bar.update_layout(
        height=300,
        margin=dict(t=20, b=80, l=20, r=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        hovermode="x unified",
        xaxis=dict(
            tickangle=-40,
            tickfont=dict(size=10),
            automargin=True,
            title_standoff=25
        ),
        yaxis=dict(
            tickfont=dict(size=10),
            automargin=True,
            title_standoff=15
        )
    )

    st.plotly_chart(fig_bar, use_container_width=True)

# ===== PIE (tidak ikut filter komoditas) =====
with c2:
    st.subheader("Komposisi Komoditas")

    pie_df = df_compare.groupby("Komoditas", as_index=False)["Produksi"].sum()

    fig_pie = px.pie(
        pie_df,
        names="Komoditas",
        values="Produksi",
        hole=0.5,
        color_discrete_sequence=["#8da98d","#a3b8a3","#c7d9c7","#b8ccb8","#d4e4d4","#e8f0e8","#9db89d","#7a9e7a","#6b8f6b","#5c805c","#4d704d"]
    )

    fig_pie.update_traces(
        textposition='inside',
        textfont_size=10,
        insidetextorientation='auto'
    )

    fig_pie.update_layout(
        height=300,
        margin=dict(t=20, b=20, l=20, r=120),   # ← r=120 beri ruang legend
        paper_bgcolor='rgba(0,0,0,0)',
        legend=dict(
            font=dict(size=9),
            x=1.02,
            y=0.5,
            xanchor='left',
            yanchor='middle',
            bgcolor='rgba(0,0,0,0)'
        )
    )

    st.plotly_chart(fig_pie, use_container_width=True)

# ===== PERBANDINGAN (tidak ikut filter komoditas) =====
with c3:
    st.subheader("Perbandingan Komoditas")

    compare_df = df_compare.groupby("Komoditas", as_index=False)["Produksi"].sum()

    fig_compare = px.bar(
        compare_df,
        x="Komoditas",
        y="Produksi",
        color="Komoditas",
        color_discrete_sequence=["#8da98d","#a3b8a3","#c7d9c7","#b8ccb8","#d4e4d4","#e8f0e8","#9db89d","#7a9e7a","#6b8f6b","#5c805c","#4d704d"]
    )

    fig_compare.update_layout(
        height=300,
        margin=dict(t=20, b=80, l=20, r=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        xaxis=dict(
            tickangle=-40,
            tickfont=dict(size=10),
            automargin=True,
            title_standoff=25
        ),
        yaxis=dict(
            tickfont=dict(size=10),
            automargin=True,
            title_standoff=15
        )
    )

    st.plotly_chart(fig_compare, use_container_width=True)
# ======================
# WILAYAH
# ======================
st.markdown("""
<h3 style font-weight: 800; text-transform: uppercase; margin-bottom: 10px;'>
DISTRIBUSI WILAYAH DESA
</h3>
""", unsafe_allow_html=True)

wilayah_df = df_filtered.groupby("Wilayah", as_index=False).agg({
    "Produksi":"sum",
    "Petani":"sum",
    "Luas_Lahan":"sum",
    "Pupuk Phonska":"sum",
    "Pupuk Nitrea":"sum",
    "Pupuk Urea":"sum"
})

st.dataframe(
    wilayah_df.rename(columns={
        "Wilayah": "WILAYAH",
        "Produksi": "PRODUKSI (Kg)",
        "Petani": "PETANI (Orang)",
        "Luas_Lahan": "LUAS LAHAN (Ha)",
        "Pupuk Phonska": "PUPUK PHONSKA (Kg)",
        "Pupuk Nitrea": "PUPUK NITREA (Kg)",
        "Pupuk Urea": "PUPUK UREA (Kg)"
    }).style.set_properties(**{
        'text-align': 'center',
        'font-weight': '500'
    }).set_table_styles([
        {
            'selector': 'th',
            'props': [('text-align', 'center'), ('font-weight', '800'), ('text-transform', 'uppercase')]
        }
    ]),
    height=220,
    use_container_width=True,
    hide_index=True
)

# ======================
# PRODUK OLAHAN (SWIPE VERSION)
# ======================
st.markdown("## PRODUK OLAHAN")

# DATA PRODUK OLAHAN (nama variabel bebas, tapi nanti masuk ke doc_filtered)
data_produk_olahan = pd.DataFrame([
    {
        "caption": "Panen Wilayah A",
        "file": "ProdukOlahan/contoh 1.png",
        "Program": "Lembata",
        "tanggal": "2025-01-12"
    },
    {
        "file": "ProdukOlahan/contoh 2.png",
        "Program": "Lembata",
        "tanggal": "2025-02-15",
        "caption": "Distribusi Hasil"
    },
    {
        "file": "ProdukOlahan/contoh 4.png",
        "Program": "Ruteng",
        "tanggal": "2025-03-20",
        "caption": "Aktivitas Petani"
    },
    {
        "file": "ProdukOlahan/Contoh 5.png",
        "Program": "Sulteng",
        "tanggal": "2025-01-12",
        "caption": "Petani Sulteng"
    },
    {
        "file": "ProdukOlahan/Contoh 6.png",
        "Program": "Giripurno",
        "tanggal": "2025-04-15",
        "caption": "Giripurno Farm"
    },
    {
        "file": "ProdukOlahan/Contoh 7.png",
        "Program": "Sumut",
        "tanggal": "2025-03-20",
        "caption": "Sumatera Sejahtera"
    }
])

# ======================
# PREP DATA
# ======================
data_produk_olahan["tanggal"] = pd.to_datetime(data_produk_olahan["tanggal"])
data_produk_olahan["Tahun"] = data_produk_olahan["tanggal"].dt.year.astype(int)

df_doc = df_doc.copy()
df_doc["Program"] = df_doc["Program"].astype(str).str.lower().str.strip()
data_produk_olahan["Program"] = data_produk_olahan["Program"].astype(str).str.lower().str.strip()

# ======================
# FILTER (tetap pakai doc_filtered 🔥)
# ======================
program_aktif = df_doc["Program"].unique()

if tahun != "Semua Tahun":
    doc_filtered = data_produk_olahan[
        (data_produk_olahan["Program"].isin(program_aktif)) &
        (data_produk_olahan["Tahun"] == int(tahun))
    ].copy()
else:
    doc_filtered = data_produk_olahan[
        (data_produk_olahan["Program"].isin(program_aktif))
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
    st.info("Tidak ada produk olahan untuk filter ini")
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
        st.warning("Tidak ada Produk Olahan")
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

# ======================
# PUPUK (SWIPE VERSION)
# ======================
st.markdown("## PUPUK")

# DATA PUPUK
data_pupuk = pd.DataFrame([
    {
        "caption": "Pupuk Phonska",
        "file": "Pupuk/contoh 1.png",
        "Program": "Lembata",
        "tanggal": "2025-01-12"
    },
    {
        "file": "Pupuk/contoh 2.png",
        "Program": "Lembata",
        "tanggal": "2025-02-15",
        "caption": "Pupuk Urea"
    },
    {
        "file": "Pupuk/contoh 4.png",
        "Program": "Ruteng",
        "tanggal": "2025-03-20",
        "caption": "Pupuk Nitrea"
    },
    {
        "file": "Pupuk/Contoh 5.png",
        "Program": "Sulteng",
        "tanggal": "2025-01-12",
        "caption": "Distribusi Pupuk"
    },
    {
        "file": "Pupuk/Contoh 6.png",
        "Program": "Giripurno",
        "tanggal": "2025-04-15",
        "caption": "Gudang Pupuk"
    },
    {
        "file": "Pupuk/Contoh 7.png",
        "Program": "Sumut",
        "tanggal": "2025-03-20",
        "caption": "Stok Pupuk"
    }
])

# ======================
# PREP DATA
# ======================
data_pupuk["tanggal"] = pd.to_datetime(data_pupuk["tanggal"])
data_pupuk["Tahun"] = data_pupuk["tanggal"].dt.year.astype(int)

df_doc = df_doc.copy()
df_doc["Program"] = df_doc["Program"].astype(str).str.lower().str.strip()
data_pupuk["Program"] = data_pupuk["Program"].astype(str).str.lower().str.strip()

# ======================
# FILTER (tetap doc_filtered 🔥)
# ======================
program_aktif = df_doc["Program"].unique()

if tahun != "Semua Tahun":
    doc_filtered = data_pupuk[
        (data_pupuk["Program"].isin(program_aktif)) &
        (data_pupuk["Tahun"] == int(tahun))
    ].copy()
else:
    doc_filtered = data_pupuk[
        (data_pupuk["Program"].isin(program_aktif))
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
    st.info("Tidak ada pupuk yang digunakan untuk filter ini")
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
        st.warning("Tidak ada Pupuk yang digunakan")
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

# ======================
# DOKUMENTASI (SWIPE VERSION)
# ======================
st.markdown("## Dokumentasi")

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

if tahun != "Semua Tahun":
    doc_filtered = data_dokumentasi[
        (data_dokumentasi["Program"].isin(program_aktif)) &
        (data_dokumentasi["Tahun"] == int(tahun))
    ].copy()
else:
    doc_filtered = data_dokumentasi[
        (data_dokumentasi["Program"].isin(program_aktif))
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
