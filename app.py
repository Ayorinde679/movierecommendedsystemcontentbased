import pickle
import streamlit as st
from pathlib import Path
import pandas as pd
import requests

st.header('Movie Recommender System')

BASE_DIR = Path(__file__).resolve().parent
PICKLE_DIR = BASE_DIR / "picklemodel"

movies = pickle.load(open(PICKLE_DIR / "movie_dict.pkl", "rb"))
similarity = pickle.load(open(PICKLE_DIR / "similarity.pkl", "rb"))

if isinstance(movies, dict):
    movies_df = pd.DataFrame(movies)
else:
    movies_df = movies

movie_list = movies_df['title'].values



selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)
def fetch_poster(movie_id):
    """Fetches the movie poster URL from TMDB API."""
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    try:
        data = requests.get(url)
        data.raise_for_status()  # Raise an exception for bad status codes
        data = data.json()
        poster_path = data.get('poster_path')
        if poster_path:
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_path
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching poster: {e}")
    # Return a placeholder if the poster is not found or an error occurs
    return "https://placehold.co/500x750/333/FFFFFF?text=No+Poster"

def recommend(movie):
    df = movies_df
    movie_index = df[df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = df.iloc[i[0]].movie_id
        recommended_movies.append(df.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster


if st.button('Recommend'):
    recommendations, recommended_movies_poster= recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommendations[0])
        st.image(recommended_movies_poster[0])
    with col2:
        st.text(recommendations[1])
        st.image(recommended_movies_poster[1])              
    with col3:
        st.text(recommendations[2])
        st.image(recommended_movies_poster[2])
    with col4:
        st.text(recommendations[3])
        st.image(recommended_movies_poster[3])
    with col5:
        st.text(recommendations[4])
        st.image(recommended_movies_poster[4])



