from urllib.parse import urlparse
import json

def is_url(url: str) -> bool:
    '''
    Проверяет является ли текст url
    '''
    try:
        url_link = urlparse(url) # url -> scheme://netloc/path;parameters?query#fragment
        return all([url_link.netloc, url_link.scheme])
    except Exception:
        return False

def get_url() -> str:
    url = input("Пожалуйста, вставьте url на профиль игрока: ")
    
    while is_url(url) != True:
        print("Ошибка: введите корректную ссылку на профиль игрока!")
        print("Пример: https://s3.chess-results.com/tnr125754.aspx?lan=11&art=9&snr=1\n")
        url = input("Пожалуйста, вставьте url на профиль игрока: ")
    
    return url

def print_results(old_r: int, new_r: int, url: str) -> None:
    print("#"*46)
    print(f"Профиль игрока: {url}")
    print(f"Старый нац.рейтинг: {old_r}\nНовый нац.рейтинг: {new_r}")
    print("#"*46)

def print_info() -> None:
    with open("profile.json", "r", encoding="utf-8") as f:
        info_dict = json.load(f)
        # Вывод информации о профиле игрока
        print(f"Полное имя: {info_dict["Fullname"]}")
        print(f"Национальный рейтинг: {info_dict["National rating"]}")
        # Вывод информации о каждом сопернике
        s = "-"*56 + "\n|" + f"{'Полное имя':^30}" + "|"\
            + f"{'Нац.Рейт.':^11}" + "|" + f"{'Результат':^11}" + "|"
        print(s)
        for opponent in info_dict["Opponents"]:
            s = "|" + f"{opponent["Fullname"]:^30}" + "|"\
            + f"{opponent["National rating"]:>11}" + "|" + f"{opponent["Result"]:>11}" + "|"
            print(s)
        print("-"*56)