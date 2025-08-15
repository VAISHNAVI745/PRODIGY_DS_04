import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------
# Page Config & Custom Styling
# ----------------------------
st.set_page_config(page_title="Twitter Sentiment Analysis", layout="wide")

# Dark mode custom CSS
st.markdown("""
    <style>
        .stApp {
            background-color: #0E1117;
            color: white;
        }
        h1, h2, h3, h4, h5, h6 {
            color: white;
        }
        .css-1d391kg {
            background-color: #0E1117;
        }
        .css-18e3th9 {
            background-color: #0E1117;
        }
    </style>
""", unsafe_allow_html=True)

# ----------------------------
# Title
# ----------------------------
st.markdown("<h1 style='text-align: center; color: #00BFFF;'>🐦 Twitter Sentiment Analysis</h1>", unsafe_allow_html=True)
st.markdown("---")

# ----------------------------
# Load Dataset
# ----------------------------
df = pd.read_csv("data/twitter_training.csv", header=None)
df.columns = ["ID", "Brand", "Sentiment", "Tweet"]
df["Sentiment"] = df["Sentiment"].str.capitalize()

# ----------------------------
# Sidebar Filters
# ----------------------------
with st.sidebar:
    st.header("🔍 Filters")
    brand_options = ["All"] + sorted(df["Brand"].unique().tolist())
    selected_brand = st.selectbox("Select Brand", brand_options)

    sentiment_options = ["Positive", "Negative", "Neutral", "Irrelevant"]
    selected_sentiments = st.multiselect("Select Sentiment(s)", sentiment_options, default=sentiment_options)

# ----------------------------
# Filtered Data
# ----------------------------
filtered_df = df.copy()
if selected_brand != "All":
    filtered_df = filtered_df[filtered_df["Brand"] == selected_brand]
filtered_df = filtered_df[filtered_df["Sentiment"].isin(selected_sentiments)]

# ----------------------------
# Row 1: Brand and Sentiment Counts
# ----------------------------
col1, col2 = st.columns(2)

with col1:
    brand_counts = df["Brand"].value_counts().reset_index()
    brand_counts.columns = ["Brand", "Count"]
    fig1 = px.bar(
        brand_counts, x="Brand", y="Count", title="📊 Count of Tweets by Brand",
        color_discrete_sequence=["#00BFFF"], template="plotly_dark"
    )
    fig1.update_layout(xaxis_title="Brand", yaxis_title="Count")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    sentiment_counts = df.groupby(["Brand", "Sentiment"]).size().reset_index(name="Count")
    fig2 = px.bar(
        sentiment_counts, x="Brand", y="Count", color="Sentiment",
        title="📊 Tweets by Brand & Sentiment",
        color_discrete_map={
            "Positive": "#32CD32",     # Lime Green
            "Negative": "#FF4500",     # Orange Red
            "Neutral": "#FFD700",      # Gold
            "Irrelevant": "#1E90FF"    # Dodger Blue
        },
        template="plotly_dark"
    )
    fig2.update_layout(xaxis_title="Brand", yaxis_title="Count")
    st.plotly_chart(fig2, use_container_width=True)

# ----------------------------
# Row 2: Data Table & Donut Chart
# ----------------------------
col3, col4 = st.columns([2, 1])

with col3:
    st.subheader("📋 Filtered Tweets")
    st.dataframe(
        filtered_df[["Brand", "Sentiment", "Tweet"]],
        use_container_width=True,
        height=400
    )

with col4:
    pie_data = df["Sentiment"].value_counts().reset_index()
    pie_data.columns = ["Sentiment", "Count"]
    fig3 = px.pie(
        pie_data, names="Sentiment", values="Count",
        title="🧁 Sentiment Proportion",
        hole=0.4,
        color_discrete_map={
            "Positive": "#32CD32",
            "Negative": "#FF4500",
            "Neutral": "#FFD700",
            "Irrelevant": "#1E90FF"
        },
        template="plotly_dark"
    )
    st.plotly_chart(fig3, use_container_width=True)

# ----------------------------
# Footer
# ----------------------------
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: white;'>Built by Prodigy InfoTech | Data Science Internship Task 4</p>",
    unsafe_allow_html=True
)
