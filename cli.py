from requests import get
from bs4 import BeautifulSoup
from utils import get_url, print_results, print_info
from chess_res_api import *
from chess_calc import get_newRating, get_oldRating

import os

# Функция меню в терминале
def main_menu():
    while True:
        # Получаем url
        profile_url = get_url()

        responce = get_html(profile_url)
        if responce:
            block = get_tables(responce)
            d = get_profile(block)
            create_table(d)

            print_results(get_oldRating(), get_newRating(), profile_url)

            print_info()
            
        else:
            # Ошибка доступа к сайту
            print("Сайт временно недоступен, повторите попытку попозже")
            break
            
        
        flag = input("Желаете продолжить? Y/n: ").lower()
        os.system("clear") if os.name == "posix" else os.system("cls")
        if flag not in "y":
            break