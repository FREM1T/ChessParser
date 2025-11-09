from requests import get
from bs4 import BeautifulSoup
from utils import is_url, get_url
from chess_res_api import *


# Получение url на профиль игрока
profile_url = get_url()

responce = get_html(profile_url)

if responce:
    info = get_nRating(get_tables(responce)[0])

    print(*info)
else:
    print("Информация отсутсвует...")