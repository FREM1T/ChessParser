from urllib.parse import urlparse
from rich.console import Console
import plotext as plt
import json

console = Console()

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

def print_colored_value(value) -> None:
    up = "↑"
    down = "↓"

    if value > 0:
        value = abs(value)
        s = f" +{value:<4.1f}"
        console.print(f"{s} {up}", style="#00FF00", highlight=False, end="")
    elif value < 0:
        value = abs(value)
        s = f" -{value:<4.1f}"
        console.print(f"{s} {down}", style="#FF0000", highlight=False, end="")
    else:
        console.print(" 0       ", style="white", highlight=False, end="")

def print_results(old_r: int, new_r: int, url: str) -> None:
    print("#"*46)
    print(f"Профиль игрока: {url}")
    print(f"Старый нац.рейтинг: {old_r}\nНовый нац.рейтинг: {new_r}")
    print("#"*46)

def print_info(hist: list, old_r, new_r) -> None:
    with open("profile.json", "r", encoding="utf-8") as f:
        info_dict = json.load(f)

        # Окантовка 
        console.print("#"*68, style="bold blue")

        # Вывод информации о профиле игрока
        console.print("#", style="bold blue", end=" ")
        print(f"Полное имя: {info_dict["Fullname"]:<52}", end=" ")
        console.print("#", style="bold blue")

        # Вывод информации о каждом сопернике
        console.print("#", style="bold blue", end=" ")
        s = " |" + f"{'Полное имя':^30}" + "|"\
            + f"{'Нац.Рейт.':^11}" + "|" + f"{'Результат':^11}" + "|"
        print("-"*56, end="")
        console.print(" "*9 +"#", style="bold blue")
        console.print("#", style="bold blue", end="")
        print(s, end="")
        console.print(" "*9 +"#", style="bold blue")

        i = 0
        for opponent in info_dict["Opponents"]:
            s = "|" + f"{opponent["Fullname"]:^30}" + "|"\
            + f"{opponent["National rating"]:>11}" + "|" + f"{opponent["Result"]:>11}" + "|"
            console.print("# ", style="bold blue", end="")
            print(s, end='')
            print_colored_value(hist[i])
            console.print(" #", style="bold blue")

            i += 1

        console.print("#", style="bold blue", end=" ")
        print("-"*56, end="")
        console.print(" "*9 + "#", style="bold blue")

        console.print("#", style="bold blue", end="")
        console.print(f" Рейтинг: {old_r:^4} -> {new_r:<48}", end="")
        console.print("#", style="bold blue")

        console.print("#"*68, style="bold blue")

def show_plot(hist: list, rating: int) -> None:
    new_hist = [x+rating for x in hist]
    plt.plot(new_hist, color="black")
    plt.grid(True)


    plt.show()
    
    return None