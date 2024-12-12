import json
import requests
import folium
from dotenv import load_dotenv
from geopy import distance
import os


def load_coffee_data(file_path):
    with open("coffee.json", "r", encoding="CP1251") as coffee_file:
        file_content = coffee_file.read()
        return json.loads(file_content)


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(
        base_url,
        params={
            "geocode": address,
            "apikey": apikey,
            "format": "json",
        },
    )
    response.raise_for_status()
    found_places = response.json()["response"]["GeoObjectCollection"][
        "featureMember"
    ]

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant["GeoObject"]["Point"]["pos"].split(" ")
    return lon, lat


def calculate_distance(user_lat, user_lon, cafe_lat, cafe_lon):
    user_coords = (user_lat, user_lon)
    cafe_coords = (cafe_lat, cafe_lon)
    return distance.distance(user_coords, cafe_coords).km


def create_cafe_info(coffee_list, coords):
    cafes_info = []
    for coffee in coffee_list:
        coffee_name = coffee["Name"]
        coffee_longitude = coffee["geoData"]["coordinates"][0]
        coffee_latitude = coffee["geoData"]["coordinates"][1]

        distance_to_cafe = calculate_distance(
            coords[1], coords[0], coffee_latitude, coffee_longitude
        )

        cafes_info.append(
            {
                "title": coffee_name,
                "distance": distance_to_cafe,
                "latitude": coffee_latitude,
                "longitude": coffee_longitude,
            }
        )
    return cafes_info


def get_cafe_distance(cafe):
    return cafe["distance"]


def create_map(coords, nearby_cafes):
    map = folium.Map(location=[coords[1], coords[0]], zoom_start=11)

    folium.Marker(
        location=[coords[1], coords[0]],
        popup="Вы здесь",
        icon=folium.Icon(color="red"),
    ).add_to(map)

    for cafe in nearby_cafes:
        folium.Marker(
            location=[cafe["latitude"], cafe["longitude"]],
            popup=f"{cafe['title']} ({cafe['distance']:.2f} км)",
            icon=folium.Icon(color="green"),
        ).add_to(map)

    return map


def main():
    load_dotenv()
    apikey = os.getenv("APIKEY")

    location = input("Где вы находитесь? ")
    coords = fetch_coordinates(apikey, location)
    if not coords:
        return

    coffee_list = load_coffee_data("coffee.json")

    cafes_info = create_cafe_info(coffee_list, coords)

    nearby_cafes = sorted(cafes_info, key=get_cafe_distance)[:5]

    map = create_map(coords, nearby_cafes)

    map.save("index.html")


if __name__ == "__main__":
    main()
