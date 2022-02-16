import sys
from io import BytesIO
from find_params import find_params
# Этот класс поможет нам сделать картинку из потока байт

import requests
from PIL import Image

# Пусть наше приложение предполагает запуск:
# python search.py Москва, ул. Ак. Королева, 12
# Тогда запрос к геокодеру формируется следующим образом:
toponym_to_find = "Москва, ул. Ак. Королева, 12"

toponym_longitude, toponym_lattitude = find_params(toponym_to_find)

spn = float(input())
pt = f"{toponym_longitude},{toponym_lattitude},pmwtm1"

# Собираем параметры для запроса к StaticMapsAPI:
print(spn, pt)
map_params = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "spn": spn,
    "l": "map",
    "pt": pt,
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)

Image.open(BytesIO(
    response.content)).show()
# Создадим картинку
# и тут же ее покажем встроенным просмотрщиком операционной системы