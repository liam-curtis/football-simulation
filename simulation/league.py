from team import Team
import math
import random

#League Class
class League:
    def __init__(self, teams_df):
        self.teams_list = [] #list of teams in class Team format
        teams = list(teams_df["Squad"]) #contains solely the names of the teams
        for team in teams:
            self.teams_list.append(Team(team, teams_df )) #premier_league_players is placeholder -> player stats not implemented
        self.league_size = len(teams) #league size is # of rows in league
        self.team_results = {} #key = week, value = list that contains array of teams in specific order 1 = first team won, 0 = draw, -1 second team won
        self.goal_results = {} #key = team (1 = arsenal), value = list that contains array goals scored per week
        self.team_rankings = self.ranking() #ranking returns a new copy of team_list that is ordered by points
        self.team_schedule = self.schedule() #key = week, value = list that contains array of teams in specific order
        

    #scheduling function for the league
    def schedule(self):
        team_schedule = {}
        rotation = [] # list of indexes, use team_dict to modify into teams

        for i in range(self.league_size):
            rotation.append(i) #adds the indexes into list for modifacation

        #circle 1, represents every team playing the other once
        for i in range(self.league_size - 1): 
            team_schedule[i] = rotation.copy()
            #rotate, leaving the first index in the same place
            temp = rotation[self.league_size - 1] #temp variable to hold value of first index rotated
            for m in range(self.league_size - 1, 0, -1):
                if m == 1:
                    rotation[m] = temp #rotation[m] =  index 1
                else:
                    rotation[m] = rotation[m - 1] #rotation[m] =  previous m-1 team

        rotation.clear() #clear list for second cycle
        for i in range(self.league_size):
            rotation.append(i) #adds the indexes back into list for modifacation

        #cicle 2, second cycle of teams playing each other
        for i in range(self.league_size - 1): 
            team_schedule[i+self.league_size-1] = rotation.copy()
            #rotate, leaving the first index in the same place
            temp = rotation[self.league_size - 1] #temp variable to hold value of first index rotated
            for m in range(self.league_size - 1, 0, -1):
                if m == 1: 
                    rotation[m] = temp
                else:
                    rotation[m] = rotation[m - 1]

        return team_schedule
    
    #displays the table in text format
    def display_table(self):
        table = "{:<3} {:<15} {:<4} {:<4} {:<4} {:<4}\n".format("#", "Team", "Pts", "GF", "GA", "GD")
        for i in range(self.league_size):
            table += "{:<3} {:<15} {:<4} {:<4} {:<4} {:<4}\n".format(i+1, self.team_rankings[i].name, self.team_rankings[i].points, self.team_rankings[i].goals_for, self.team_rankings[i].goals_against, self.team_rankings[i].GD)
        return table
    
    #ranks the teams based on points
    def ranking(self):
        rankings = self.teams_list.copy()
        rankings.sort(key = lambda x : x.points, reverse=True)
        return rankings
    
    #runs a simulated matchweek
    def matchweek(self, week):
        #run the new matches and update results
        for i in range(self.league_size//2):
            match_result = match(self.teams_list[self.team_schedule[week][i]], self.teams_list[self.team_schedule[week][self.league_size-i-1]], week) #simulate the match between scheduled teams
            if week in self.team_results:
                self.team_results[week].append(match_result) #if not first match can append
            else:
                self.team_results[week] = [match_result] #otherwise must set equal to 
           
            #allocating points based on results of match
            #methods explained in the team 1 win section
            if self.team_results[week][i] == 1: #team 1 win 
                self.teams_list[self.team_schedule[week][i]].points += 3 #add to total points for season for team1
                self.teams_list[self.team_schedule[week][self.league_size-i-1]].points += 0 #add to total points for season for team2
                if week > 0: #if week > 0 then there should already be a value in the points_weekly list, otherwise must initialize a value in the list first
                    #uses the team list at index of dictionary team_schedule with key week at index i, and appends to the list points_weekly the value of the previous points_weekly + added points (3,1,0)
                    self.teams_list[self.team_schedule[week][i]].points_weekly.append(self.teams_list[self.team_schedule[week][i]].points_weekly[week-1] + 3)
                    self.teams_list[self.team_schedule[week][self.league_size-i-1]].points_weekly.append(self.teams_list[self.team_schedule[week][self.league_size-i-1]].points_weekly[week-1])
                else:
                    self.teams_list[self.team_schedule[week][i]].points_weekly.append(3)
                    self.teams_list[self.team_schedule[week][self.league_size-i-1]].points_weekly.append(0)
            elif self.team_results[week][i] == 0: #draw
                self.teams_list[self.team_schedule[week][i]].points += 1
                self.teams_list[self.team_schedule[week][self.league_size-i-1]].points += 1
                if week > 0:
                    self.teams_list[self.team_schedule[week][i]].points_weekly.append(self.teams_list[self.team_schedule[week][i]].points_weekly[week-1] + 1)
                    self.teams_list[self.team_schedule[week][self.league_size-i-1]].points_weekly.append(self.teams_list[self.team_schedule[week][self.league_size-i-1]].points_weekly[week-1] + 1)
                else:
                    self.teams_list[self.team_schedule[week][i]].points_weekly.append(1)
                    self.teams_list[self.team_schedule[week][self.league_size-i-1]].points_weekly.append(1)
            else: #team 2 win
                self.teams_list[self.team_schedule[week][i]].points += 0
                self.teams_list[self.team_schedule[week][self.league_size-i-1]].points += 3
                if week > 0:
                    self.teams_list[self.team_schedule[week][i]].points_weekly.append(self.teams_list[self.team_schedule[week][i]].points_weekly[week-1])
                    self.teams_list[self.team_schedule[week][self.league_size-i-1]].points_weekly.append(self.teams_list[self.team_schedule[week][self.league_size-i-1]].points_weekly[week-1] + 3)
                else:
                    self.teams_list[self.team_schedule[week][i]].points_weekly.append(0)
                    self.teams_list[self.team_schedule[week][self.league_size-i-1]].points_weekly.append(3)
        self.team_rankings = self.ranking()

    #function that returns a string that contains information for league matches
    def display_matches(self, week):
        display = "Matches of Week: " + str(week+1) +"\n"
        if week <= 37:
            for i in range(self.league_size//2):
               display += str(self.teams_list[self.team_schedule[week][i]].name) + " vs " + str(self.teams_list[self.team_schedule[week][self.league_size-i-1]].name) + "\n"
            return display
        else:
            return "End of Season\n"
        
    #function that returns a string that contains results for previous week league matches
    def display_results(self, week):
        display = "Results of Week: " + str(week) +"\n"
        if week > 0 and week <= 37:
            for i in range(self.league_size//2):
               display += str(self.teams_list[self.team_schedule[week-1][i]].name) + "[" + str(self.teams_list[self.team_schedule[week-1][i]].goals_weekly[week-1]) + "]" + " vs " + str(self.teams_list[self.team_schedule[week-1][self.league_size-i-1]].name) + "[" + str(self.teams_list[self.team_schedule[week-1][self.league_size-i-1]].goals_weekly[week-1]) + "]\n"
            return display+"---------------------"
        elif week > 37:
            for i in range(self.league_size//2):
               display += str(self.teams_list[self.team_schedule[37][i]].name) + "[" + str(self.teams_list[self.team_schedule[37][i]].goals_weekly[37]) + "]" + " vs " + str(self.teams_list[self.team_schedule[37][self.league_size-i-1]].name) + "[" + str(self.teams_list[self.team_schedule[37][self.league_size-i-1]].goals_weekly[37]) + "]\n"
            return display+"---------------------"
        else:
            return "No results\n---------------------"
        
    #displays selected week
    def display_table_weekly(self, week):
        table = "{:<3} {:<15} {:<4} {:<4} {:<4} {:<4}\n".format("#", "Team", "Pts", "GF", "GA", "GD")
        teams = self.ranking_weekly(week)
        for i in range(self.league_size):
            table += "{:<3} {:<15} {:<4} {:<4} {:<4} {:<4}\n".format(i+1, teams[i].name, teams[i].points_weekly[week], teams[i].goals_for_weekly[week], teams[i].goals_against_weekly[week], teams[i].GD_weekly[week])
        return table
    #returns rankings given week
    def ranking_weekly(self, week):
        rankings = self.teams_list.copy()
        for i in range(len(rankings)):
            rankings[i].points = rankings[i].points_weekly[week]
        rankings.sort(key = lambda x : x.points, reverse=True)
        return rankings
    
#runs a match between two teams, and runs goal differential
def match(team1, team2, week):
    #right now, we will use a random system of 0-3 goals per game
    #plan to implement a better model for the future
    team1_goals = goalsScored(team1)
    team2_goals = goalsScored(team2)

    #update goals after match
    team1.goals_for += team1_goals
    team1.goals_against += team2_goals
    team2.goals_for += team2_goals
    team2.goals_against += team1_goals
    team1.GD = team1.goals_for - team1.goals_against
    team2.GD = team2.goals_for - team2.goals_against

    #manage week by week goals
    if week > 0:
        team1.goals_weekly.append(team1_goals)
        team2.goals_weekly.append(team2_goals)

        team1.goals_for_weekly.append(team1.goals_for_weekly[week-1] + team1_goals)
        team2.goals_for_weekly.append(team2.goals_for_weekly[week-1] + team2_goals)

        team1.goals_against_weekly.append(team1.goals_against_weekly[week-1] + team2_goals)
        team2.goals_against_weekly.append(team2.goals_against_weekly[week-1] + team1_goals)

        team1.GD_weekly.append(team1.GD_weekly[week-1] + team1_goals - team2_goals)
        team2.GD_weekly.append(team2.GD_weekly[week-1] + team2_goals - team1_goals)
    else:
        team1.goals_weekly.append(team1_goals)
        team2.goals_weekly.append(team2_goals)

        team1.goals_for_weekly.append(team1_goals)
        team2.goals_for_weekly.append(team2_goals)

        team1.goals_against_weekly.append(team2_goals)
        team2.goals_against_weekly.append(team1_goals)

        team1.GD_weekly.append(team1_goals - team2_goals)
        team2.GD_weekly.append(team2_goals - team1_goals)
    #return the winner of the match
    if team1_goals > team2_goals:
        return 1
    elif team1_goals < team2_goals:
        return -1
    else:
        return 0

#uses a poisson distribution to model the amount of goals scored
#uses xG as the mean
def goalsScored(team):
    l = team.xG
    distribution = []
    #generate the expected goals from 0-6
    for k in range(6):
        if k == 0: #for first there is nothing to add
            distribution.append((math.pow(l,k))*(math.pow(2.718,-l))/(math.factorial(k)))
        else: #sum the rest of the distribution in a cumulative frequency manner?
            distribution.append(distribution[k-1] + (math.pow(l,k))*(math.pow(2.718,-l))/(math.factorial(k)))
    #genertate a random number 0-1
    #find which goal value it is less than
    num = random.random()
    for i in range(6):
        if num < distribution[i]:
            return i
    return 0