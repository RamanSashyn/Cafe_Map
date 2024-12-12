import json
import requests
import folium
from dotenv import load_dotenv
from geopy import distance
from pprint import pprint
import os


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


def calculate_distance(lat1, lon1, lat2, lon2):
    coords_1 = (lat1, lon1)
    coords_2 = (lat2, lon2)
    return distance.distance(coords_1, coords_2).km


def get_cafe_distance(cafe):
    return cafe["distance"]


def main():
    load_dotenv()
    apikey = os.getenv("API_KEY")

    location = input("Где вы находитесь? ")
    coords = fetch_coordinates(apikey, location)
    if not coords:
        print("Проверьте адрес!")
        return
    print(f"Ваши координаты: {coords}")

    with open("coffee.json", "r", encoding="CP1251") as coffee_file:
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
        cafes_info.append(
            {
                "title": coffee_name,
                "distance": distance_to_cafe,
                "latitude": coffee_latitude,
                "longitude": coffee_longitude,
            }
        )

    nearby_cafes = sorted(cafes_info, key=get_cafe_distance)[:5]
    pprint(nearby_cafes, sort_dicts=False)

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

    map.save("index.html")


if __name__ == "__main__":
    main()
