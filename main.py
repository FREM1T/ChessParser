from requests import get
from bs4 import BeautifulSoup
from utils import is_url, get_url
from chess_res_api import *
from chess_calc import get_newRating

# Получение url на профиль игрока
profile_url = get_url()

responce = get_html(profile_url)
if responce:
    block = get_tables(responce)
    d = get_profile(block)
    create_table(d)

    print(get_newRating())