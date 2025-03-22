import os
import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Determine the correct path to the movies.csv file
if 'DYNO' in os.environ:
    DATA_PATH = "data/movies.csv"  # Streamlit Cloud
else:
    DATA_PATH = "./data/movies.csv"  # Local

# Load the movies.csv dataset
movies_df = pd.read_csv(DATA_PATH)

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
    # Find movies that contain the entered title (case-insensitive)
    matching_movies = movies_df[movies_df['title'].str.contains(movie_title, case=False)]

    if not matching_movies.empty:
        # Use the index of the first matching movie
        idx = matching_movies.index[0]
    else:
        return "Movie not found"

    # Get the pairwise similarity scores
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the top 10 most similar movies (excluding the movie itself)
    sim_scores = sim_scores[1:11]

    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar movies with titles and genres
    recommended_movies = movies_df[['title', 'genres']].iloc[movie_indices]
    return recommended_movies

# Streamlit web app
# Custom CSS for centering
st.markdown("""
<style>
.centered-title {
    text-align: center;
    font-weight: bold;
}
.centered-widget {
    display: flex;
    justify-content: center;
}
.centered-widget > div {
    width: 80%; /* Adjust width as needed */
}
</style>
""", unsafe_allow_html=True)

# Centered title
st.markdown('<h1 class="centered-title">Movie Recommender</h1>', unsafe_allow_html=True)

# Create columns to center the text input
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    movie_title = st.text_input(
        label='Enter a movie title', 
        label_visibility='hidden', 
        placeholder='Enter a movie title'
        )

if movie_title:
    # Find the entered movie in the dataframe
    input_movie_match = movies_df[movies_df['title'].str.contains(movie_title, case=False)]
    
    # Get movie recommendations and display
    recommendations = get_recommendations(movie_title)
    if isinstance(recommendations, str):
        st.write(recommendations)
    else:
        input_movie_genres_str = ", ".join(input_movie_match.iloc[0]['genres'])
        st.write(f"If you liked '{input_movie_match.iloc[0]['title']}' Genres: {input_movie_genres_str}, you might also like:")
        st.dataframe(recommendations)
