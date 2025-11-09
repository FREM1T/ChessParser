from requests import get
from bs4 import BeautifulSoup

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

def get_nRating(table) -> list:
    info = table.find_all("tr")
    name = info[0].get_text(separator=" - ")
    nRating = info[4].get_text(separator=" - ")

    return [name, nRating]

def get_matchs(table) -> list:
    