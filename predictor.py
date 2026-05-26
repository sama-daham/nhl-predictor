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

def get_todays_games():
    data = requests.get("https://api-web.nhle.com/v1/schedule/now").json()
    games = data["gameWeek"][0]["games"]
    result = []
    for game in games:
        result.append({"id": game["id"],
        "away": game["awayTeam"]["abbrev"], 
        "home": game["homeTeam"]["abbrev"]})
    return result    

def games_today():
    if get_todays_games() is not None:
        return True
    return False

def pick_game():
    if games_today():
        games = get_todays_games()
        print("Games today: ")
        for i, game in enumerate(games):
            print(str(i+1) + ". " + game["away"] + " @ " + game["home"])  
        choice = input("Pick a game: ")
        return games[int(choice)-1]["id"]
    else:
        return "No games today"

def get_live_game_state(game_id):
    data = requests.get(f"https://api-web.nhle.com/v1/gamecenter/{game_id}/landing").json()
    result = []
    if data["gameState"] == "LIVE":
        time_adjustment = (3 - data["periodDescriptor"]["number"])*20
        result = [data["awayTeam"]["abbrev"],data["homeTeam"]["abbrev"],data["clock"]["secondsRemaining"]/60 + time_adjustment,data["awayTeam"]["score"],data["homeTeam"]["score"]]
        if data["clock"]["inIntermission"]:
            result[2] = time_adjustment
        return result
    raise ValueError("Game is not live")

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

def run_live():
    game_id = pick_game()
    try:
        state = get_live_game_state(game_id)
        result = poisson_predictor(*state)
        print(f"Time remaining: {state[2]}")
        print(f"{state[0]} win probability: {result:.1%}")
        print(f"{state[1]} win probability: {1-result:.1%}")
    except ValueError as e:
        print(f"Game not available: {e}")