import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):

    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=55c68a740792cf01d161a5a684215561".format(movie_id))

    data = response.json()

    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended = []
    movie_ids = []
    for k in movies_list:

        movie_ids.append(movies.iloc[k[0]].id)
        recommended.append(movies.iloc[k[0]].title)
    return recommended, movie_ids


movies_dict = pickle.load(open('Movies.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open("similarity.pkl", 'rb'))
st.title("Movie Recommender")

movie_name = st.selectbox(
    "Which movie you already watched ?",
    movies['title'].values
)
if st.button('Recommend'):
    st.caption("Please wait, we are fetching the recommendations for you")
    names, ids = recommend(movie_name)
    poster = []
    for i in ids:
        poster.append(fetch_poster(i))
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:

        st.image(poster[0], caption=names[0])

    with col2:

        st.image(poster[1], caption=names[1])

    with col3:
        st.image(poster[2], caption=names[2])

    with col4:

        st.image(poster[3], caption=names[3])

    with col5:

        st.image(poster[4], caption=names[4])

