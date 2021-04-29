import os
import sys
import requests


def locate():
    geocoder_request = "http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode=сыктывкар+Карла+Маркса+202&format=json"
    coords = requests.get(geocoder_request)
    if coords:
        json_response = coords.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        # Координаты центра топонима:
        toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
        toponym_coodrinates = toponym["Point"]["pos"]
        longitude, latitude = toponym_coodrinates.split(' ')
        print(toponym_address, toponym_coodrinates)
    else:
        print("Ошибка выполнения запроса:")
        print(geocoder_request)
        print("Http статус:", coords.status_code, "(", coords.reason, ")")
        return

    map_request = f"https://static-maps.yandex.ru/1.x/?ll={longitude},{latitude}&spn=0.0007,0.0007&l=sat,skl"
    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    os.chdir("..")
    map_file = "static/images/map.jpg"
    with open(map_file, "wb") as file:
        file.write(response.content)
