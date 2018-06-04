import sqlite3
import re
import nba_py
from nba_py import team
from nba_py import league
from nba_py import game
from nba_py.constants import *
import numpy as np

connect = sqlite3.connect("nbadb.db")
scoreboard = nba_py.Scoreboard(month=4,day=14,year=2018)
calendar = scoreboard.game_header()
for d in range(15,31):
    scoreboard=nba_py.Scoreboard(month=4,day=d,year=2018)
    calendar1 = scoreboard.game_header()
    calendar = calendar.append(calendar1,ignore_index=True)
cursor = connect.cursor()
calendar.to_sql("calendar1",connect)

