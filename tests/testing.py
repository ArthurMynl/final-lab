import requests
import random
import string
import pytest

@pytest.fixture(scope="session")
def setup_data():
    letters = string.ascii_letters  # You can include string.digits or string.punctuation if needed
    return ''.join(random.choice(letters) for _ in range(10))


def test_list_movies():
    response = requests.get("http://localhost:8000/movie/")
    assert response.status_code == 200

    # Ensure that the response is a JSON array
    movies = response.json()
    assert isinstance(movies, list)

    # If you're expecting exactly 100 movies
    assert len(movies) == 100

    # If the exact number can vary and you just want to ensure you're getting a list (perhaps not empty)
    assert len(movies) > 0  # Remove or adjust this line based on your requirements
    
    
def test_get_specific_movie():
    # URL encode the query parameters
    movie_title = "The Dark Knight"
    url_encoded_title = requests.utils.quote(movie_title)

    # Construct the full URL
    url = f"http://localhost:8000/movie/specific/?title={url_encoded_title}"

    # Make the request
    response = requests.get(url)

    # Check the status code
    assert response.status_code == 200

    # Parse the JSON response
    movies = response.json()

    # Print response text for debugging
    print(response.text)

    # Check if exactly one movie is returned
    assert isinstance(movies, list)
    assert len(movies) == 1
    
    
def test_update_movie(setup_data):
    # URL encode the movie title
    movie_title = "The Dark Knight"
    url_encoded_title = requests.utils.quote(movie_title)

    # Construct the full URL
    url = f"http://localhost:8000/movie/{url_encoded_title}"

    # JSON payload for the update
    update_payload = {
        "plot": setup_data,
    }

    # Make the PUT or PATCH request
    response = requests.put(url, json=update_payload)

    # Check the status code
    assert response.status_code == 200

    # Check the response body
    assert response.json() == {"message": "Movie updated successfully"}


def test_update_movie_same_data(setup_data):
    # URL encode the movie title
    movie_title = "The Dark Knight"
    url_encoded_title = requests.utils.quote(movie_title)

    # Construct the full URL
    url = f"http://localhost:8000/movie/{url_encoded_title}"

    # JSON payload for the update
    update_payload = {
        "plot": setup_data,
    }

    # Make the PUT or PATCH request
    response = requests.put(url, json=update_payload)

    # Check the status code
    assert response.status_code == 400

    # Check the response body
    assert response.json() == {"detail": "No update performed. Perhaps the new data is the same as existing data."}


def test_update_movie_not_found():
    # URL encode the movie title
    movie_title = "Some Movie"
    url_encoded_title = requests.utils.quote(movie_title)

    # Construct the full URL
    url = f"http://localhost:8000/movie/{url_encoded_title}"

    # JSON payload for the update
    update_payload = {
        "plot": "New plot description",
    }

    # Make the PUT or PATCH request
    response = requests.put(url, json=update_payload)

    # Check the status code
    assert response.status_code == 404

    # Check the response body
    assert response.json() == {"detail": f"Movie with title '{movie_title}' not found"}
    
    
def test_get_common_movies():
    response = requests.get("http://localhost:8000/movie/common")
    assert response.status_code == 200

    # Ensure that the response is a JSON array
    movies = response.json()
    assert isinstance(movies, int)

    assert movies > 0  
    
def test_list_users_who_rated_movie():
    movie_title = "Unforgiven"
    url_encoded_title = requests.utils.quote(movie_title)

    # Construct the full URL
    url = f"http://localhost:8000/movie/{url_encoded_title}/rated-users"

    # Make the request
    response = requests.get(url)

    # Check the status code
    assert response.status_code == 200

    # Parse the JSON response
    users = response.json()

    # Print response text for debugging
    print(response.text)

    # Check if exactly one movie is returned
    assert isinstance(users, list)
    assert len(users) > 0
    
    
def test_list_user_ratings():
    user_name = "Jessica Thompson"
    url_encoded_user_name = requests.utils.quote(user_name)

    # Construct the full URL
    url = f"http://localhost:8000/movie/{url_encoded_user_name}/ratings"

    # Make the request 
    response = requests.get(url)

    assert response.status_code == 200

    # Parse the JSON response
    user_ratings = response.json()

    # Print response text for debugging
    print(response.text)

    # Assertions to match the expected result format:
    assert isinstance(user_ratings, dict)
    assert user_ratings['user'] == user_name
    assert 'movies_rated' in user_ratings
    assert isinstance(user_ratings['movies_rated'], int)
    assert 'rated_movies' in user_ratings
    assert isinstance(user_ratings['rated_movies'], list)
    assert len(user_ratings['rated_movies']) > 0 