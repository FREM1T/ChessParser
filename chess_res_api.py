from requests import get
from bs4 import BeautifulSoup
import json

def get_html(url: str):
    try:
        responce = get(url)
        if responce.status_code != 200:
            print("Не удалось получить доступ к сайту, попробуйте позже...")
            return None
        
        return responce.text
    except Exception:
        print("Не удалось получить доступ к сайту, попробуйте позже...")
        return None

def get_tables(responce: str) -> list:
    soup = BeautifulSoup(responce, "lxml")
    player_table = []
    container = soup.find("div", id="F7")
    
    if container:
        tables = container.find_all("table", class_="CRs1") 
        player_table.append(tables[0])
        player_table.append(tables[1])
    
    return player_table

def get_player_info(table) -> list:
    '''
    Функция 
    '''
    info = table.find_all("tr")
    fullname = (info[0].text)[3:].replace(",", "") # ФИО
    nat_rating = (info[3].text)[11:]
    player_info = [fullname, nat_rating]
    return player_info

def get_matches(table) -> list:
    info = table.find_all("tr")
    matches = info
    return matches

def get_profile(block: list) -> dict:
    '''
    Функция создает словарь, основанный на профиле игрока https://chess-results.com/
    '''

    # Разбиваем блок маленькие таблицы
    matches = get_matches(block[1])         # Массив с информацией об оппонентах 
    player_info = get_player_info(block[0]) # Массив с информацией об игроке
    chess_profile = dict()                  # Инициализация словаря

    # Находим индекс нац.рейт.
    line_ind = matches.pop(0).find_all("th")
    nat_rat_flag = False
    i_rating = 0
    for i in range(len(line_ind)):
        if line_ind[i].text == "Рейт.Нац.":
            nat_rat_flag = True
            i_rating = i
            break

    # Заполняем данные для профиля
    chess_profile["Fullname"] = player_info[0]
    chess_profile["National rating"] = int(player_info[1]) if player_info[1] else 1000

    # Заполняем данные о турнире
    matches_list = [] # Массив для оппонентов
    for i in range(0, len(matches), 2):
        fields = matches[i].find_all("td")

        res = matches[i].find("table").find("td", class_="CR").text
        fullname = fields[4].text
        if nat_rat_flag:
            nat_rating = int(fields[i_rating].text)
        else:
            nat_rating = 1000
        # res = (fields[i_res].text)
        # Обработка res
        if res == "½":
            res = 0.5
        else:
            res = float(res)
        
        opponent = {"Fullname": fullname, "National rating": nat_rating, "Result": res}
        matches_list.append(opponent)

    chess_profile["Opponents"] = matches_list

    return chess_profile

def create_table(obj: dict, filename = "profile.json") -> None:
    '''
    Функция записывает в файл {filename}.json словарь, переданный в аргемент
    '''

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=4)
    f.close()
    
    return None