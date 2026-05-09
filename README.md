# MovieRecommendation
Develop a Movie Recommendation system that would suggest top 5 movies based on user input.
# 🎬 Movie Recommendation System

A **content-based movie recommendation system** that suggests similar movies using NLP techniques  built with Python, Streamlit, and the TMDB API.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red?style=flat-square&logo=streamlit)
![scikit-learn](https://img.shields.io/badge/scikit--learn-TF--IDF-orange?style=flat-square&logo=scikit-learn)
![TMDB](https://img.shields.io/badge/TMDB-API-green?style=flat-square)

---

## Features

- Search from a dataset of 45,000+ movies
- Get 5 content-based recommendations instantly
- Live movie posters fetched from TMDB API
- Click any poster to open the TMDB movie page
- Pre-computed similarity matrix for fast results
- Clean cinematic dark UI

---

## Demo

> Select a movie → Click **Recommend** → Get 5 similar movies with posters

---

## How It Works

The system recommends movies based on **content similarity**  not ratings or user behaviour. It analyses:

- Movie genres
- Plot keywords
- Overview / synopsis
- Cast members
- Crew (director, etc.)

These features are combined into a single text "tag" per movie, which is then vectorized and compared using cosine similarity.

---

## Technical Pipeline

### 1. Data Preprocessing

Raw metadata from the [TMDB Movies Dataset](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset) is cleaned and merged:

```python
df['tags'] = df['overview'] + df['genres'] + df['keywords'] + df['cast'] + df['crew']
df['tags'] = df['tags'].apply(lambda x: x.lower().replace(" ", ""))
```

---

### 2. Vectorization with TF-IDF

Text tags are converted into numerical vectors using **TF-IDF (Term Frequency–Inverse Document Frequency)**.

**Why TF-IDF over Count Vectorizer?**

| Feature | Count Vectorizer | TF-IDF |
|---|---|---|
| Counts word occurrences | ✅ | ✅ |
| Penalises common words (`the`, `is`) | ❌ | ✅ |
| Rewards meaningful/rare words | ❌ | ✅ |
| Better recommendation accuracy | ❌ | ✅ |

```python
from sklearn.feature_extraction.text import TfidfVectorizer

tfidf = TfidfVectorizer(max_features=50000, ngram_range=(1,2), stop_words='english')
vectorized_data = tfidf.fit_transform(df['tags'])
```

**TF-IDF Formula:**

```
TF-IDF(t, d) = TF(t, d) × log(N / df(t))
```

Where `t` = term, `d` = document, `N` = total documents, `df(t)` = documents containing term `t`.

---

### 3. Cosine Similarity

After vectorization, the **similarity between every pair of movies** is computed and stored in a matrix.

```
similarity(A, B) = (A · B) / (|A| × |B|)
```

- Result ranges from **0** (completely different) to **1** (identical)
- Higher angle → lower similarity
- Lower angle → higher similarity

```python
from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity(vectorized_data)
```

---

### 4. Recommendation Logic

```python
def recommend(movie):
    movie_index = df[df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    return [(df.iloc[i[0]].title, df.iloc[i[0]].id) for i in movie_list]
```

---

### 5. TMDB Poster Fetching

Movie posters are fetched live from the TMDB API using the movie's TMDB ID. A title-search fallback is used if the stored ID is stale:

```
https://image.tmdb.org/t/p/w500/<poster_path>
```

---

## System Workflow

```
User selects a movie
        ↓
Look up movie index in DataFrame
        ↓
Fetch row from precomputed similarity matrix
        ↓
Sort by score → pick top 5 (excluding self)
        ↓
For each result: call TMDB API → fetch poster bytes
        ↓
Render cards with st.image() + TMDB link
```

---

## Project Structure

```
movie-recommender/
│
├── Main.py                  # Streamlit frontend
├── MovieRecommendation.ipynb  # Data preprocessing & model building
├── movies_dict.pkl         # Serialised movies DataFrame
├── similarity.pkl          # Precomputed cosine similarity matrix
├── requirements.txt        # Python dependencies
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.8+
- A free [TMDB API key](https://www.themoviedb.org/settings/api)
- The [TMDB Movies Dataset](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset) (for re-training)

---

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/movie-recommender.git
cd movie-recommender
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Generate Pickle Files *(skip if already present)*

Run all cells in `MovieRecommendation.ipynb`. This will create:
- `movies_dict.pkl`
- `similarity.pkl`

### 4. Run the App

```bash
streamlit run Main.py
```

### 5. Enter Your TMDB API Key

Open the **Settings** panel in the left sidebar and paste your TMDB v3 API key. Posters will load automatically.

---

## Requirements

```
streamlit
pandas
scikit-learn
requests
pickle5
numpy
```

Install all at once:

```bash
pip install streamlit pandas scikit-learn requests numpy
```

---

## Getting a TMDB API Key

1. Create a free account at [themoviedb.org](https://www.themoviedb.org)
2. Go to **Settings → API**
3. Request an API key (choose "Developer")
4. Copy your **API Read Access Token (v3)**

---

## Dataset

**Source:** [The Movies Dataset  Kaggle](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset)

| Property | Value |
|---|---|
| Total movies | ~45,000 |
| Features used | title, genres, keywords, overview, cast, crew, id |
| Vectorizer | TF-IDF (`max_features=50000`, `ngram_range=(1,2)`) |
| Similarity metric | Cosine Similarity |

---

## FAQ

**Q: Why are some posters not showing?**  
A: Make sure your TMDB API key is entered . For older/obscure movies, the system falls back to a title search to find the poster.

**Q: Can I add more movies?**  
A: Yes  add rows to the dataset and re-run the notebook to regenerate the pickle files.

**Q: Why is the first load slow?**  
A: The `similarity.pkl` matrix (~45k × 45k) takes a moment to load into memory. Subsequent runs use Streamlit's cache so it stays fast.

---

## License

This project is for educational purposes. Movie data and posters are provided by [TMDB](https://www.themoviedb.org). This product uses the TMDB API but is not endorsed or certified by TMDB.
