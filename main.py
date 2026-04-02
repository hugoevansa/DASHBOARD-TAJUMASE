import streamlit as st
import pandas as pd
import numpy as np

# CONFIG
st.set_page_config(page_title="Dashboard Analytics", layout="wide")

# ======================
# HEADER FILTER
# ======================
st.title("Dashboard Analytics")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.selectbox("Property name", ["GA Property 1", "GA Property 2"])
with col2:
    st.selectbox("Channel", ["All", "Organic", "Direct"])
with col3:
    st.selectbox("Session source / medium", ["All", "Google", "Social"])
with col4:
    st.selectbox("Device category", ["All", "Mobile", "Desktop"])
with col5:
    st.selectbox("Country", ["Indonesia", "USA", "UK"])

st.divider()

# ======================
# KPI CARDS
# ======================
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpi1.metric("Sessions", "5.1M")
kpi2.metric("Total users", "2.9M")
kpi3.metric("New users", "1.8M")
kpi4.metric("Avg. engagement time", "06:15")

st.divider()

# ======================
# TABLE + PIE CHART
# ======================
left, right = st.columns([2,1])

# Dummy data table
data = pd.DataFrame({
    "Channel": ["Organic Search", "Direct", "Referral", "Paid Search"],
    "Sessions": [2800000, 1300000, 768000, 132000],
    "Total users": [1900000, 581000, 278000, 63500],
    "New users": [1500000, 268700, 41400, 24400],
    "Conversions": [3300000, 4400000, 2400000, 461500]
})

with left:
    st.subheader("Channel Performance")
    st.dataframe(data, use_container_width=True)

with right:
    st.subheader("Properties Breakdown")
    pie_data = pd.DataFrame({
        "Property": ["GA Property 1", "GA Property 2", "GA Property 3"],
        "Users": [67.1, 31.5, 1.4]
    })
    st.pyplot(pie_data.set_index("Property").plot.pie(y="Users", autopct='%1.1f%%').figure)

st.divider()

# ======================
# LINE CHARTS
# ======================
st.subheader("Performance Trends")

dates = pd.date_range(start="2024-02-01", periods=100)

def generate_series(base):
    return base + np.random.randn(100) * base * 0.05

chart1, chart2, chart3, chart4 = st.columns(4)

with chart1:
    st.caption("Sessions")
    df = pd.DataFrame({
        "Date": dates,
        "GA Property 1": generate_series(300000),
        "GA Property 2": generate_series(250000)
    })
    st.line_chart(df.set_index("Date"))

with chart2:
    st.caption("Total users")
    df = pd.DataFrame({
        "Date": dates,
        "GA Property 1": generate_series(200000),
        "GA Property 2": generate_series(150000)
    })
    st.line_chart(df.set_index("Date"))

with chart3:
    st.caption("New users")
    df = pd.DataFrame({
        "Date": dates,
        "GA Property 1": generate_series(120000),
        "GA Property 2": generate_series(80000)
    })
    st.line_chart(df.set_index("Date"))

with chart4:
    st.caption("Conversions")
    df = pd.DataFrame({
        "Date": dates,
        "GA Property 1": generate_series(700000),
        "GA Property 2": generate_series(600000)
    })
    st.line_chart(df.set_index("Date"))
