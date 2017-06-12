import csv
import json
import re
import xlrd

derby_matches = [("Arsenal","Tottenham",1.0),("Chelsea","Arsenal",0.9),("Man City","Man United",1.0),("Man United","Liverpool",1.0),("Sunderland","Newcastle",1.0),("West Ham","Chelsea",0.6),("QPR","Chelsea",0.7),("Liverpool","Everton",0.8),("Swansea","Cardiff",1.0),("West Brom","Aston Villa",0.7),("Sunderland","Middlesbrough",0.6),("Bournemouth","Southampton",0.6),("West Ham","Crystal Palace",0.4),("Chelsea","Tottenham",0.8),("Arsenal","West Ham",0.3)]

def isDerby(match1,match2):
	for match in derby_matches:
		if (match1==match[0] and match2==match[1]) or (match1==match[1] and match2==match[0]):
			return match
	return False

def proj():
	workbook = xlrd.open_workbook('12-13_match_data.xls')
	worksheet = workbook.sheet_by_name('12-13_match_data')

	d = {}
	rows = worksheet.row_values(0)
	
	i = 0
	for col in rows:
		d[col] = i
		i += 1
	files = ["06-07.csv","07-08.csv","08-09.csv","09-10.csv","10-11.csv","11-12.csv"]
	team_positions = {}
	average_position = {}
	positions = []
	for f in files:
		with open(f) as tsvfile:
		    tsvreader = csv.reader(tsvfile,delimiter = ",")
		    for line in tsvreader:
		         positions.append((int(line[0]),line[1]))	


	#col1 = worksheet.col_values(d['HomeTeam'])
	#print col1


	dof = {}

	j = 0
	form = {}
	goal_difference = {}
	#rows_all = worksheet.row_values()
	for row in range(worksheet.nrows):
		if j == 0:	
			j += 1
		else:
			dof[j] = worksheet.row_values(row)
			j += 1

	print dof[1][d['HomeTeam']]
	teams = []
	teams.append('teams')
	for yezus in range(1,11):
		teams.append(dof[yezus][d['HomeTeam']])
		teams.append(dof[yezus][d['AwayTeam']])
	#print teams
	WLD = {}

	WLD['win'] = 2
	WLD['draw'] = 1
	WLD['loss'] = 0
	form = {}
	home_value = []
	away_value = []
	GD_home = []
	GD_away = []
	concentration={}
	i=0
	j=0
	for position in positions:
		if position[1]=="Manchester United":
			positions[j] = [position[0],"Man United"]
		if position[1]=="Manchester City":
			positions[j] = [position[0],"Man City"]
		j+=1
	for team in teams:
		if i==0:
			i+=1
		else:
			form[team] = []
			team_positions[team] = []
			goal_difference[team] = (0,0)
			concentration[team]=[]
			for position in positions:
				if (team in position[1] or team==position[1] or position[1] in team):
					team_positions[team].append(position[0])
	#print(teams)
	#print(positions)
	print(team_positions)
	i=0
	for team in teams:
		if i==0:
			i+=1
		else:
			s = sum(team_positions[team])
			n = len(team_positions[team])
			while n<6:
				s = s + 21
				n+=1
			average_position[team] = round(float(s)/n,1)
	print(average_position)
	j=0
	home_concentration = []
	away_concentration = []
	home_win_odds=[]
	away_win_odds=[]
	home_average_position=[]
	away_average_position=[]
	draw_odds=[]
	results = []
	for row in range(worksheet.nrows):
		if j == 0:	
			j += 1
		else:
			home = dof[j][d['HomeTeam']]
			away = dof[j][d['AwayTeam']]
			i=j
			#betting odds features
			H_odds = dof[j][d['B365H']]
			A_odds = dof[j][d['B365A']]
			D_odds = dof[j][d['B365D']]

			H = 1- float(1)/(H_odds)
			A = 1- float(1)/(A_odds)
			D = 1- float(1)/(D_odds)

			home_win_odds.append(H)
			away_win_odds.append(A)
			draw_odds.append(D)
			#average position for the home team and the away team
			home_average_position.append(1-float(average_position[home])/21)
			away_average_position.append(1-float(average_position[away])/21)

			#default x values for home and away
			x1=2
			x2=2
			#calculating the x values for the concentration feature
			result = dof[j][d['FTR']]
			if j!=1:
				i=0
				for c in reversed(concentration[home]):
					if c==1:
						x1 = i+1
						break
					i+=1
				i=0
				for c in reversed(concentration[away]):
					if c==1:
						x2 = i+1
						break
					i+=1
			if result=='A':
				if average_position[away] - average_position[home] > 7:
					if len(concentration[home])==15:
						concentration[home].pop(0)
					if len(concentration[away])==15:
						concentration[home].pop(0)
					concentration[home].append(1)
					concentration[away].append(0)
				else:
					if len(concentration[home])==15:
						concentration[home].pop(0)
					if len(concentration[away])==15:
						concentration[away].pop(0)
					concentration[home].append(0)
					concentration[away].append(0)
			if result=='H':
				if average_position[home] - average_position[away] > 7:
					if len(concentration[away])==15:
						concentration[away].pop(0)
					if len(concentration[home])==15:
						concentration[home].pop(0)
					concentration[away].append(1)
					concentration[home].append(0)
				else:
					if len(concentration[away])==15:
						concentration[away].pop(0)
					if len(concentration[home])==15:
						concentration[home].pop(0)
					concentration[home].append(0)
					concentration[away].append(0)
			if result=='D':
				if len(concentration[away])==15:
					concentration[away].pop(0)
				concentration[away].append(0)
				if len(concentration[home])==15:
					concentration[home].pop(0)
				concentration[home].append(0)
			"""if home=="Man United":
				print concentration[home]
			if away=="Man United":
				print concentration[away]"""
			#print x1
			#print x2
			home_concentration.append(1-1.0/x1)
			away_concentration.append(1-1.0/x2)
			#Calculate the goal difference of the home team and the away team up till now.
			result = dof[j][d['FTR']]
			if j<11:
				GD_home.append(0)
				GD_away.append(0)
			else:
				GD_home.append(goal_difference[home][0] - goal_difference[home][1])
				GD_away.append(goal_difference[away][0] - goal_difference[away][1])
			goal_difference[home] = (goal_difference[home][0] + dof[j][d['FTHG']],goal_difference[home][1] + dof[j][d['FTAG']])
			#goal_difference[home][1] = goal_difference[home][1] + dof[j][d['HTAG']]
			goal_difference[away] = (goal_difference[away][0] + dof[j][d['FTAG']],goal_difference[away][1] + dof[j][d['FTHG']])
			#goal_difference[away][1] = goal_difference[away][1] + dof[j][d['HTHG']]
			
			if len(form[home])<3:
				home_value.append(0.5)
			else:
				home_value.append(float(sum(form[home]))/12)
			if len(form[away])<3:
				away_value.append(0.5)
			else:
				away_value.append(float(sum(form[away]))/12)
			if isDerby(home,away)!=False:
				match = isDerby(home,away)
				formH = home_value.pop()
				formA = away_value.pop()
				new_formH = formH + match[2]*((formH - formA)/2)
				new_formA = formA + match[2]*((formH - formA)/2)
				home_value.append(new_formH)
				away_value.append(new_formA)
			if (result == 'H'):					#filing the form table based on result of the match. Keep only the 6 most recent results in the form table
				if (len(form[away]) == 6):
					form[away].pop(0)
				form[away].append(0)
				if (len(form[home]) == 6):
					form[home].pop(0)
				form[home].append(2)
			elif(result == 'A'):
				if (len(form[away]) == 6):
					form[away].pop(0)
				form[away].append(2)
				if (len(form[home]) == 6):
					form[home].pop(0)
				form[home].append(0)
			else:
				if (len(form[away]) == 6):
					form[away].pop(0)
				form[away].append(1)
				if (len(form[home]) == 6):
					form[home].pop(0)
				form[home].append(1)
			results.append(result)
			j+=1
	i=0
	"""for team in teams:
		if i==0:
			i+=1
		else:
			GD[team] = goal_difference[team][0] - goal_difference[team][1]"""
	i=0
	minimum_GD = min(GD_home)
	maximum_GD = max(GD_home)
	for GD in GD_home:
		GD_home[i] = (GD - minimum_GD)/(maximum_GD - minimum_GD)
		i+=1
	i=0
	minimum_GD = min(GD_away)
	maximum_GD = max(GD_away)
	for GD in GD_away:
		GD_away[i] = (GD - minimum_GD)/(maximum_GD - minimum_GD)
		i+=1
	"""print form
	print(len(home_value))
	print(away_value)
	print(GD_home)
	print(GD_away)
	print(home_concentration)
	print(away_concentration)
	print(home_win_odds)
	print(away_win_odds)"""

	print(average_position)
	print(home_concentration)
	print(concentration["Arsenal"])
	#print(teams)
	data_features = []
	data_features.append(home_value)
	data_features.append(away_value)
	#data_features.append(GD_home)
	#data_features.append(GD_away)
	#data_features.append(home_concentration)
	#data_features.append(away_concentration)
	data_features.append(home_win_odds)
	data_features.append(away_win_odds)
	data_features.append(draw_odds)
	#data_features.append(home_average_position)
	#data_features.append(away_average_position)
	data_features.append(results)
	#print(data_features)
	data_features = zip(*data_features)
	#print(data_features)
	writer = csv.writer(open('data_features.csv','ab'))
	for data in data_features:
		writer.writerow(data)
	outer=1					
if __name__ == '__main__':
	proj()