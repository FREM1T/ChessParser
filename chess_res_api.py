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
    # Нахождение положения нац.рейт.
    for i in range(len(info)):
        tmp = info[i].find_all("td")
        if tmp[0].text == "Нац.рейтинг":
            nat_rating = tmp[1].text
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
    i_fullname = 0
    for i in range(len(line_ind)):
        if line_ind[i].text == "Имя":
            i_fullname = i
        if line_ind[i].text == "Рейт.Нац.":
            nat_rat_flag = True
            i_rating = i
            break

    # Заполняем данные для профиля
    chess_profile["Fullname"] = player_info[0]
    if player_info[1]:
        chess_profile["National rating"] = int(player_info[1]) if int(player_info[1]) >= 1000 else 1000
    else: chess_profile["National rating"] = 1000

    # Заполняем данные о турнире
    matches_list = [] # Массив для оппонентов
    i = 0
    while i < len(matches):
        fields = matches[i].find_all("td")
        
        # Обработка bye

        if fields[i_fullname].text == "bye":
            res = "-1"
            nat_rating = "-"
            fullname = fields[i_fullname].text
        else:
            res = matches[i].find("table").find("td", class_="CR").text
            fullname = fields[i_fullname].text
            if nat_rat_flag:
                nat_rating = int(fields[i_rating].text)
            else:
                nat_rating = 1000
            i += 1

        # Обработка res
        if res == "½":
            res = 0.5
        else:
            res = float(res)
        
        opponent = {"Fullname": fullname, "National rating": nat_rating, "Result": res}
        matches_list.append(opponent)
        i += 1

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