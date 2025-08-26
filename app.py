import pandas as pd
import streamlit as st

# --- Data Loading ---
# The correct way to load a CSV file from GitHub is to use the raw URL.
# This URL has been updated with the one you provided.
url = "https://raw.githubusercontent.com/garemagaba/Analyze-Best-Selling-Amazon-Books-GaremaGaba/refs/heads/main/bestsellers.csv"

try:
    df = pd.read_csv(url)
except Exception as e:
    st.error(f"Error loading the dataset: {e}. Please ensure the URL is a raw file link.")
    st.stop()

# --- Data Cleaning and Preprocessing ---
# Strip whitespace from column names to prevent errors.
df.columns = df.columns.str.strip()

# Rename columns for clarity.
df.rename(columns={
    "Name": "Title",
    "Year": "Publication Year",
    "User Rating": "Rating" # Correcting the column name to match the dataset
}, inplace=True)

# Drop any duplicate rows to ensure data integrity.
df.drop_duplicates(inplace=True)

# --- Streamlit App UI ---

# Set the title of the Streamlit app.
st.title("Amazon Best Sellers Analysis (2009-2019)")

# Sidebar for controls
st.sidebar.title("App Controls")

# Placeholder for sidebar image.
# Using the URL provided by the user.
sidebar_image_url = "https://static.vecteezy.com/system/resources/thumbnails/066/027/770/small/many-books-are-flying-in-a-library-photo.jpg"
st.sidebar.image(sidebar_image_url, use_container_width=True)

# --- Slicers (Selectboxes) for user interaction ---

# Slicer for selecting a genre. The "All" option allows users to see both genres.
selected_genre = st.sidebar.selectbox(
    "Select a Genre:",
    options=["All"] + list(df['Genre'].unique())
)

# Slicer for selecting a specific author.
# The list of authors is dynamic and depends on the selected genre.
if selected_genre == "All":
    authors_in_genre = sorted(list(df['Author'].unique()))
else:
    authors_in_genre = sorted(list(df[df['Genre'] == selected_genre]['Author'].unique()))

selected_author = st.sidebar.selectbox(
    "Select an Author:",
    options=["All"] + authors_in_genre
)

# Slicer for selecting a year range.
year_range = st.sidebar.slider(
    "Select a Year Range:",
    min_value=int(df['Publication Year'].min()),
    max_value=int(df['Publication Year'].max()),
    value=(int(df['Publication Year'].min()), int(df['Publication Year'].max()))
)

# --- Data Filtering based on slicers ---

# Filter the dataframe based on the selected genre.
filtered_df = df
if selected_genre != "All":
    filtered_df = filtered_df[filtered_df['Genre'] == selected_genre]

# Filter the dataframe based on the selected author.
if selected_author != "All":
    filtered_df = filtered_df[filtered_df['Author'] == selected_author]

# Filter the dataframe based on the selected year range.
filtered_df = filtered_df[
    (filtered_df['Publication Year'] >= year_range[0]) &
    (filtered_df['Publication Year'] <= year_range[1])
]

# --- Main Page Content (Dynamically updated) ---

st.header("Overview")
st.write(f"Showing best sellers for **{selected_genre}** genre by **{selected_author}** from **{year_range[0]}** to **{year_range[1]}**.")
st.write(filtered_df.head(10))

# --- Charts and Analysis ---

if not filtered_df.empty:
    st.subheader("Top Authors by Book Count")
    # Using value_counts() to get the count of books for each author, then plotting the top 10.
    author_counts = filtered_df['Author'].value_counts().head(10)
    st.bar_chart(author_counts)

    st.subheader("Average Ratings by Genre")
    # Grouping the filtered data by genre to calculate the average rating.
    avg_rating_by_genre = filtered_df.groupby("Genre")["Rating"].mean()
    st.bar_chart(avg_rating_by_genre)

    st.subheader("Average Price by Genre")
    # Grouping the filtered data by genre to calculate the average price.
    avg_price_by_genre = filtered_df.groupby("Genre")["Price"].mean()
    st.bar_chart(avg_price_by_genre)
else:
    st.warning("No data available for the selected filters. Please adjust your selections.")

# Placeholder for main page image.
# Using the URL provided by the user.
main_image_url = "https://images.stockcake.com/public/6/1/7/617f8768-68bc-4c72-84ea-d426b5624796_large/books-and-blooms-stockcake.jpg"
st.image(main_image_url, use_container_width=True)
