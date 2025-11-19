import requests

API_KEY = "2aaf18d5"    # ONLY the key, NOT the URL
url = f"http://www.omdbapi.com/?apikey={API_KEY}&t=Inception"

print(requests.get(url).text)

movies = [
    "The Shawshank Redemption",
    "The Dark Knight",
    "Fight Club",
    "Inception"
]

def get_movie_info(title):
    url = "http://www.omdbapi.com/"
    params = {
        "t": title,
        "apikey": API_KEY
    }
    r = requests.get(url, params=params)
    print("DEBUG:", r.text)
    return r.json()

all_data = {}

for movie in movies:
    info = get_movie_info(movie)
    if info.get("Response") == "True":
        all_data[movie] = info
    else:
        all_data[movie] = {"error": info.get("Error")}

for movie, data in all_data.items():
    print(f"\n--- {movie} ---")
    print("IMDB ID:", data.get("imdbID"))
    print("Actors:", data.get("Actors"))
    print("Year:", data.get("Year"))
    print("Rating:", data.get("imdbRating"))
    print("Genre:", data.get("Genre"))
    print("Plot:", data.get("Plot"))