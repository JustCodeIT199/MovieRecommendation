import streamlit as st
import pickle
import pandas as pd
import requests

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title=" Movie Recommendation System",
    page_icon="🎬",
    layout="wide",
)

# ─────────────────────────────────────────────
# CUSTOM CSS  — refined dark theme (fixed)
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* ═══════════════════════════════════════════
   1. GLOBAL CANVAS
═══════════════════════════════════════════ */
.stApp {
    background-color: #111318 !important;
}
section[data-testid="stMain"],
.main .block-container {
    background-color: #111318 !important;
    padding-top: 2.5rem;
}
/* kill any residual white panels */
[data-testid="stAppViewContainer"],
[data-testid="stHeader"] {
    background-color: #111318 !important;
}

/* ═══════════════════════════════════════════
   2. BASE TEXT
═══════════════════════════════════════════ */
html, body,
p, span, label, div,
[class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    color: #d4cfc8 !important;
}

/* ═══════════════════════════════════════════
   3. HERO
═══════════════════════════════════════════ */
.hero-title {
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: clamp(2.4rem, 5vw, 4rem);
    letter-spacing: 0.07em;
    background: linear-gradient(90deg, #c9922a 0%, #f0d090 50%, #c9922a 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-align: center;
    margin-bottom: 0.2rem;
    line-height: 1.1;
}
.hero-sub {
    text-align: center;
    color: #6b6560 !important;
    font-size: 0.82rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    margin-top: 0;
    margin-bottom: 2.5rem;
}

/* ═══════════════════════════════════════════
   4. SEARCH PANEL
═══════════════════════════════════════════ */
.search-container {
    background: #1a1d24;
    border: 1px solid #2c2f38;
    border-radius: 14px;
    padding: 1.8rem 2rem 1.4rem;
    margin-bottom: 2rem;
    box-shadow: 0 4px 24px rgba(0,0,0,0.45);
}

/* ═══════════════════════════════════════════
   5. SELECTBOX  — the tricky bit
   Target every layer BaseWeb renders
═══════════════════════════════════════════ */

/* outer wrapper */
div[data-baseweb="select"] {
    background-color: #22252e !important;
    border-radius: 8px !important;
}

/* the visible control box */
div[data-baseweb="select"] > div:first-child {
    background-color: #22252e !important;
    border: 1.5px solid #3d4050 !important;
    border-radius: 8px !important;
    min-height: 44px !important;
}
div[data-baseweb="select"] > div:first-child:hover {
    border-color: #c9922a !important;
}

/* the selected-value text */
div[data-baseweb="select"] [data-testid="stSelectboxContainer"] span,
div[data-baseweb="select"] div[class*="singleValue"],
div[data-baseweb="select"] div[class*="placeholder"],
div[data-baseweb="select"] input {
    color: #e8e2d8 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
}

/* dropdown arrow icon */
div[data-baseweb="select"] svg {
    fill: #c9922a !important;
}

/* the dropdown list popup */
ul[data-baseweb="menu"],
div[data-baseweb="popover"] ul,
div[data-baseweb="menu"] {
    background-color: #1e2028 !important;
    border: 1px solid #2c2f38 !important;
    border-radius: 8px !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.6) !important;
}

/* each list item */
ul[data-baseweb="menu"] li,
div[data-baseweb="menu"] li {
    background-color: #1e2028 !important;
    color: #d4cfc8 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
}
ul[data-baseweb="menu"] li:hover,
div[data-baseweb="menu"] li:hover,
ul[data-baseweb="menu"] li[aria-selected="true"],
div[data-baseweb="menu"] li[aria-selected="true"] {
    background-color: #2d3040 !important;
    color: #f0d090 !important;
}

/* Streamlit's own selectbox label */
.stSelectbox label {
    color: #6b6560 !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.08em !important;
}

