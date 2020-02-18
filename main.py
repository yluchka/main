from geopy.geocoders import Nominatim
from years_dict import films_locations, YEAR_DICT
import mpu
import time
import folium


def films_coordinates(year: str) -> dict:
    """
    returns a dictionary with the name of the movie in the keys
    and the longitude and latitude of the values
    """
    dict_locations = films_locations(YEAR_DICT, year)
    b = Nominatim(user_agent="specify_your_app_name_here")
    coordinates = {}
    start = time.perf_counter()
    for movie in dict_locations:
        if time.perf_counter() - start > 180:
            break
        try:
            coordinates_of_film = b.geocode(dict_locations[movie][0])
            if coordinates_of_film is None:
                continue
        except Exception:
            continue
        coordinates[movie] = coordinates_of_film.latitude, coordinates_of_film.longitude
    return coordinates


def closest_movies_to_the_user(latitude: str, longitude: str, year: str) -> dict:
    """
    returns the dictionary with the ten closest movies
    to the specified user location
    """
    coordinates = films_coordinates(year)
    user_coordinate = (latitude, longitude)
    sorted_films = sorted(coordinates.items(), key= lambda x: mpu.haversine_distance(x[1], user_coordinate))
    return sorted_films[:10]


def map_generation(latitude: float, longtitude: float, year: str):
    """
    generates a map showing up country and to ten of the closest
    user-defined film shoots in a given year
    """
    location_near = closest_movies_to_the_user(latitude, longtitude, str(year))
    gen_map = folium.Map()
    snd_layer = folium.FeatureGroup("films loc")
    for film in location_near:
        snd_layer.add_child(folium.Marker(location=film[1], popup=film[0],  icon=folium.Icon()))
    gen_map.add_child(snd_layer)
    fg_pp = folium.FeatureGroup(name="Population")
    fg_pp.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(), style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000 else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))
    gen_map.add_child(fg_pp)
    gen_map.add_child(folium.LayerControl())
    gen_map.save("map.html")


def user():
    """
    function for the user
    """
    year = input("Please enter a year you would like to have a map for: ")
    latitude = float(input("Please enter your latitude: "))
    longtitude = float(input("Please enter your longtitude: "))
    print("Map is generating...")
    print("Please wait...")
    map_generation(latitude, longtitude, year)
    print("Finished. Please have look at the map map.html")

if __name__ == "__main__":
    user()
