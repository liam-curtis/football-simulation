# football-simulation

This program is a simulation that simulates a league using a FBRef.com dataset for soccer. 
It is currently set up to use the premier league. 

Features:
Simulate soccer league
Ability to go back to weeks previously done
Goals scored in match use a Poisson Distribution with maximum of 6 goals, using xG as mean
Ability to see statistics such as GF GA GD Pts
Ability to see previous results and future matchups
Matching algorithm that ensures every team plays every other team twice (Double Round Robin)
Interactive GUI

Known issues:
Going to past week and then moving to current week has an error where it doesn't move forward 
as expected. 
Teams are only ranked by points, should add GD as tie breaker

Future features:
Work with Players dataset, allowing for teams to each have 11 players and a full roster.
Display more statistics (MP, xG)
Display top scorers (and other stats) week-by-week
Display Graphs that show team / player performance accross season
Integrate more variables into match model (defense score)
Integrate variables into season model (momentum, injuries, suspensions)
