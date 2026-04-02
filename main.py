import streamlit as st
import pandas as pd
import plotly.express as px

# CONFIG
st.set_page_config(page_title="Dashboard Panen Rempah", layout="wide")

# ======================
# 🎨 SAGE THEME
# ======================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #e6efe9, #f4f7f5);
}
.block-container {
    padding-top: 1rem;
}
div[data-testid="stMetric"] {
    background-color: #ffffff;
    padding: 16px;
    border-radius: 14px;
    border-left: 6px solid #8da98d;
}
h1 {color:#5f7a61;}
h2, h3 {color:#6b8f71;}
</style>
""", unsafe_allow_html=True)

# ======================
# UPLOAD FILE
# ======================
uploaded_file = st.file_uploader("Upload File Excel (.xlsx)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # ======================
    # FILTER
    # ======================
    col1, col2, col3, col4 = st.columns([2,1,1,1])

    with col1:
        st.title("🌾 Dashboard Panen Rempah")

    with col2:
        program = st.selectbox("Program", df["Program"].unique())

    df = df[df["Program"] == program]

    with col3:
        tahun = st.selectbox("Tahun", sorted(df["Tahun"].unique()))

    df = df[df["Tahun"] == tahun]

    with col4:
        produk = st.selectbox("Produk", df["Produk"].unique())

    df = df[df["Produk"] == produk]

    # ======================
    # KPI
    # ======================
    total_panen = df["Produksi"].sum()
    anggaran = total_panen * 15000
    luas_lahan = df["Luas_Lahan"].sum()
    produktivitas = total_panen / luas_lahan if luas_lahan != 0 else 0

    k1, k2, k3, k4 = st.columns(4)

    k1.metric("Anggaran", f"Rp {anggaran:,.0f}")
    k2.metric("Total Panen", f"{total_panen} Kg")
    k3.metric("Luas Lahan", f"{luas_lahan:.1f} Ha")
    k4.metric("Produktivitas", f"{produktivitas:.1f} Kg/Ha")

    # ======================
    # CHART
    # ======================
    c1, c2, c3 = st.columns(3)

    # BAR BULANAN
    with c1:
        st.subheader("Produksi Bulanan")

        bulanan = df.groupby("Bulan")["Produksi"].sum().reset_index()

        fig_bar = px.bar(
            bulanan,
            x="Bulan",
            y="Produksi",
            color_discrete_sequence=["#8da98d"]
        )

        fig_bar.update_layout(height=260, plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_bar, use_container_width=True)

    # PIE
    with c2:
        st.subheader("Komposisi Produk")

        pie_df = df.groupby("Produk")["Produksi"].sum().reset_index()

        fig_pie = px.pie(
            pie_df,
            names="Produk",
            values="Produksi",
            hole=0.5,
            color_discrete_sequence=["#8da98d","#a3b8a3","#c7d9c7"]
        )

        fig_pie.update_layout(height=260)
        st.plotly_chart(fig_pie, use_container_width=True)

    # PERBANDINGAN
    with c3:
        st.subheader("Perbandingan Produk")

        compare_df = df.groupby("Produk")["Produksi"].sum().reset_index()

        fig_compare = px.bar(
            compare_df,
            x="Produk",
            y="Produksi",
            color="Produk",
            color_discrete_sequence=["#8da98d","#a3b8a3","#c7d9c7"]
        )

        fig_compare.update_layout(height=260, showlegend=False)
        st.plotly_chart(fig_compare, use_container_width=True)

    # ======================
    # WILAYAH
    # ======================
    st.subheader("Distribusi Wilayah Desa")

    wilayah_df = df.groupby("Wilayah").agg({
        "Produksi":"sum",
        "Petani":"sum",
        "Luas_Lahan":"sum"
    }).reset_index()

    st.dataframe(wilayah_df, use_container_width=True)

else:
    st.warning("Silakan upload file Excel terlebih dahulu.")
