import pandas as pd
import tkinter as tk
from league import League


path = "C:/VS Code/football-simulation/team_statistics/bundesliga_team_statistics.csv"
bundesliga_team_statistics = pd.read_csv(path)

#Gathering and Formatting Data
#Thanks to fbref.com for statistics. Link: https://fbref.com/en/comps/9/stats/Premier-League-Stats
#Create Dataframe of basic premier league statistics / player statistics
la_liga_team_statistics = pd.read_csv("C:/VS Code/football-simulation/team_statistics/la_liga_team_statistics.csv")
premier_league_team_statistics = pd.read_csv("C:/VS Code/football-simulation/team_statistics/premier_league_team_statistics.csv")
serie_a_team_statistics = pd.read_csv("C:/VS Code/football-simulation/team_statistics/serie_a_team_statistics.csv")
ligue_1_team_statistics = pd.read_csv("C:/VS Code/football-simulation/team_statistics/ligue_1_team_statistics.csv")
bundesliga_team_statistics = pd.read_csv("C:/VS Code/football-simulation/team_statistics/bundesliga_team_statistics.csv")


#Driver
league_container = [League(premier_league_team_statistics),League(la_liga_team_statistics),League(bundesliga_team_statistics),League(serie_a_team_statistics),League(ligue_1_team_statistics)]
league_dictionary = {"Premier League":0,"La Liga":1,"Bundesliga":2,"Serie A":3,"Ligue 1":4}
current_league = 0
week = 0
doneWeek = 0

#Tkinter functions
def terminate(): #closes program
    window.destroy()

def nextWeek(): #runs one week (or progresses to current week if looking at past history)
    global week
    global doneWeek
    if doneWeek < week:
        doneWeek += 1
        lbl_table.configure(text=league_container[current_league].display_table_weekly(doneWeek))
        lbl_matches.configure(text="\n"+league_container[current_league].display_results(doneWeek)+"\n"+league_container[current_league].display_matches(doneWeek))
    else:
        for i in range(len(league_container)):
            if i == 2 and week > 33:
                print("")
            else: 
                league_container[i].matchweek(week)
        week += 1
        doneWeek = week
        lbl_table.configure(text=league_container[current_league].display_table())
        lbl_matches.configure(text="\n"+league_container[current_league].display_results(week)+"\n"+league_container[current_league].display_matches(week))
        update_dropdown_options()

def runSeason(): #runs to end of season
    global week
    global doneWeek
    global current_league
    doneWeek = 37
    while(week != 38):
        for i in range(len(league_container)):
            if i == 2 and week > 33:
                print("")
            else: 
                league_container[i].matchweek(week)
        week += 1
        doneWeek = week
        update_dropdown_options()
    lbl_table.configure(text=league_container[current_league].display_table())
    lbl_matches.configure(text="\n"+league_container[current_league].display_results(38)+"\n"+league_container[current_league].display_matches(38))

def change_week_display(): #changes the displayed values depending on the week
    global doneWeek
    global current_league
    selected_week = int(clicked.get()) - 1
    doneWeek = selected_week
    lbl_table.configure(text=league_container[current_league].display_table_weekly(selected_week))
    lbl_matches.configure(text="\n"+league_container[current_league].display_results(selected_week+1)+"\n"+league_container[current_league].display_matches(selected_week+1))

def update_dropdown_options(): #updates the dropdown menu options depending on how many weeks have occurred
    current_week = week if week < 38 else 38
    options = list(range(1, current_week + 1))
    drop['menu'].delete(0, 'end')
    for option in options:
        drop['menu'].add_command(label=option, command=tk._setit(clicked, option))

def change_league_display():
    global current_league
    global league_dictionary
    current_league = league_dictionary[clickedL.get()]
    print(current_league)
    if doneWeek != week:
        change_week_display()
    else:
        lbl_table.configure(text=league_container[current_league].display_table())
        lbl_matches.configure(text="\n"+league_container[current_league].display_results(week)+"\n"+league_container[current_league].display_matches(week))

#Interactive Tkinter Window
window = tk.Tk()
window.geometry("1200x600+50+50")
window.title("Simulation")
lbl_table = tk.Label(window,text=league_container[current_league].display_table(),justify="left",font="Courier")
lbl_matches = tk.Label(window,text="\n"+league_container[current_league].display_results(0)+"\n"+league_container[current_league].display_matches(0),justify="left",font="Courier")
btn_exit = tk.Button(master=window,text= "Exit",command=terminate,bg='#dd7973', fg='black',font="Courier")
btn_nextWeek = tk.Button(master=window,text= "Go To Next Week",command=nextWeek,bg='#71e3ff', fg='black',font="Courier")
btn_runSeason = tk.Button(master=window,text= "Go to End of Season",command=runSeason,bg='#71e3ff', fg='black',font="Courier")

#drop down menu for week selection
clicked = tk.StringVar(window)
clicked.set("Week")
options = [1]
drop = tk.OptionMenu(window, clicked, *options)
btn_drop = tk.Button(window, text="Select Week",command=change_week_display,bg='#7fd24b', fg='black',font="Courier")
drop.configure(font="Courier")

#drop down menu for league selection
clickedL = tk.StringVar(window)
clickedL.set("League")
optionsL = ["Premier League", "La Liga", "Bundesliga", "Serie A", "Ligue 1"]
dropL = tk.OptionMenu(window, clickedL, *optionsL)
btn_dropL = tk.Button(window, text="Select League",command=change_league_display,bg='#7fd24b', fg='black',font="Courier")
dropL.configure(font="Courier")

#use grid to place all widgets
dropL.grid(column=2,row=0)
btn_dropL.grid(column=3,row=0)
lbl_table.grid(column=0,row=1)
btn_nextWeek.grid(column=0,row=2)
btn_runSeason.grid(column=0,row=3)
lbl_matches.grid(column=1,row=1)
drop.grid(column=2,row=2)
btn_drop.grid(column=3,row=2)
btn_exit.grid(column=1,row=3)

window.mainloop()
