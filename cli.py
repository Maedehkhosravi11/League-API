import requests
import datetime

API_TOKEN = 'ab24d8d891664568a8f69c3c5597b45e'
LEAGUES_API_URL = 'http://api.football-data.org/v4/areas/'
MATCHES_API_URL = 'https://api.football-data.org/v4/competitions/{}/matches'


COMMON_LEAGUES = {
    'La Liga': 'PD',
    'Bundesliga': 'BL1',
    'Premier League': 'PL',
    'Serie A': 'SA'
}

def get_leagues():
    headers = {
        'X-Auth-Token': API_TOKEN
    }
    response = requests.get(LEAGUES_API_URL, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None

def get_matches(league_id, date_from, date_to):
    headers = {
        'X-Auth-Token': API_TOKEN
    }
    params = {
        'dateFrom': date_from,
        'dateTo': date_to
    }
    url = MATCHES_API_URL.format(league_id)
    print(url)
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None

def valid_date(date_str):
    try:
        datetime.datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def main():
    
    print("Choose a football league:")
    for i, league in enumerate(COMMON_LEAGUES, 1):
        print(f"{i}. {league}")
    print(f"{len(COMMON_LEAGUES) + 1}. More")


    choice = input("Enter the number of your choice: ")

    try:
        choice_index = int(choice) - 1
        if choice_index < 0 or choice_index > len(COMMON_LEAGUES):
            print("Invalid choice.")
            return
        
        if choice_index < len(COMMON_LEAGUES):
            league_name = list(COMMON_LEAGUES.keys())[choice_index]
            league_id = COMMON_LEAGUES[league_name]
            print(f"You chose {league_name}.")
        else:
            # Display additional leagues
            leagues_data = get_leagues()
            if not leagues_data or 'areas' not in leagues_data:
                print("Could not retrieve leagues.")
                return
            
            areas = leagues_data['areas']
            print("Choose a football league area:")
            for i, area in enumerate(areas, 1):
                print(f"{i}. {area['name']}")
            
            
            additional_choice = input("Enter the number of your choice: ")
            try:
                additional_choice_index = int(additional_choice) - 1
                if additional_choice_index < 0 or additional_choice_index >= len(areas):
                    print("Invalid choice.")
                    return
                
                chosen_area = areas[additional_choice_index]
                league_id = chosen_area['id']
                print(f"You chose {chosen_area['name']}.")
            except ValueError:
                print("Invalid input. Please enter a number.")
                return

        
        date_from = input("Enter the start date (YYYY-MM-DD): ")
        if not valid_date(date_from):
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
            return

        date_to = input("Enter the end date (YYYY-MM-DD): ")
        if not valid_date(date_to):
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
            return

        
        matches = get_matches(league_id, date_from, date_to)
        if matches and 'matches' in matches:
            for match in matches['matches']:
                home_team = match['homeTeam']['name'] if 'homeTeam' in match else 'Unknown'
                away_team = match['awayTeam']['name'] if 'awayTeam' in match else 'Unknown'
                
                if 'score' in match and 'fullTime' in match['score']:
                    home_score = match['score']['fullTime']['home'] if match['score']['fullTime']['home'] is not None else '?'
                    away_score = match['score']['fullTime']['away'] if match['score']['fullTime']['away'] is not None else '?'
                    score_str = f"{home_score}:{away_score}"
                else:
                    score_str = " - "

                match_date = match['utcDate'][:10] if 'utcDate' in match else 'Unknown'
                print(f"{match_date}: {home_team} vs {away_team} - {score_str}")

    except ValueError:
        print("Invalid input. Please enter a number.")

if __name__ == '__main__':
    main()
