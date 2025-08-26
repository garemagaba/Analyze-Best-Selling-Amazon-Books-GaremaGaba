import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# --------------------------
# Header + Intro
# --------------------------
st.header("📚 Amazon Book Analysis Dashboard")

st.markdown("""
This dashboard explores the **Amazon Bestsellers Dataset**.  
We’ll analyze trends in **ratings, reviews, price, and genres**.
""")

st.image("https://img.freepik.com/free-vector/hand-drawn-flat-design-stack-books_23-2149342941.jpg")

# --------------------------
# Load dataset
# --------------------------
url = "https://raw.githubusercontent.com/your-repo/books.csv"
df = pd.read_csv(url)

# --------------------------
# Tabs for Navigation
# --------------------------
tab1, tab2 = st.tabs(["📊 Overview", "📈 Visualizations"])

# --------------------------
# TAB 1: Overview
# --------------------------
with tab1:
    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    st.write("### Summary Statistics")
    st.write(df.describe())

# --------------------------
# TAB 2: Visualizations
# --------------------------
with tab2:
    st.subheader("Exploratory Visualizations")

    # Histogram of Ratings
    st.write("### ⭐ Rating Distribution")
    fig, ax = plt.subplots()
    sns.histplot(df['Rating'], kde=True, ax=ax, color="skyblue")
    st.pyplot(fig)

    # Scatterplot Price vs Rating
    st.write("### 💰 Price vs Rating")
    fig, ax = plt.subplots()
    sns.scatterplot(data=df, x="Price", y="Rating", hue="Genre", ax=ax)
    st.pyplot(fig)

    # Heatmap
    st.write("### 🔥 Correlation Heatmap")
    plt.figure(figsize=(6,4))
    sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm")
    st.pyplot(plt)

    # Pairplot
    st.write("### 🔗 Pairplot of Features")
    sns.pairplot(df[['Rating','Reviews','Price','Year']], hue="Genre", diag_kind="kde")
    st.pyplot(plt)
