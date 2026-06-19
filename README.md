# 🏒 NHL Win Probability Predictor
A real-time win probability model for live NHL games, built and live-tested during the 2026 Stanley Cup Playoffs.
## What It Does
Given a live NHL game, this model calculates the probability that each team wins — updated continuously as goals are scored and time ticks down. It also pulls live FanDuel implied probabilities via The Odds API so you can compare the model's output against the betting market in real time.
## Why I Built It
I wanted to apply probability theory to something I actually follow. Hockey is a low-scoring sport, which makes goal-scoring well-modeled by a Poisson process — and that makes in-game win probability a tractable math problem. This project is my attempt to build that from scratch and test it against real playoff games.
## How It Works
- Applies Bayesian updating to adjust team scoring rates as game state evolves
- Models goal arrivals as a Poisson process using each team's GF/60 and GA/60 rates
- Blends offensive rate with opponent defensive rate to estimate an effective scoring parameter (λ)
- Updates win probability continuously based on current score and time remaining
- Fetches live game state from the NHL Stats API
- Pulls live FanDuel moneyline odds from The Odds API for real-time comparison
## Sample Output

**CAR @ MTL — May 25, 2026 (Playoffs)**
MTL won. With ~12 minutes left in the 3rd period, the model had MTL at 68–70% — while FanDuel had CAR as the favorite at ~59%. The model's score-adjusted probabilities correctly reflected the game state.
**CAR @ VGK — June 14, 2026 (Stanley Cup Final)**
CAR won. The model opened at ~45% CAR, jumped to ~62% after an early CAR goal, and tracked closely with FanDuel's movement throughout. By the final minutes, both the model and market converged on CAR at ~99%.

\`\`\`
2026-06-14 19:29:48
Time remaining: 55.7
CAR win probability: 62.0%
VGK win probability: 23.3%
FanDuel data:
CAR: 69.9%
VGK: 35.7%
\`\`\`

## Setup
```bash
git clone https://github.com/sama-daham/nhl-predictor
cd nhl-predictor
pip install -r requirements.txt
```
Add your Odds API key to `config.py`:
```python
ODDS_API_KEY = "your_key_here"
```
Then run:
```bash
python3 examples.py
```
## Future Improvements
- **Overtime model** — OT is currently treated as continued regulation-style scoring rather than true sudden-death dynamics
- **Playoff-adjusted scoring rates** — season-long GF/60 underestimates hot playoff teams; blend regular season and postseason rates
- **Goalie adjustment** — isolating goalie performance via save % or GSAx rather than approximating via team GA/60
- **Score-state effects** — no adjustment yet for trailing teams pulling the goalie late, or defensive play when leading
- **Backtesting framework** — systematic accuracy testing across full season game logs to formally calibrate against market odds


## Built With
Python · NHL Stats API · The Odds API (FanDuel)