/* ═══════════════════════════════════════════
   6. BUTTON
═══════════════════════════════════════════ */
div.stButton > button {
    background: linear-gradient(135deg, #b07820 0%, #e8b86d 100%) !important;
    color: #111318 !important;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1.05rem !important;
    letter-spacing: 0.14em !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.6rem 1.5rem !important;
    height: 44px !important;
    cursor: pointer !important;
    transition: filter 0.2s, transform 0.15s !important;
    width: 100% !important;
}
div.stButton > button:hover {
    filter: brightness(1.12) !important;
    transform: translateY(-2px) !important;
}
div.stButton > button:active {
    transform: translateY(0) !important;
}

/* ═══════════════════════════════════════════
   7. MOVIE CARDS
═══════════════════════════════════════════ */
.movie-card {
    background: #1a1d24;
    border: 1px solid #2c2f38;
    border-radius: 12px;
    overflow: hidden;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}
.movie-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 16px 40px rgba(201,146,42,0.22);
}
.movie-card img {
    width: 100%;
    display: block;
    aspect-ratio: 2/3;
    object-fit: cover;
}
.movie-card-body {
    padding: 0.75rem 0.9rem 0.9rem;
    background: #1a1d24;
}
.movie-card-rank {
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 0.78rem;
    letter-spacing: 0.18em;
    color: #c9922a !important;
    margin-bottom: 0.25rem;
}
.movie-card-title {
    font-size: 0.88rem;
    font-weight: 500;
    color: #e0dbd2 !important;
    line-height: 1.4;
}
.movie-card-tmdb {
    font-size: 0.75rem;
    color: #c9922a !important;
    margin-top: 0.4rem;
    letter-spacing: 0.04em;
    opacity: 0.8;
    transition: opacity 0.2s;
}
.movie-card:hover .movie-card-tmdb {
    opacity: 1;
}
.movie-card-fallback {
    background: #22252e;
    width: 100%;
    aspect-ratio: 2/3;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 3rem;
}

/* ═══════════════════════════════════════════
   8. MISC UI
═══════════════════════════════════════════ */
.gold-divider {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent 0%, #c9922a 40%, #c9922a 60%, transparent 100%);
    margin: 1.8rem 0;
    opacity: 0.5;
}
.section-label {
    color: #6b6560 !important;
    font-size: 0.8rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
}
.err-box {
    background: #1f1518;
    border: 1px solid #5a2020;
    border-radius: 8px;
    padding: 0.9rem 1.4rem;
    color: #e07070 !important;
    font-size: 0.9rem;
}
.info-box {
    background: #141a22;
    border: 1px solid #1e3a55;
    border-radius: 8px;
    padding: 0.9rem 1.4rem;
    color: #70b0d8 !important;
    font-size: 0.9rem;
}
.footer {
    text-align: center;
    color: #333640 !important;
    font-size: 0.75rem;
    margin-top: 3rem;
    letter-spacing: 0.08em;
}

/* hide Streamlit's default top toolbar / hamburger clutter */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# CONSTANTS  — replace with your real key
# ─────────────────────────────────────────────
TMDB_API_KEY     = "Your_TMDB_API_Key_Here"  # ← REPLACE with your TMDB API key
TMDB_POSTER_BASE = "https://image.tmdb.org/t/p/w500"
TMDB_API_BASE    = "https://api.themoviedb.org/3"
TMDB_MOVIE_PAGE  = "https://www.themoviedb.org/movie"


# ─────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_data():
    """Load pickled movies dict and similarity matrix."""
    movies = pd.DataFrame(pickle.load(open("movies_dict.pkl", "rb")))
    similarity = pickle.load(open("similarity.pkl", "rb"))
    return movies, similarity


# ─────────────────────────────────────────────
# CORE FUNCTIONS
# ─────────────────────────────────────────────
def fetch_poster_and_id(movie_title: str, tmdb_id: int) -> tuple:
    """
    Try two strategies to get a poster + confirmed TMDB id:
      1. Direct lookup by numeric TMDB id  (fast, works when dataset id is valid)
      2. Search by title                   (fallback when id is stale / invalid)
    Returns (poster_url | None, confirmed_tmdb_id | None)
    """
    confirmed_id = None
    poster_url   = None

    # ── Strategy 2: title search fallback ─────────────────────
    if not poster_url:
        try:
            resp = requests.get(
                f"{TMDB_API_BASE}/search/movie",
                params={
                    "api_key": TMDB_API_KEY,
                    "query": movie_title,
                    "language": "en-US",
                    "page": 1,
                },
                timeout=6,
            )
            if resp.status_code == 200:
                results = resp.json().get("results", [])
                if results:
                    best = results[0]
                    path = best.get("poster_path")
                    if path:
                        poster_url = f"{TMDB_POSTER_BASE}{path}"
                    confirmed_id = best.get("id")
        except Exception:
            pass

    return poster_url, confirmed_id


