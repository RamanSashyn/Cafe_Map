import json


with open("coffee.json", "r", encoding='CP1251') as coffee_file:
    file_content = coffee_file.read()
    coffee_list = json.loads(file_content)

for coffee in coffee_list:
    print(coffee["Name"], coffee['Latitude_WGS84'], coffee['Longitude_WGS84'])


first_coffee_name = coffee_list[0]["Name"]
first_coffee_latitude = coffee_list[0]["geoData"]["coordinates"][0]
first_coffee_longitude = coffee_list[0]["geoData"]["coordinates"][1]


print(first_coffee_name)
print(first_coffee_latitude)
print(first_coffee_longitude)

