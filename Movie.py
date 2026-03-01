import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Movie Review", layout="wide")

API_KEY = "86f6075c"

# ---------------- CSS ----------------
st.markdown("""
<style>
.stApp { background-color: #0f172a; }
h1 { color: #f8fafc; font-weight:600; }
body, p, div { color: #e2e8f0; }

.notice {
    background: linear-gradient(135deg,#b8860b,#d4af37);
    color:#1a1a1a;
    padding:15px;
    border-radius:10px;
    margin-bottom:20px;
    font-size:14px;
}

.movie-title {
    font-size:17px;
    font-weight:600;
    margin-top:10px;
    min-height:45px;
}

.rating {
    color:#facc15;
    font-size:15px;
    margin-bottom:30px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- Notice ----------------
st.markdown("""
<div class="notice">
เว็บไซต์นี้จัดทำขึ้นเพื่อการศึกษาเท่านั้น ไม่ได้มีวัตถุประสงค์เพื่อการพาณิชย์<br>
This website is created for educational purposes only and not for commercial use.
</div>
""", unsafe_allow_html=True)

st.title("🎬 Movie Review Website")

# ---------------- Load CSV ----------------
df = pd.read_csv("movie.csv")

# แปลงคะแนน
df["Score"] = df["Critics' Score"].replace("No rating", "-")

df["Score_clean"] = (
    df["Score"]
    .replace("-", None)
    .str.replace("%","",regex=False)
)

df["Score_clean"] = pd.to_numeric(df["Score_clean"], errors="coerce")

# ---------------- ดาว ----------------
def make_stars(score):
    if pd.isna(score):
        return "-"
    return "⭐" * round(score / 20)

# ---------------- Cache Poster ----------------
@st.cache_data(show_spinner=False)
def get_poster(title):
    try:
        url = f"https://www.omdbapi.com/?t={title}&apikey={API_KEY}"
        res = requests.get(url, timeout=5).json()
        if res.get("Response") == "True":
            return res.get("Poster")
    except:
        pass
    return None

# ---------------- Search ----------------
search = st.text_input("🔎 ค้นหาชื่อภาพยนตร์")

if search:
    filtered = df[df["Title"].str.contains(search, case=False, na=False)]
else:
    filtered = df

# ---------------- No result ----------------
if search and filtered.empty:
    st.warning("ไม่พบภาพยนตร์ที่ตรงกับคำค้นหา")

    if st.button("⬅ กลับหน้าหลัก"):
        st.rerun()

# ---------------- Show movies ----------------
else:

    if search:
        if st.button("⬅ กลับหน้าหลัก"):
            st.rerun()

    cols = st.columns(4)

    for i, row in enumerate(filtered.itertuples()):

        with cols[i % 4]:

            st.markdown(
                f"<div class='movie-title'>{row.Title}</div>",
                unsafe_allow_html=True
            )

            poster = get_poster(row.Title)

            if poster and poster != "N/A":
                st.image(poster, width=230)
            else:
                st.image("https://via.placeholder.com/300x450?text=No+Image", width=230)

            if row.Score == "-":
                st.markdown("<div class='rating'>-</div>", unsafe_allow_html=True)
            else:
                stars = make_stars(row.Score_clean)
                st.markdown(
                    f"<div class='rating'>{stars} {row.Score}</div>",
                    unsafe_allow_html=True
                )