def recommend(movie_name: str, movies: pd.DataFrame, similarity) -> list[dict]:
    """
    Return a list of 5 dicts: {title, movie_id}
    based on cosine-similarity ranking.
    Raises ValueError if movie is not found.
    """
    matches = movies[movies["title"] == movie_name]
    if matches.empty:
        raise ValueError(f'Movie "{movie_name}" not found in the dataset.')

    movie_index = matches.index[0]
    distances = similarity[movie_index]
    movie_list = sorted(
        enumerate(distances), key=lambda x: x[1], reverse=True
    )[1:6]

    recommendations = []
    for idx, _ in movie_list:
        row = movies.iloc[idx]
        raw_id = row.get("id", 0)
        try:
            mid = int(float(str(raw_id)))
        except (ValueError, TypeError):
            mid = 0
        recommendations.append({"title": row["title"], "movie_id": mid})
    return recommendations


# ─────────────────────────────────────────────
# APP LAYOUT
# ─────────────────────────────────────────────
# Hero
st.markdown('<h1 class="hero-title">🎬 Movie Recommendation System</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-sub">Discover films you\'ll love — powered by content similarity</p>', unsafe_allow_html=True)

# Load data
try:
    movies_df, similarity_matrix = load_data()
    movie_titles = sorted(movies_df["title"].dropna().unique().tolist())
except FileNotFoundError as e:
    st.markdown(
        f'<div class="err-box">⚠️ Could not load data files: <code>{e}</code><br>'
        'Make sure <b>movies_dict.pkl</b> and <b>similarity.pkl</b> are in the same directory as app.py.</div>',
        unsafe_allow_html=True,
    )
    st.stop()

# Search panel
with st.container():
    st.markdown('<div class="search-container">', unsafe_allow_html=True)

    col_select, col_btn = st.columns([4, 1], gap="medium")

    with col_select:
        selected_movie = st.selectbox(
            "Search for a movie",
            options=[""] + movie_titles,
            index=0,
            placeholder="Type or select a movie title…",
            label_visibility="collapsed",
        )

    with col_btn:
        recommend_clicked = st.button("▶  RECOMMEND", use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

# Results
if recommend_clicked:
    if not selected_movie:
        st.markdown(
            '<div class="info-box">ℹ️ Please select a movie from the dropdown first.</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)
        st.markdown(
            f'<p style="color:#8a8070;font-size:0.85rem;letter-spacing:0.15em;'
            f'text-transform:uppercase;margin-bottom:1.2rem;">'
            f'Because you liked &nbsp;<strong style="color:#e8b86d">{selected_movie}</strong></p>',
            unsafe_allow_html=True,
        )

        with st.spinner("Finding your next watch…"):
            try:
                recs = recommend(selected_movie, movies_df, similarity_matrix)
            except ValueError as ve:
                st.markdown(f'<div class="err-box">⚠️ {ve}</div>', unsafe_allow_html=True)
                st.stop()

            # Fetch posters + confirmed TMDB ids for all 5 recommendations
            poster_data = [
                fetch_poster_and_id(rec["title"], rec["movie_id"])
                for rec in recs
            ]

        # Render cards
        cols = st.columns(5, gap="medium")
        for i, (col, rec, (poster_url, confirmed_id)) in enumerate(
            zip(cols, recs, poster_data)
        ):
            with col:
                tmdb_url = (
                    f"{TMDB_MOVIE_PAGE}/{confirmed_id}"
                    if confirmed_id
                    else f"https://www.themoviedb.org/search?query={requests.utils.quote(rec['title'])}"
                )

                img_html = (
                    f'<img src="{poster_url}" alt="{rec["title"]} poster" '
                    f'style="width:100%;display:block;aspect-ratio:2/3;object-fit:cover;">'
                    if poster_url
                    else '<div class="movie-card-fallback">🎞️</div>'
                )

                card_html = f"""
                <a href="{tmdb_url}" target="_blank" rel="noopener noreferrer"
                   style="text-decoration:none;">
                  <div class="movie-card">
                    {img_html}
                    <div class="movie-card-body">
                      <div class="movie-card-rank">PICK #{i+1}</div>
                      <div class="movie-card-title">{rec["title"]}</div>
                      <div class="movie-card-tmdb">View on TMDB →</div>
                    </div>
                  </div>
                </a>
                """
                st.markdown(card_html, unsafe_allow_html=True)

# Footer
st.markdown(
    '<p class="footer">Powered by TF-IDF · Cosine Similarity · TMDB API</p>',
    unsafe_allow_html=True,
)