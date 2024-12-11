import json
import requests




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


location = input('Где вы находитесь? ')
coords = fetch_coordinates(apikey, location)
print(f'Ваши координаты: {coords}')


with open("coffee.json", "r", encoding='CP1251') as coffee_file:
    file_content = coffee_file.read()
    coffee_list = json.loads(file_content)

for coffee in coffee_list:
    print(coffee["Name"], coffee['Latitude_WGS84'], coffee['Longitude_WGS84'])




