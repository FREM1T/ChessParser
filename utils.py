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