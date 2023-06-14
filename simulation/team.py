#Team Class
class Team:
    # constructor
    def __init__(self, name, teams_df):
        self.name = name #Name of team
        #self.players_df = players_df.loc[players_df["Squad"] == name, :] # grabs the roster from players_df
        self.xG = teams_df.loc[teams_df['Squad'] == name, 'xG'].item() / (len(teams_df)*2-2) #grabs the expected goals per game
        self.points = 0
        self.points_weekly = [] #list that contains week by week points
        self.goals_weekly = [] #list that contains week by week goals (NOT SUMMED)
        self.goals_for_weekly = [] #list that contains week by week goals_for
        self.goals_against_weekly = [] #list that contains week by week goals_against
        self.GD_weekly = [] #list that contains week by week GD
        self.goals_for = 0
        self.goals_against = 0
        self.GD = self.goals_for - self.goals_against
