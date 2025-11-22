import json

def get_growthRate(nat_rat = 1000) -> int:
    growth_rate = 60
    if nat_rat >= 2400:
        growth_rate = 10
    elif nat_rat >= 2200:
        growth_rate = 20
    elif nat_rat >= 2000:
        growth_rate = 25
    elif nat_rat >= 1800:
        growth_rate = 30
    elif nat_rat >= 1600:
        growth_rate = 35
    elif nat_rat >= 1400:
        growth_rate = 40
    elif nat_rat >= 1200:
        growth_rate = 50
            
    return growth_rate

def get_probability(prof_rat = 1000, opp_rat = 1000) -> float:
    prob = 0
    
    with open("probs.csv") as f:
        for line in f:
            line = line.split(";")
            a, b = map(int, line[0].split("-"))
            p1, p2 = map(float, [line[1], line[2]])
            if a <= abs(prof_rat-opp_rat) <= b:
                prob = p1 if prof_rat < opp_rat else p2
                break
    f.close()
    
    return prob

def get_newRating() -> int:
    # https://ruchess.ru/blogs/tkachev/kuda-za-reytingom-podatsya/
    # PD = 0
    # N = 0
    # K = 0
    Ro = 0 # Rating (old)
    Rn = 0 # Rating (new)
    with open("profile.json", "r", encoding="utf-8") as f:
        d = json.load(f)
        Ro = d["National rating"]
        
        total = 0
        for opponent in d["Opponents"]:
            opponents_R = opponent["National rating"]
            N = opponent["Result"]
            PD = get_probability(Ro, opponents_R)
            K = get_growthRate(Ro)
            delta_R = (N - PD) * K
            total += delta_R
        Rn = Ro + total
    f.close()
    
    return int(Rn)