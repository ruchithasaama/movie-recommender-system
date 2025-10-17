import pickle
import streamlit as st
import requests
import pandas as pd
import time
import gdown
import os

# -------------------------------
# Download .pkl files if not exist
# -------------------------------
if not os.path.exists("movie_list.pkl"):
    url = "https://drive.google.com/uc?id=19B79AxM67gaJrZfWKvX_7LLXyAqvx7Lw"
    gdown.download(url, "movie_list.pkl", quiet=False)

if not os.path.exists("similarity.pkl"):
    url = "https://drive.google.com/uc?id=12kVDki1F0JqSKWWSvfT_nmgDjTJbWcJr"
    gdown.download(url, "similarity.pkl", quiet=False)

# -------------------------------
# Load data
# -------------------------------
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# -------------------------------
# Helper functions
# -------------------------------
def fetch_poster(movie_id, retries=3):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    for i in range(retries):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            poster_path = data.get('poster_path')
            if poster_path:
                return "https://image.tmdb.org/t/p/w500/" + poster_path
            else:
                return "https://via.placeholder.com/500x750?text=No+Image"
        except requests.exceptions.RequestException:
            time.sleep(1)
    return "https://via.placeholder.com/500x750?text=No+Image"

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

# -------------------------------
# Streamlit UI
# -------------------------------
st.header('Movie Recommender System')

movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    cols = st.columns(5)

    for col, name, poster in zip(cols, recommended_movie_names, recommended_movie_posters):
        with col:
            st.text(name)
            st.image(poster)
