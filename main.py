import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
import pandas as pd
import plotly.express as px
import base64
from pathlib import Path
import textwrap
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
    background: rgba(230, 239, 233, 0.70);
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
# LOAD LOGO
# ======================
logo_path = "Dokumentasi/Pupuk4.png"  # ← Ganti sesuai nama file logo kamu
logo_b64 = image_to_base64_local(logo_path)

# ======================
# HEADER + FILTER
# ======================
col1, col2, col3, col4 = st.columns([2,1,1,1])

with col1:
    if logo_b64:
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 14px; padding-top: 18px;">
            <img src="{logo_b64}" style="height: 60px; width: auto; object-fit: contain;"/>
            <h1 style="margin: 0; color: #5f7a61;">TAJUMASE</h1>
        </div>
        """, unsafe_allow_html=True)
    else:
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
# ===== PRODUKSI + ANGGARAN BULANAN =====
with c1:
    st.subheader("Produksi Bulanan (Kg)")

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
        category_orders={"Bulan": bulan_order}  
    )

    fig_bar.update_layout(
        height=300,
        margin=dict(t=20, b=80, l=20, r=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(230, 239, 233, 0.60)',  
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
    st.subheader("Komposisi Komoditas (%)")

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
        margin=dict(t=20, b=20, l=20, r=120),
        paper_bgcolor='rgba(230, 239, 233, 0.60)',
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
    st.subheader("Perbandingan Komoditas (Kg)")

    compare_df = df_compare.groupby("Komoditas", as_index=False)["Produksi"].sum()

    fig_compare = px.bar(
        compare_df,
        x="Komoditas",
        y="Produksi",
        color="Komoditas",
        color_discrete_sequence=["#5f7a61","#6b8f6b","#7a9e7a","#8da98d","#4d704d","#3d5c3d","#9db89d","#a3b8a3","#5c805c","#4a6b4a","#3a5a3a"]
    )

    fig_compare.update_layout(
        height=300,
        margin=dict(t=20, b=80, l=20, r=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(230, 239, 233, 0.60)', 
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
# TIME SERIES + KETERANGAN
# ======================
ts_col1, ts_col2 = st.columns([2, 1], vertical_alignment="bottom")

with ts_col1:
    st.subheader("Produksi & Anggaran Bulanan")

    bulanan_ts = df_filtered.groupby("Bulan", as_index=False).agg({
        "Produksi": "sum",
        "Anggaran": "sum"
    })

    bulan_order = ["January","February","March","April","May","June",
                   "July","August","September","October","November","December"]

    bulan_short_map = {
        "January": "Jan",
        "February": "Feb",
        "March": "Mar",
        "April": "Apr",
        "May": "May",
        "June": "Jun",
        "July": "Jul",
        "August": "Aug",
        "September": "Sep",
        "October": "Oct",
        "November": "Nov",
        "December": "Dec"
    }

    bulanan_ts["Bulan"] = pd.Categorical(
        bulanan_ts["Bulan"],
        categories=bulan_order,
        ordered=True
    )
    bulanan_ts = bulanan_ts.sort_values("Bulan")
    bulanan_ts["Bulan_Short"] = bulanan_ts["Bulan"].map(bulan_short_map)

    fig_ts = make_subplots(specs=[[{"secondary_y": True}]])

    # BAR PRODUKSI
    fig_ts.add_trace(
        go.Bar(
            x=bulanan_ts["Bulan_Short"],
            y=bulanan_ts["Produksi"],
            name="Produksi",
            marker=dict(
                color="rgba(141,169,141,0.72)",
                line=dict(color="rgba(141,169,141,1)", width=1)
            ),
            hovertemplate="<b>%{x}</b><br>Produksi: %{y:,.0f} Kg<extra></extra>"
        ),
        secondary_y=False
    )

    # LINE ANGGARAN
    fig_ts.add_trace(
        go.Scatter(
            x=bulanan_ts["Bulan_Short"],
            y=bulanan_ts["Anggaran"],
            mode="lines+markers",
            name="Anggaran",
            line=dict(color="#f08a3c", width=3, shape="spline"),
            marker=dict(size=7, color="#ff9d4d"),
            hovertemplate="<b>%{x}</b><br>Anggaran: Rp %{y:,.0f}<extra></extra>"
        ),
        secondary_y=True
    )

    fig_ts.update_layout(
        height=320,
        margin=dict(t=20, b=40, l=20, r=20),
        paper_bgcolor='rgba(230, 239, 233, 0.00)',
        plot_bgcolor='rgba(230, 239, 233, 0.00)',
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        xaxis=dict(
            title="",
            tickfont=dict(size=11),
            showgrid=False,
            zeroline=False
        ),
        yaxis=dict(
            title="Produksi (Kg)",
            tickfont=dict(size=10),
            title_font=dict(color="#5f7a61"),
            gridcolor="rgba(95,122,97,0.12)",
            zeroline=False
        )
    )

    fig_ts.update_yaxes(
        title_text="Anggaran (Rp)",
        secondary_y=True,
        tickfont=dict(size=10, color="#f08a3c"),
        title_font=dict(color="#f08a3c"),
        showgrid=False
    )

    st.plotly_chart(fig_ts, use_container_width=True)

# ======================
# TOP 3 PUPUK TERBANYAK
# ======================
pupuk_rank_df = pd.DataFrame({
    "Pupuk": ["Pupuk Phonska", "Pupuk Nitrea", "Pupuk Urea"],
    "Jumlah": [
        df_filtered["Pupuk Phonska"].sum(),
        df_filtered["Pupuk Nitrea"].sum(),
        df_filtered["Pupuk Urea"].sum()
    ]
}).sort_values("Jumlah", ascending=False).reset_index(drop=True)

top1_name = pupuk_rank_df.loc[0, "Pupuk"] if len(pupuk_rank_df) > 0 else "-"
top1_val  = pupuk_rank_df.loc[0, "Jumlah"] if len(pupuk_rank_df) > 0 else 0

top2_name = pupuk_rank_df.loc[1, "Pupuk"] if len(pupuk_rank_df) > 1 else "-"
top2_val  = pupuk_rank_df.loc[1, "Jumlah"] if len(pupuk_rank_df) > 1 else 0

top3_name = pupuk_rank_df.loc[2, "Pupuk"] if len(pupuk_rank_df) > 2 else "-"
top3_val  = pupuk_rank_df.loc[2, "Jumlah"] if len(pupuk_rank_df) > 2 else 0

with ts_col2:
    st.markdown("<div style='height: 54px;'></div>", unsafe_allow_html=True)

    pupuk_html = textwrap.dedent(f"""
    <style>
    .pupuk-summary-box {{
        background: linear-gradient(180deg, rgba(255,255,255,0.92), rgba(240,246,240,0.92));
        border-radius: 20px;
        padding: 20px 18px;
        box-shadow: 0 8px 22px rgba(0,0,0,0.06);
        min-height: 266px;
        border: 1px solid rgba(141,169,141,0.22);
        position: relative;
        overflow: hidden;
    }}

    .pupuk-summary-title {{
        margin: 0 0 16px 0;
        color: #5f7a61;
        font-size: 18px;
        font-weight: 800;
        letter-spacing: 0.3px;
    }}

    .pupuk-rank-card {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-radius: 14px;
        padding: 12px 14px;
        margin-bottom: 12px;
    }}

    .pupuk-rank-left {{
        display: flex;
        flex-direction: column;
    }}

    .pupuk-rank-label {{
        font-size: 12px;
        color: #7a8d7a;
        font-weight: 700;
    }}

    .pupuk-rank-name {{
        font-size: 15px;
        color: #2f3e34;
        font-weight: 800;
    }}

    .pupuk-rank-value {{
        font-size: 14px;
        font-weight: 800;
    }}

    .rank-1 {{
        background: rgba(255,255,255,0.84);
        border-left: 6px solid #5f7a61;
    }}

    .rank-2 {{
        background: rgba(255,255,255,0.80);
        border-left: 6px solid #8da98d;
    }}

    .rank-3 {{
        background: rgba(255,255,255,0.76);
        border-left: 6px solid #b8ccb8;
        margin-bottom: 0;
    }}

    .value-1 {{ color: #5f7a61; }}
    .value-2 {{ color: #6b8f71; }}
    .value-3 {{ color: #7b9b7d; }}
    </style>

    <div class="pupuk-summary-box">
        <div class="pupuk-summary-title">🌿 Pupuk Terbanyak Dipakai</div>

        <div class="pupuk-rank-card rank-1">
            <div class="pupuk-rank-left">
                <div class="pupuk-rank-label">#1 TERBANYAK</div>
                <div class="pupuk-rank-name">{top1_name}</div>
            </div>
            <div class="pupuk-rank-value value-1">{top1_val:,.0f} Kg</div>
        </div>

        <div class="pupuk-rank-card rank-2">
            <div class="pupuk-rank-left">
                <div class="pupuk-rank-label">#2 TERBANYAK</div>
                <div class="pupuk-rank-name">{top2_name}</div>
            </div>
            <div class="pupuk-rank-value value-2">{top2_val:,.0f} Kg</div>
        </div>

        <div class="pupuk-rank-card rank-3">
            <div class="pupuk-rank-left">
                <div class="pupuk-rank-label">#3 TERBANYAK</div>
                <div class="pupuk-rank-name">{top3_name}</div>
            </div>
            <div class="pupuk-rank-value value-3">{top3_val:,.0f} Kg</div>
        </div>
    </div>
    """)

    st.markdown(pupuk_html, unsafe_allow_html=True)
    
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
# PRODUK OLAHAN (SWIPE VERSION - FILTER PROGRAM + TAHUN)
# ======================
st.markdown("## PRODUK OLAHAN")

data_produk_olahan = pd.DataFrame([
    {
        "caption": "Sabun Olahan",
        "file": "Dokumentasi/contoh 1.png",
        "Program": "Lembata",
        "tanggal": "2025-01-12"
    },
    {
        "caption": "Bubuk Olahan",
        "file": "Dokumentasi/Bubuk4.png",
        "Program": "Ruteng",
        "tanggal": "2025-02-15"
    }
])

data_produk_olahan["tanggal"] = pd.to_datetime(data_produk_olahan["tanggal"])
data_produk_olahan["Tahun"] = data_produk_olahan["tanggal"].dt.year.astype(int)

df_doc_produk = df_doc.copy()
df_doc_produk["Program"] = df_doc_produk["Program"].astype(str).str.lower().str.strip()
data_produk_olahan["Program"] = data_produk_olahan["Program"].astype(str).str.lower().str.strip()

program_aktif = df_doc_produk["Program"].unique()

if tahun != "Semua Tahun":
    doc_filtered = data_produk_olahan[
        (data_produk_olahan["Program"].isin(program_aktif)) &
        (data_produk_olahan["Tahun"] == int(tahun))
    ].copy()
else:
    doc_filtered = data_produk_olahan[
        (data_produk_olahan["Program"].isin(program_aktif))
    ].copy()

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

if doc_filtered.empty:
    st.info("Tidak ada produk olahan untuk filter ini")
else:
    cards_html = ""

    for _, row in doc_filtered.iterrows():
        img_src = image_to_base64(row["file"])
        if img_src is None:
            continue

        cards_html += f"""
        <div class="olahan-card">
            <div class="olahan-caption">{row["caption"]}</div>

            <div class="olahan-image-wrap">
                <img src="{img_src}" class="olahan-image"/>
            </div>
        </div>
        """

    if cards_html.strip() == "":
        st.warning("File gambar produk olahan tidak ditemukan. Pastikan path file benar.")
    else:
        olahan_html = f"""
        <style>
            .olahan-wrap {{
                position: relative;
                width: 100%;
                padding: 8px 0 20px 0;
            }}

            .olahan-track {{
                display: flex;
                gap: 10px;
                overflow-x: auto;
                scroll-behavior: smooth;
                scrollbar-width: none;
                padding: 0 40px;
                align-items: flex-end;
            }}

            .olahan-track::-webkit-scrollbar {{
                display: none;
            }}

            .olahan-card {{
                flex: 0 0 33%;
                min-width: 360px;
                max-width: 520px;
                background: transparent !important;
                box-shadow: none !important;
                border: none !important;
                padding: 0 !important;
                margin: 0 !important;
            }}
            
             .olahan-caption {{
                font-size: 20px;
                font-weight: 800;
                color: #2f3e34;
                margin-bottom: 12px;
            
                text-align: center;
                letter-spacing: 0.5px;
            }}
            
            .olahan-image-wrap {{
                position: relative;
                background: transparent !important;
                box-shadow: none !important;
                border: none !important;
                border-radius: 0 !important;
                overflow: visible !important;
                display: flex;
                align-items: center;
                justify-content: center;
                min-height: 360px;
            }}

            .olahan-image {{
                width: 100%;
                height: 360px;
                object-fit: contain;
                display: block;
                filter: drop-shadow(0 14px 20px rgba(0,0,0,0.14));
                background: transparent !important;
            }}

            .olahan-nav-btn {{
                position: absolute;
                top: 50%;
                transform: translateY(-50%);
                z-index: 10;
                width: 54px;
                height: 54px;
                border: none;
                border-radius: 999px;
                background: rgba(60, 60, 60, 0.72);
                color: white;
                font-size: 30px;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: all 0.25s ease;
                backdrop-filter: blur(4px);
            }}

            .olahan-nav-btn:hover {{
                background: rgba(30, 30, 30, 0.92);
                transform: translateY(-50%) scale(1.08);
            }}

            .olahan-nav-left {{
                left: 0;
            }}

            .olahan-nav-right {{
                right: 0;
            }}
        </style>

        <div class="olahan-wrap">
            <button class="olahan-nav-btn olahan-nav-left" onclick="scrollOlahan(-1)">&#10094;</button>
            <button class="olahan-nav-btn olahan-nav-right" onclick="scrollOlahan(1)">&#10095;</button>

            <div class="olahan-track" id="olahan-track">
                {cards_html}
            </div>
        </div>

        <script>
            function scrollOlahan(direction) {{
                const track = document.getElementById("olahan-track");
                const card = track.querySelector(".olahan-card");
                if (!card) return;

                const style = window.getComputedStyle(track);
                const gap = parseInt(style.columnGap || style.gap || 10);
                const scrollAmount = card.offsetWidth + gap;

                track.scrollBy({{
                    left: direction * scrollAmount,
                    behavior: "smooth"
                }});
            }}
        </script>
        """

        components.html(olahan_html, height=460)


# ======================
# CHART PRODUK OLAHAN
# ======================
# tampil HANYA kalau Program dan Tahun dipilih spesifik
if program == "Semua Program" or tahun == "Semua Tahun":
    st.info("Chart Produk Olahan akan muncul jika Program dan Tahun dipilih spesifik.")
else:
    c4, c5 = st.columns(2)

    # ===== C4: PRODUKSI PRODUK OLAHAN =====
    with c4:
        st.subheader("Produksi Produk Olahan")

        produk_olahan_df = (
            df_filtered.groupby("Produk_Olahan", as_index=False)["Data_Produksi_Olahan"]
            .sum()
        )

        # hilangkan value 0
        produk_olahan_df = produk_olahan_df[produk_olahan_df["Data_Produksi_Olahan"] > 0]

        if produk_olahan_df.empty:
            st.info("Tidak ada data produksi produk olahan untuk filter ini.")
        else:
            fig_c4 = px.bar(
                produk_olahan_df,
                x="Produk_Olahan",
                y="Data_Produksi_Olahan",
                color="Produk_Olahan",
                color_discrete_sequence=["#5f7a61","#6b8f6b","#7a9e7a","#8da98d","#4d704d","#3d5c3d","#9db89d","#a3b8a3","#5c805c","#4a6b4a","#3a5a3a"]
            )

            fig_c4.update_layout(
                height=300,
                margin=dict(t=20, b=80, l=20, r=20),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(230, 239, 233, 0.60)',
                showlegend=False,
                xaxis=dict(
                    tickangle=-40,
                    tickfont=dict(size=10),
                    automargin=True,
                    title_standoff=25,
                    title_text="Produk Olahan"
                ),
                yaxis=dict(
                    tickfont=dict(size=10),
                    automargin=True,
                    title_standoff=15,
                    title_text="Produksi (Kg)"
                )
            )

            st.plotly_chart(fig_c4, use_container_width=True)

    # ===== C5: PENJUALAN PRODUK OLAHAN =====
    with c5:
        st.subheader("Penjualan Produk Olahan")

        penjualan_olahan_df = (
            df_filtered.groupby("Produk_Olahan", as_index=False)["Data_Penjualan_Olahan"]
            .sum()
        )

        # hilangkan value 0
        penjualan_olahan_df = penjualan_olahan_df[penjualan_olahan_df["Data_Penjualan_Olahan"] > 0]

        if penjualan_olahan_df.empty:
            st.info("Tidak ada data penjualan produk olahan untuk filter ini.")
        else:
            fig_c5 = px.bar(
                penjualan_olahan_df,
                x="Produk_Olahan",
                y="Data_Penjualan_Olahan",
                color="Produk_Olahan",
                color_discrete_sequence=["#3d5c3d","#4a6b4a","#5c805c","#6b8f6b","#3a5a3a","#5f7a61","#7a9e7a","#8da98d","#4d704d","#9db89d","#a3b8a3"]
            )

            fig_c5.update_layout(
                height=300,
                margin=dict(t=20, b=80, l=20, r=20),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(230, 239, 233, 0.60)',
                showlegend=False,
                xaxis=dict(
                    tickangle=-40,
                    tickfont=dict(size=10),
                    automargin=True,
                    title_standoff=25,
                    title_text="Produk Olahan"
                ),
                yaxis=dict(
                    tickfont=dict(size=10),
                    automargin=True,
                    title_standoff=15,
                    title_text="Penjualan (Bulan)"
                )
            )

            st.plotly_chart(fig_c5, use_container_width=True)


# ======================
# PUPUK (SWIPE VERSION - NO FILTER)
# ======================
st.markdown("## PUPUK")

# DATA PUPUK
data_pupuk = pd.DataFrame([
    {
        "caption": "Pupuk Phonska",
        "file": "Dokumentasi/Pupuk1.png"
    },
    {
        "caption": "Pupuk Urea",
        "file": "Dokumentasi/Pupuk2.png"
    },
    {
        "caption": "Pupuk Nitrea",
        "file": "Dokumentasi/Pupuk3.png"
    }
])

# TIDAK IKUT FILTER APAPUN
doc_filtered = data_pupuk.copy()

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
    st.info("Tidak ada pupuk yang digunakan")
else:
    cards_html = ""

    for _, row in doc_filtered.iterrows():
        img_src = image_to_base64(row["file"])

        if img_src is None:
            continue

        cards_html += f"""
        <div class="pupuk-card">
            <div class="pupuk-caption">{row["caption"]}</div>

            <div class="pupuk-image-wrap">
                <img src="{img_src}" class="pupuk-image"/>
            </div>
        </div>
        """

    if cards_html.strip() == "":
        st.warning("File gambar pupuk tidak ditemukan. Pastikan path file benar.")
    else:
        pupuk_html = f"""
        <style>
            .pupuk-wrap {{
                position: relative;
                width: 100%;
                padding: 8px 0 20px 0;
            }}

            .pupuk-track {{
                display: flex;
                gap: 10px;
                overflow-x: auto;
                scroll-behavior: smooth;
                scrollbar-width: none;
                padding: 0 40px;
                align-items: flex-end;
            }}

            .pupuk-track::-webkit-scrollbar {{
                display: none;
            }}

            .pupuk-card {{
                flex: 0 0 33%;
                min-width: 360px;
                max-width: 520px;
                background: transparent !important;
                box-shadow: none !important;
                border: none !important;
                padding: 0 !important;
                margin: 0 !important;
            }}

            .pupuk-caption {{
                font-size: 20px;
                font-weight: 800;
                color: #2f3e34;
                margin-bottom: 12px;
            
                text-align: center;
                letter-spacing: 0.5px;
            }}

            .pupuk-image-wrap {{
                position: relative;
                background: transparent !important;
                box-shadow: none !important;
                border: none !important;
                border-radius: 0 !important;
                overflow: visible !important;
                display: flex;
                align-items: center;
                justify-content: center;
                min-height: 360px;
            }}

            .pupuk-image {{
                width: 100%;
                height: 360px;
                object-fit: contain;
                display: block;
                filter: drop-shadow(0 14px 20px rgba(0,0,0,0.14));
                background: transparent !important;
            }}

            .pupuk-nav-btn {{
                position: absolute;
                top: 50%;
                transform: translateY(-50%);
                z-index: 10;
                width: 54px;
                height: 54px;
                border: none;
                border-radius: 999px;
                background: rgba(60, 60, 60, 0.72);
                color: white;
                font-size: 30px;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: all 0.25s ease;
                backdrop-filter: blur(4px);
            }}

            .pupuk-nav-btn:hover {{
                background: rgba(30, 30, 30, 0.92);
                transform: translateY(-50%) scale(1.08);
            }}

            .pupuk-nav-left {{
                left: 0;
            }}

            .pupuk-nav-right {{
                right: 0;
            }}
        </style>

        <div class="pupuk-wrap">
            <button class="pupuk-nav-btn pupuk-nav-left" onclick="scrollPupuk(-1)">&#10094;</button>
            <button class="pupuk-nav-btn pupuk-nav-right" onclick="scrollPupuk(1)">&#10095;</button>

            <div class="pupuk-track" id="pupuk-track">
                {cards_html}
            </div>
        </div>

        <script>
            function scrollPupuk(direction) {{
                const track = document.getElementById("pupuk-track");
                const card = track.querySelector(".pupuk-card");
                if (!card) return;

                const style = window.getComputedStyle(track);
                const gap = parseInt(style.columnGap || style.gap || 10);
                const scrollAmount = card.offsetWidth + gap;

                track.scrollBy({{
                    left: direction * scrollAmount,
                    behavior: "smooth"
                }});
            }}
        </script>
        """

        components.html(pupuk_html, height=460)

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
            <div class="doc-image-wrap">
                <img src="{img_src}" class="doc-image"/>
        
                <div class="doc-overlay">
                    <div class="doc-title">{row["caption"]}</div>
                    <div class="doc-date">{tanggal_label}</div>
                </div>
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
                box-shadow: 0 12px 28px rgba(0,0,0,0.12);
                background: #fff;
            }}
            
            .doc-image {{
                width: 100%;
                height: 260px;
                object-fit: cover;
                display: block;
                transition: transform 0.4s ease;
            }}
            
            .doc-card:hover .doc-image {{
                transform: scale(1.05);
            }}
            
            .doc-overlay {{
                position: absolute;
                left: 0;
                bottom: 0;
                width: 100%;
                padding: 14px 16px;
            
                display: flex;
                justify-content: space-between;
                align-items: center;
            
                background: linear-gradient(
                    to top,
                    rgba(0,0,0,0.88),
                    rgba(0,0,0,0.55),
                    rgba(0,0,0,0.00)
                );
            }}
            
            .doc-title {{
                color: white;
                font-size: 16px;
                font-weight: 700;
            }}
            
            .doc-date {{
                position: absolute;
                right: 40px;  
                bottom: 10px;
            
                background: rgba(255,255,255,0.92);
                color: #2f3e34;
                padding: 5px 12px;
                border-radius: 999px;
                font-size: 12px;
                font-weight: 600;
            }}
            
            .doc-caption {{
                display: none;
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
            const track = document.getElementById("docs-track");
            let isScrolling = false;
        
            function getCardWidth() {{
                const card = track.querySelector(".doc-card");
                if (!card) return 0;
        
                const style = window.getComputedStyle(track);
                const gap = parseInt(style.columnGap || style.gap || 20);
                return card.offsetWidth + gap;
            }}
        
            function scrollDocs(direction) {{
                if (isScrolling) return;
        
                const cardWidth = getCardWidth();
                if (!cardWidth) return;
        
                const maxScrollLeft = track.scrollWidth - track.clientWidth;
                const current = track.scrollLeft;
                const tolerance = 5;
        
                isScrolling = true;
        
                // Klik kanan di ujung -> balik ke awal
                if (direction > 0 && current >= maxScrollLeft - tolerance) {{
                    track.scrollTo({{
                        left: 0,
                        behavior: "smooth"
                    }});
        
                    setTimeout(() => {{
                        isScrolling = false;
                    }}, 500);
        
                    return;
                }}
        
                // Klik kiri di awal -> pindah ke ujung
                if (direction < 0 && current <= tolerance) {{
                    track.scrollTo({{
                        left: maxScrollLeft,
                        behavior: "smooth"
                    }});
        
                    setTimeout(() => {{
                        isScrolling = false;
                    }}, 500);
        
                    return;
                }}
        
                // Scroll normal
                track.scrollBy({{
                    left: direction * cardWidth,
                    behavior: "smooth"
                }});
        
                setTimeout(() => {{
                    isScrolling = false;
                }}, 500);
            }}
        </script>
        """

        components.html(carousel_html, height=380)                
