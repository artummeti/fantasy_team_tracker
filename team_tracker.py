import os
from dotenv import load_dotenv
from sleeper_tracker import *
from player_database_manager import *
from get_player_news import *
from analyze_player_news import *

load_dotenv()

league_id = int(os.environ.get('LEAGUE_ID'))
username = os.environ.get('SLEEPER_USERNAME')

def get_sleeper_data(league_id: int, week: int, username: str, update_db: bool = False):
    if update_db:
        update_player_database

    get_weekly_matchup(league_id, week, username)


week = 7

print('Current Matchup:')
get_sleeper_data(league_id, week, username)
print()

team = get_team_player_names(league_id, username)

for player in team:
    player_news = get_player_news(player)
    print(player_news)
    
    sentiment = analyze_article(player_news)
    decision = decide_start_or_bench(sentiment)
    print(f"Suggestion: {decision}\n")
