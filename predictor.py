import math
import urllib.request
import json
import requests

# lightweight Poisson PMF in case scipy is not available
def _poisson_pmf(k, mu):
    # k: non-negative int, mu: expected value
    if k < 0:
        return 0.0
    try:
        return (mu**k) * math.exp(-mu) / math.factorial(k)
    except OverflowError:
        return 0.0
    
def get_standings(team): #use official abbreviation in all caps
    data = requests.get("https://api-web.nhle.com/v1/standings/now").json()
    for item in data["standings"]:
        if item["teamAbbrev"]["default"] == team:
            return item["goalsForPctg"]
    raise ValueError("Team not found")

def poisson_predictor(team1, team2, time_remaining, score1, score2):
    #returns probability of team1 winning
    rate1 = get_standings(team1)
    rate2 = get_standings(team2)
    exp_goals1 = rate1/60*time_remaining
    exp_goals2 = rate2/60*time_remaining
    win_prob = 0.0
    for i in range(15): #highest nhl score ever was 12
        for j in range(15):
            prob1 = _poisson_pmf(i, exp_goals1)
            prob2 = _poisson_pmf(j, exp_goals2)
            if (score1+i) > (score2+j):
                win_prob += (prob1*prob2)
    return win_prob

#col-vgk game 3
print(poisson_predictor("COL", "VGK", 20, 3, 3))
print(poisson_predictor("COL", "VGK", 11.6, 3, 4))
print(poisson_predictor("COL", "VGK", 1, 3, 5))