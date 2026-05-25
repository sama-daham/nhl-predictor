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
            return (item["goalsForPctg"], float(item["goalAgainst"]/item["gamesPlayed"]))
    raise ValueError("Team not found")

def poisson_predictor(team1, team2, time_remaining, score1, score2):
    #returns probability of team1 winning
    team1_stats = get_standings(team1)
    team2_stats = get_standings(team2)
    #rateA = avg(teamA scoring, teamB scored on)
    rate1 = (team1_stats[0] + team2_stats[1])/2
    rate2 = (team2_stats[0] + team1_stats[1])/2 
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
