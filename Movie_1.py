import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Mini Netflix - Rotten", layout="wide")

# ---------------------------
# 🎨 Netflix Theme CSS
# ---------------------------
st.markdown("""
<style>
body {
    background-color: #141414;
}
.stApp {
    background-color: #141414;
    color: white;
}
h1, h2, h3 {
    color: #E50914;
}
.stButton>button {
    background-color: #E50914;
    color: white;
    border-radius: 8px;
}
.stButton>button:hover {
    background-color: #b20710;
}
.css-1d391kg {background-color:#000000;}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# โหลดข้อมูล
# ---------------------------
@st.cache_data
def load_data(uploaded_file):
    df = pd.read_csv(uploaded_file)
    df = df.dropna(subset=["title"])
    return df

# ---------------------------
# Session
# ---------------------------
if "watchlist" not in st.session_state:
    st.session_state.watchlist = []

if "page" not in st.session_state:
    st.session_state.page = "Home"

# ---------------------------
# Sidebar
# ---------------------------
st.sidebar.title("🎬 Mini Netflix")

if st.sidebar.button("🏠 Home"):
    st.session_state.page = "Home"

if st.sidebar.button("❤️ My Watchlist"):
    st.session_state.page = "Watchlist"

if st.sidebar.button("🗑 Clear Watchlist"):
    st.session_state.watchlist = []

uploaded_file = st.sidebar.file_uploader("Upload rotten_tomatoes_movies.csv", type=["csv"])

search = st.sidebar.text_input("🔎 Search")

# ---------------------------
# Functions
# ---------------------------
def toggle_watchlist(movie_id):
    if movie_id in st.session_state.watchlist:
        st.session_state.watchlist.remove(movie_id)
    else:
        st.session_state.watchlist.append(movie_id)

def show_movies(df):
    cols = st.columns(5)

    for i, row in df.iterrows():
        with cols[i % 5]:

            if "poster" in df.columns and pd.notna(row.get("poster")):
                st.image(row["poster"])
            else:
                st.image("https://via.placeholder.com/300x450?text=No+Image")

            st.markdown(f"**{row['title']} ({row.get('year','')})**")
            st.markdown(f"⭐ Rating: {row.get('rating','N/A')}")

            movie_id = row['title'] + str(row.get('year',""))

            if movie_id in st.session_state.watchlist:
                if st.button("Remove ❤️", key=f"r_{movie_id}_{i}"):
                    toggle_watchlist(movie_id)
            else:
                if st.button("Add ❤️", key=f"a_{movie_id}_{i}"):
                    toggle_watchlist(movie_id)

# ---------------------------
# UI
# ---------------------------
st.title("🔥 Mini Netflix - Rotten Tomatoes")

if uploaded_file is not None:

    df = load_data(uploaded_file)

    # แปลง rating เป็นตัวเลข
    if "rating" in df.columns:
        df["rating"] = pd.to_numeric(df["rating"], errors="coerce")

    # ---------------------------
    # 🎭 Genre Filter
    # ---------------------------
    if "genre" in df.columns:
        all_genres = (
            df["genre"]
            .dropna()
            .str.split(",")
            .explode()
            .str.strip()
            .unique()
        )
        selected_genre = st.sidebar.selectbox("🎭 Filter by Genre", ["All"] + sorted(all_genres))
    else:
        selected_genre = "All"

    if st.session_state.page == "Home":

        filtered = df

        # 🔎 Search
        if search:
            filtered = filtered[filtered["title"].str.contains(search, case=False, na=False)]

        # 🎭 Filter Genre
        if selected_genre != "All":
            filtered = filtered[filtered["genre"].str.contains(selected_genre, na=False)]

        # ⭐ Sort by Rating (มาก → น้อย)
        if "rating" in filtered.columns:
            filtered = filtered.sort_values(by="rating", ascending=False)

        show_movies(filtered.head(50))

    elif st.session_state.page == "Watchlist":

        st.header("❤️ My Watchlist")

        if not st.session_state.watchlist:
            st.info("ยังไม่มีหนังใน Watchlist")
        else:
            watch_df = df[
                (df["title"] + df.get("year","").astype(str))
                .isin(st.session_state.watchlist)
            ]

            if "rating" in watch_df.columns:
                watch_df = watch_df.sort_values(by="rating", ascending=False)

            show_movies(watch_df)

else:
    st.info("📂 กรุณาอัปโหลดไฟล์ rotten_tomatoes_movies.csv ก่อน")
