from imdb import IMDb

def get_full_cast(movie_title):
    ia = IMDb()
    
    # Search for the movie
    movies = ia.search_movie(movie_title)
    
    if movies:
        movie = movies[0]
        ia.update(movie, 'cast')
        
        # Get full cast list
        cast = movie.get('cast', [])
        
        print(f"\n{movie['title']} - Full Cast:")
        for person in cast[:20]:  # First 20 actors
            print(f"  - {person['name']}")
        
        return [person['name'] for person in cast]
    
    return []

# Example
get_full_cast("The Dark Knight")

print(get_full_cast("Inception"))