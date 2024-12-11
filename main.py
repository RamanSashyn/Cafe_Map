import json
import requests
from geopy import distance
from pprint import pprint



apikey = '60c9f71a-6312-4c7e-91e6-670e028c5937'


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


def calculate_distance(lat1, lon1, lat2, lon2):
    coords_1 = (lat1, lon1)
    coords_2 = (lat2, lon2)
    return distance.distance(coords_1, coords_2).km


location = input('Где вы находитесь? ')
coords = fetch_coordinates(apikey, location)
print(f'Ваши координаты: {coords}')


with open("coffee.json", "r", encoding='CP1251') as coffee_file:
    file_content = coffee_file.read()
    coffee_list = json.loads(file_content)

cafes_info = []

for coffee in coffee_list:
    coffee_name = coffee["Name"]
    coffee_longitude = coffee["geoData"]["coordinates"][0]
    coffee_latitude = coffee["geoData"]["coordinates"][1]
    distance_to_cafe = calculate_distance(
        coords[1], coords[0], coffee_latitude, coffee_longitude
    )


    cafes_info.append({
        'title': coffee_name,
        'distance': distance_to_cafe,
        'latitude': coffee_latitude,
        'longitude': coffee_longitude
    })


pprint(cafes_info, sort_dicts=False)




















