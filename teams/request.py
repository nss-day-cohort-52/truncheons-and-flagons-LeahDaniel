import sqlite3
import json
from models import Player, Team, TeamScore


def get_teams(filters):
    with sqlite3.connect("./flagons.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        teams = {}

        if filters is None:
            db_cursor.execute("""
            SELECT
                t.id,
                t.name
            FROM Teams t
            """)

            dataset = db_cursor.fetchall()

            teams = []
            for row in dataset:
                team = Team(row['id'], row['name'])
                teams.append(team.__dict__)

            return json.dumps(teams)

        else:
            if "_embed" in filters:
                for related_resource in filters['_embed']['resources']:
                    if related_resource == "teamScores":
                        db_cursor.execute("""
                        SELECT
                            t.id,
                            t.name,
                            ts.id score_id,
                            ts.team_id,
                            ts.score,
                            ts.time_stamp
                        FROM Teams t
                        JOIN TeamScores ts ON ts.team_id = t.id
                        """)
                        #! Why, if the above is a Left join, do we get an irrelevant score dictionary for team 3?
                        dataset = db_cursor.fetchall()

                        for row in dataset:
                            if row['id'] not in teams:
                                team = Team(row['id'], row['name'])
                                teams[row['id']] = team
                            else:
                                team = teams[row['id']]

                            score = int(
                                row['score']) if row['score'] is not None else 0
                            if score > 0:
                                team_score = TeamScore(
                                    row['score_id'], row['team_id'], score, row['time_stamp'])
                            team.scores.append(team_score.__dict__)

                    elif related_resource == "players":
                        db_cursor.execute("""
                        SELECT
                            t.id,
                            t.name,
                            p.id player_id,
                            p.first_name,
                            p.last_name,
                            p.team_id
                        FROM Teams t
                        LEFT JOIN Players p ON p.team_id = t.id
                        """)

                        dataset = db_cursor.fetchall()

                        for row in dataset:
                            if row['id'] not in teams:
                                team = Team(row['id'], row['name'])
                                teams[row['id']] = team
                            else:
                                team = teams[row['id']]

                            player = Player(
                                row['player_id'], row['first_name'], row['last_name'], row['team_id'])
                            team.players.append(player.__dict__)

            json_teams = []
            for team in teams.values():
                json_teams.append(team.__dict__)
            return json.dumps(json_teams)


def get_all_players():
    # Open a connection to the database
    with sqlite3.connect("./flagons.db") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            a.id,
            a.first_name,
            a.last_name,
            a.team_id
        FROM players a
        """)

        # Initialize an empty list to hold all player representations
        players = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an player instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Player class above.
            player = Player(row['id'], row['first_name'], row['last_name'],
                                row['team_id'])

            players.append(player.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(players)

def get_all_team_scores():
    # Open a connection to the database
    with sqlite3.connect("./flagons.db") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            a.id,
            a.team_id,
            a.score,
            a.time_stamp
        FROM TeamScores a
        """)

        # Initialize an empty list to hold all player representations
        team_scores = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an player instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Player class above.
            team_score = TeamScore(row['id'], row['team_id'], row['score'],
                                row['time_stamp'])

            team_scores.append(team_score.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(team_scores)