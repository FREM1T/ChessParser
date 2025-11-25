from urllib.parse import urlparse

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
    print("#"*100)
    print(f"Профиль игрока: {url}")
    print(f"Старый нац.рейтинг: {old_r}\nНовый нац.рейтинг: {new_r}")
    print("#"*100)