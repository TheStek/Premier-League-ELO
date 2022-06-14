import numpy as np
import pandas as pd


class Team:

	"""
	name: team name
	elos: 1d list of all elos
	current_elo: current elo of team (last element of elos)
	match_history: 2darray/table with columns match_date, result (W/L/D), opponent (name), old elo, new elo, elo change


	"""


	def __init__(self, name):
		self.name = name
		self.elos = [1000]
		self.current_elo = 1000
		self.match_history = []

	def addMatch(self, date, result, opponent, new_elo):
		self.match_history.append((date, result, opponent, self.current_elo, new_elo, new_elo - self.current_elo))
		self.elos.append(new_elo)
		self.current_elo = new_elo



def getEloChange(r1, r2, result, K = 50):
	"""
	
	Function takes in the current elo of the two teams along with the match result and returns the new elos
	r1, r2 are numbers
	result is an int: 1 team 1 won, 0 draw, -1 team 2 won


	Maths taken from https://metinmediamath.wordpress.com/2013/11/27/how-to-calculate-the-elo-rating-including-example/

	"""

	R1 = 10**(r1/400)
	R2 = 10**(r2/400)

	E1 = R1 / (R1 + R2)
	E2 = R2 / (R1 + R2)

	# Convert result to 1 for win, 0.5 for draw, 0 for loss
	S1 = (result + 1) / 2
	S2 = 1 - S1

	r1_new = r1 + K*(S1 - E1)
	r2_new = r2 + K*(S2 - E2)

	return r1_new, r2_new


def recordMatch(home_name, away_name, result, date):
	home_team = teams[home_name]
	away_team = teams[away_name]

	new_home_elo, new_away_elo = getEloChange(home_team.current_elo, away_team.current_elo, result)

	home_team.addMatch(date, result, away_name, new_home_elo)
	away_team.addMatch(date, -1* result, home_name, new_away_elo)




match_data = pd.read_csv("Data/Match Data.csv")


# Setup all team objects
teams = {name: Team(name) for name in match_data["Home"].unique()}

for match in match_data[["Home", "Away", "Result", "Date"]].itertuples(index = False, name = None):
	recordMatch(*match)


team_histories = []

for team_name in teams.keys():
	team = teams[team_name]

	df = pd.DataFrame(team.match_history, 
		columns = ("Date", "Result", "Opponent", "Old Elo", "New Elo", "Elo Change"))

	df["Team"] = team_name

	team_histories.append(df)


pd.concat(team_histories).to_csv("Data/Team Histories.csv", index = False)



