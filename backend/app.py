import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the movies.csv dataset
movies_df = pd.read_csv("../data/movies.csv")

# Preprocess the genres column: split the genres into a list
movies_df['genres'] = movies_df['genres'].apply(lambda x: x.split('|'))

# Convert the list of genres to a string for TF-IDF vectorization
movies_df['genres_string'] = movies_df['genres'].apply(lambda x: ' '.join(x))

# Create TF-IDF vectors for the genres
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(movies_df['genres_string'])

# Calculate the cosine similarity between movies
cosine_sim = cosine_similarity(tfidf_matrix)

# Function to get movie recommendations based on content-based filtering
def get_recommendations(movie_title, cosine_sim=cosine_sim):
    # Get the index of the movie
    try:
        idx = movies_df[movies_df['title'] == movie_title].index[0]
    except IndexError:
        return "Movie not found"

    # Get the pairwise similarity scores
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the top 10 most similar movies (excluding the movie itself)
    sim_scores = sim_scores[1:11]

    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar movies
    return movies_df['title'].iloc[movie_indices]

# Streamlit web app
st.title('Movie Recommender')

movie_title = st.text_input('Enter a movie title:')

if movie_title:
    recommendations = get_recommendations(movie_title)
    if isinstance(recommendations, str):
        st.write(recommendations)
    else:
        st.write('Recommendations:')
        st.write(recommendations)
