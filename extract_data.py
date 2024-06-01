import requests
import pandas as pd 
# TMDB API key
API_KEY = '' # put your tmdb api key here

# Base URL for TMDB API
BASE_URL = 'https://api.themoviedb.org/3'

# Function to search for the latest movies with credits
def search_latest_movies_with_credits(count,p):
    url = f'{BASE_URL}/discover/movie'
    params = {
        'api_key': API_KEY,
        'language': 'en',  # set 'hi' for hindi/bollywood movies
        'with_original_language': 'en',  # set 'hi' for hindi language (Bollywood movies)
        'region': 'US', # set 'IN' for India
        'sort_by': 'popularity.desc',  # Sort by popularity in descending order
        'page': p,  # Start from page 1
        'include_adult': False,  # Exclude adult content
        'include_video': False  # Exclude video content
    }

    movies = []
    credit = []
    total_pages = 1
    while len(movies) < count:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            total_pages = data['total_pages']
            results = data['results']
            for movie in results:
                # Get movie details
                movie_id = movie['id']
                movie_details = get_movie_details(movie_id)
                # Get movie credits
                credits = get_movie_credits(movie_id)
                # Add these details to their respective list
                movies.append(movie_details)
                credit.append(credits)
                
                if len(movies) == count:
                    break
            params['page'] += 1
            #print(params['page'])
        else:
            print('Error:', response.status_code)
            break

    return movies,credit,params['page']

# Function to get movie details
def get_movie_details(movie_id):
    url = f'{BASE_URL}/movie/{movie_id}'
    params = {
        'api_key': API_KEY,
        'language': 'en',  # set 'hi' for hindi/bollywood movies
        'with_original_language': 'en',  # set 'hi' for hindi language (Bollywood movies)
        'region': 'US', # set 'IN' for India
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print('Error:', response.status_code)
        return None

# Function to get movie credits
def get_movie_credits(movie_id):
    url = f'{BASE_URL}/movie/{movie_id}/credits'
    params = {
        'api_key': API_KEY
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print('Error:', response.status_code)
        return None

# Search for the latest movies with credits
HMovies = pd.DataFrame()
HCredits = pd.DataFrame()
page = 1
for i in range(1,6):
    movies,credits,page = search_latest_movies_with_credits(1000,page) # Retrieve 10,000 latest movies with credits
    print(i,page)
    hollywood_movies = pd.DataFrame(movies)
    hollywood_credits = pd.DataFrame(credits)
    HMovies = pd.concat([HMovies,hollywood_movies], axis=0)
    HCredits = pd.concat([HCredits,hollywood_credits], axis=0)
    HMovies.to_csv('/kaggle/working/hollywood_movies.csv', index=False) 
    HCredits.to_csv('/kaggle/working/hollywood_credits.csv', index=False) 