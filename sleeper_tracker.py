import requests
from player_database_manager import get_player_info

# using the player id, get their name
def get_player_name(player_id):
    player_info = get_player_info(player_id)
    return player_info['full_name'] if player_info else "Unknown Player"

# get team/player data using specified url
def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    print(f"Error fetching data from {url}: Status code {response.status_code}")
    return None

# get the current matchup of the week
def get_weekly_matchup(league_id, week, user_display_name):
    rosters = fetch_data(f"https://api.sleeper.app/v1/league/{league_id}/rosters")
    if not rosters:
        return

    users = fetch_data(f"https://api.sleeper.app/v1/league/{league_id}/users")
    if not users:
        return

    matchups = fetch_data(f"https://api.sleeper.app/v1/league/{league_id}/matchups/{week}")
    if not matchups:
        return

    roster_dict = {r['roster_id']: {'owner_id': r['owner_id'], 'players': r['players'], 'starters': r['starters']} for r in rosters}
    user_dict = {u['user_id']: u['display_name'] for u in users}
    user_id_dict = {u['display_name']: u['user_id'] for u in users}

    user_id = user_id_dict.get(user_display_name)
    if not user_id:
        print(f"User '{user_display_name}' not in league.")
        return

    user_roster_id = None
    for rid, data in roster_dict.items():
        if data['owner_id'] == user_id:
            user_roster_id = rid
            break

    if not user_roster_id:
        print(f"Roster for user '{user_display_name}' not found.")
        return

    user_matchup = None
    for m in matchups:
        if m['roster_id'] == user_roster_id:
            user_matchup = m
            break

    if not user_matchup:
        print(f"No matchup found for user '{user_display_name}' in week {week}.")
        return

    opponent_roster_id = None
    for m in matchups:
        if m['matchup_id'] == user_matchup['matchup_id'] and m['roster_id'] != user_roster_id:
            opponent_roster_id = m['roster_id']
            break

    if not opponent_roster_id:
        print(f"Could not find opponent for {user_display_name}.")
        return

    opponent_id = roster_dict[opponent_roster_id]['owner_id']
    opponent_name = user_dict.get(opponent_id, "Unknown Opponent")

    # small method to print the score of the team in ppr
    def print_team_performance(team_name, roster_id, matchup_data):
        starters = roster_dict[roster_id]['starters']
        bench = [p for p in roster_dict[roster_id]['players'] if p not in starters]
        
        print(f"\n{team_name}'s Team:")
        print("Starters:")
        for player_id in starters:
            player_name = get_player_name(player_id)
            actual_score = matchup_data['players_points'].get(player_id, 0)
            print(f"  {player_name}: {actual_score:.2f} pts")

        print("Bench:")
        for player_id in bench:
            player_name = get_player_name(player_id)
            actual_score = matchup_data['players_points'].get(player_id, 0)
            print(f"  {player_name}: {actual_score:.2f} pts")

        print(f"Total Score: {matchup_data['points']:.2f} pts")

    # print your team and opposing team's scores

    print_team_performance(user_display_name, user_roster_id, user_matchup)
    
    opponent_matchup = None
    for m in matchups:
        if m['roster_id'] == opponent_roster_id:
            opponent_matchup = m
            break

    if opponent_matchup:
        print_team_performance(opponent_name, opponent_roster_id, opponent_matchup)
    else:
        print(f"Could not find {opponent_name}'s team data.")

# get all of the players on a users team
def get_team_player_names(league_id, user_display_name):
    rosters = fetch_data(f"https://api.sleeper.app/v1/league/{league_id}/rosters")
    if not rosters:
        return []

    users = fetch_data(f"https://api.sleeper.app/v1/league/{league_id}/users")
    if not users:
        return []

    roster_dict = {r['roster_id']: {'owner_id': r['owner_id'], 'players': r['players']} for r in rosters}
    user_dict = {u['user_id']: u['display_name'] for u in users}
    user_id_dict = {u['display_name']: u['user_id'] for u in users}

    user_id = user_id_dict.get(user_display_name)
    if not user_id:
        print(f"User '{user_display_name}' not in league.")
        return []

    user_roster_id = None
    for rid, data in roster_dict.items():
        if data['owner_id'] == user_id:
            user_roster_id = rid
            break

    if not user_roster_id:
        print(f"Roster for user '{user_display_name}' not found.")
        return []

    player_ids = roster_dict[user_roster_id]['players']
    player_names = [get_player_name(player_id) for player_id in player_ids]
    
    return player_names