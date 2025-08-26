import pandas as pd
import streamlit as st

url = "https://raw.githubusercontent.com/garemagaba/Analyze-Best-Selling-Amazon-Books-GaremaGaba/refs/heads/main/bestsellers.csv"

try:
    df = pd.read_csv(url)
except Exception as e:
    st.error(f"Error loading the dataset: {e}. Please ensure the URL is a raw file link.")
    st.stop()

df.columns = df.columns.str.strip()

df.rename(columns={
    "Name": "Title",
    "Year": "Publication Year",
    "User Rating": "Rating"
}, inplace=True)

df.drop_duplicates(inplace=True)

st.title("Amazon Best Sellers Analysis (2009-2019)")

st.sidebar.title("App Controls")

sidebar_image_url = "https://static.vecteezy.com/system/resources/thumbnails/066/027/770/small/many-books-are-flying-in-a-library-photo.jpg"
st.sidebar.image(sidebar_image_url, use_container_width=True)

selected_genre = st.sidebar.selectbox(
    "Select a Genre:",
    options=["All"] + list(df['Genre'].unique())
)

if selected_genre == "All":
    authors_in_genre = sorted(list(df['Author'].unique()))
else:
    authors_in_genre = sorted(list(df[df['Genre'] == selected_genre]['Author'].unique()))

selected_author = st.sidebar.selectbox(
    "Select an Author:",
    options=["All"] + authors_in_genre
)

year_range = st.sidebar.slider(
    "Select a Year Range:",
    min_value=int(df['Publication Year'].min()),
    max_value=int(df['Publication Year'].max()),
    value=(int(df['Publication Year'].min()), int(df['Publication Year'].max()))
)

filtered_df = df
if selected_genre != "All":
    filtered_df = filtered_df[filtered_df['Genre'] == selected_genre]

if selected_author != "All":
    filtered_df = filtered_df[filtered_df['Author'] == selected_author]

filtered_df = filtered_df[
    (filtered_df['Publication Year'] >= year_range[0]) &
    (filtered_df['Publication Year'] <= year_range[1])
]

st.header("Overview")
st.write(f"Showing best sellers for **{selected_genre}** genre by **{selected_author}** from **{year_range[0]}** to **{year_range[1]}**.")
st.write(filtered_df.head(10))

if not filtered_df.empty:
    st.subheader("Top Authors by Book Count")
  
    author_counts = filtered_df['Author'].value_counts().head(10)
    st.bar_chart(author_counts)

    st.subheader("Average Ratings by Genre")
   
    avg_rating_by_genre = filtered_df.groupby("Genre")["Rating"].mean()
    st.bar_chart(avg_rating_by_genre)

    st.subheader("Average Price by Genre")
 
    avg_price_by_genre = filtered_df.groupby("Genre")["Price"].mean()
    st.bar_chart(avg_price_by_genre)
else:
    st.warning("No data available for the selected filters. Please adjust your selections.")

main_image_url = "https://images.stockcake.com/public/6/1/7/617f8768-68bc-4c72-84ea-d426b5624796_large/books-and-blooms-stockcake.jpg"
st.image(main_image_url, use_container_width=True)
