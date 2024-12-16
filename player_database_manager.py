import requests
import sqlite3
import json
from datetime import datetime, timedelta

# if needed, update the local player database
# from sleeper api documentation
def update_player_database(force_update=False):
    conn = sqlite3.connect('nfl_players.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS players
    (id TEXT PRIMARY KEY, 
    first_name TEXT, 
    last_name TEXT, 
    full_name TEXT,
    team TEXT,
    position TEXT,
    age INTEGER,
    data TEXT, 
    last_updated TEXT)
    ''')

    cursor.execute("SELECT last_updated FROM players LIMIT 1")
    result = cursor.fetchone()
    
    current_time = datetime.now()
    if result:
        last_updated = datetime.fromisoformat(result[0])
        if (current_time - last_updated) < timedelta(days=7) and not force_update:
            print("Player database is up to date.")
            conn.close()
            return

    print("Updating player database...")
    
    players_url = "https://api.sleeper.app/v1/players/nfl"
    response = requests.get(players_url)
    
    if response.status_code != 200:
        print(f"Error fetching players: Status code {response.status_code}")
        conn.close()
        return
    
    players = response.json()

    for player_id, player_data in players.items():
        first_name = player_data.get('first_name', '')
        last_name = player_data.get('last_name', '')
        full_name = f"{first_name} {last_name}".strip()
        team = player_data.get('team', '')
        position = player_data.get('position', '')
        age = player_data.get('age', 0)

        cursor.execute('''
        INSERT OR REPLACE INTO players 
        (id, first_name, last_name, full_name, team, position, age, data, last_updated)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (player_id, first_name, last_name, full_name, team, position, age, 
              json.dumps(player_data), current_time.isoformat()))

    conn.commit()
    conn.close()
    print("Player database updated successfully.")

#get a players name, position age and data using their player id
def get_player_info(player_id):
    conn = sqlite3.connect('nfl_players.db')
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, first_name, last_name, full_name, team, position, age, data 
    FROM players WHERE id = ?
    """, (player_id,))
    result = cursor.fetchone()

    if result:
        player_info = {
            'id': result[0],
            'first_name': result[1],
            'last_name': result[2],
            'full_name': result[3],
            'team': result[4],
            'position': result[5],
            'age': result[6],
            'data': json.loads(result[7])
        }
    else:
        player_info = None

    conn.close()
    return player_info


# if __name__ == "__main__":
# manage_player_database()