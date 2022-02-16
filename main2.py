import sys
from io import BytesIO
from find_params import find_params
# Этот класс поможет нам сделать картинку из потока байт

import requests
from PIL import Image

# Пусть наше приложение предполагает запуск:
# python search.py Москва, ул. Ак. Королева, 12
# Тогда запрос к геокодеру формируется следующим образом:
toponym_to_find = " ".join(sys.argv[1:])

toponym_longitude, toponym_lattitude = find_params(toponym_to_find)

ll = f"{toponym_longitude},{toponym_lattitude}"

search_api_server = "https://search-maps.yandex.ru/v1/"
api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
search_params = {
    "apikey": api_key,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": ll,
    "type": "biz"
}

response = requests.get(search_api_server, params=search_params)



json_response = response.json()

# Получаем первую найденную организацию.
organization = json_response["features"][0]
# Название организации.
org_name = organization["properties"]["CompanyMetaData"]["name"]
org_time = organization["properties"]["CompanyMetaData"]["Hours"]["text"]
# Адрес организации.
org_address = organization["properties"]["CompanyMetaData"]["address"]

# Получаем координаты ответа.
point = organization["geometry"]["coordinates"]
delta_s = ((point[0] - float(toponym_longitude)) ** 2
           + (point[1] - float(toponym_lattitude)) ** 2) ** 0.5
org_point = "{0},{1}".format(point[0], point[1])
delta = "0.005"

# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
    # позиционируем карту центром на наш исходный адрес
    "ll": ll,
    "spn": ",".join([delta, delta]),
    "l": "map",
    # добавим точку, чтобы указать найденную аптеку
    "pt": "{0},pm2dgl".format(org_point) + "~" + "{0},pm2dgl".format(ll)
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)
info = [org_address, org_name, org_time, delta_s]
print(*info)

Image.open(BytesIO(
    response.content)).show()