import streamlit as st
import requests
import pandas as pd

st.title("📺 Rotten Tomatoes Newest TV Series")

url = "https://www.rottentomatoes.com/napi/browse/tv_series_browse/sort:newest"
res = requests.get(url)

if res.status_code == 200:
    data = res.json()

    items = data.get("results", [])

    movies = []
    for item in items:
        title = item.get("title")
        year = item.get("year")
        score = item.get("tomatometerScore")
        poster = item.get("posterImageUrl")

        movies.append({
            "Title": title,
            "Year": year,
            "Score": score,
            "Poster": poster
        })

    df = pd.DataFrame(movies)

    st.dataframe(df)

    for m in movies:
        st.image(m["Poster"], width=150)
        st.write(f"**{m['Title']} ({m['Year']})**  ⭐ {m['Score']}")
        st.markdown("---")
else:
    st.error("ไม่สามารถดึงข้อมูลจาก Rotten Tomatoes ได้")
