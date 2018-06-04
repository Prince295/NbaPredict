import sqlite3
import re
import nba_py
from nba_py import team
from nba_py import league
from nba_py import game
from nba_py.constants import *
import numpy as np

def get_tempo(home,guest):
    connect = sqlite3.connect("nbadb.db")
    cursor = connect.cursor()

    cursor.execute("""SELECT PACE,OFF_RATING,DEF_RATING FROM team_adv_stats
                                                  WHERE TEAM_ID = (?)
                                              """, (guest,))
    tempo_away,off_rat_away,def_rat_away = cursor.fetchall()[0]
    cursor.execute("""SELECT PACE,OFF_RATING,DEF_RATING FROM team_adv_stats
                                                      WHERE TEAM_ID = (?)
                                                  """, (home,))
    tempo_home,off_rat_home,def_rat_home = cursor.fetchall()[0]
    result = team.TeamDefensiveDashboard().overall()
    result = result.to_dict()
    team_stats = league.TeamStats()
    team_stats.__init__(team_id=home,opponent_team_id=guest,measure_type=MeasureType.Advanced )
    home_vs_opponent = team_stats.overall().to_dict()
    team_stats.__init__(team_id=guest, opponent_team_id=home,measure_type=MeasureType.Advanced)
    away_vs_opponent = team_stats.overall().to_dict()
    team_stats.__init__(team_id=home, opponent_team_id=guest,location=Location.Home,measure_type=MeasureType.Advanced)
    home_vs_opponent_home = team_stats.overall().to_dict()
    team_stats.__init__(team_id=guest, opponent_team_id=home, measure_type=MeasureType.Advanced,location='Road')
    away_vs_opponent_away = team_stats.overall().to_dict()
    tempo = (tempo_home + 2*home_vs_opponent['PACE'][0] + 3*home_vs_opponent_home['PACE'][0]+tempo_away)/7
    off_rat = (off_rat_home + 1.1*home_vs_opponent['OFF_RATING'][0] + 1.2*home_vs_opponent_home['OFF_RATING'][0] + def_rat_away)/4.3
    def_rat = (def_rat_home + 1.1*home_vs_opponent['DEF_RATING'][0] + 1.2*home_vs_opponent_home['DEF_RATING'][0] + off_rat_away )/4.3
    score_home = (off_rat * tempo)/100
    score_away = (def_rat * tempo)/100
    return score_home, score_away,home,guest


    connect.commit()


def get_refs(score_home, score_away,home, guest):

    connect = sqlite3.connect("nbadb.db")
    cursor = connect.cursor()
    officials_dict = game.BoxscoreSummary('0041700151').officials().to_dict()
    off_params = []
    for i in range(len(officials_dict['FIRST_NAME'])):
        cursor.execute("""SELECT FirstName, LastName, "FGA Home Teams","FGA Visitor Teams", "FTA Home Teams","FTA Visitor Teams" FROM officials
                                                      WHERE FirstName = (?) AND LastName = (?)
                                                  """, (officials_dict['FIRST_NAME'][i],officials_dict['LAST_NAME'][i],))
        off_params.append(cursor.fetchall()[0])
    cursor.execute("""SELECT FTA,FGA,FT_PCT,FG_PCT FROM team_stats_home
                                                      WHERE TEAM_ID = (?)
                                                  """, (home,))
    fta_home, fga_home, ft_pct_home,fg_pct_home = cursor.fetchall()[0]
    cursor.execute("""SELECT FTA,FGA,FT_PCT,FG_PCT FROM team_stats_away
                                                          WHERE TEAM_ID = (?)
                                                      """, (guest,))

    fta_away, fga_away, ft_pct_away, fg_pct_away = cursor.fetchall()[0]
    home_pts = fg_pct_home*(((off_params[0][2]+off_params[1][2]+off_params[2][2])/3 + fga_home)/2 - fga_home)
    away_pts = fg_pct_away * (((off_params[0][3] + off_params[1][3] + off_params[2][3]) / 3 + fga_away) / 2 - fga_away)
    home_fts = ft_pct_home * (((off_params[0][4] + off_params[1][4] + off_params[2][4]) / 3 + fta_home) / 2 - fta_home)
    away_fts = ft_pct_away * (((off_params[0][5] + off_params[1][5] + off_params[2][5]) / 3 + fta_away) / 2 - fta_away)
    score_home=score_home+home_pts+home_fts
    score_away=score_away+away_pts+away_fts

    return score_home,score_away,home,guest

def get_clutch(score_home, score_away,home,guest):
    if np.abs(score_home-score_away)<=4:
        clutch_dict_home = league.TeamStatsByClucth(measure_type=MeasureType.Default,team_id=home,point_diff=PointDiff.Less5p).overall().to_dict()
        clutch_dict_away = league.TeamStatsByClucth(measure_type=MeasureType.Default,team_id=guest,
                                                    point_diff=PointDiff.Less5p).overall().to_dict()
        score_home+=clutch_dict_home['PLUS_MINUS'][0]
        score_away+=clutch_dict_away['PLUS_MINUS'][0]
    return  score_home,score_away


def get_reb(score_home, score_away,home,guest):

    connect = sqlite3.connect("nbadb.db")
    cursor = connect.cursor()
    cursor.execute("""SELECT OREB_PCT,DREB_PCT,REB,FGM,FGA, FG_PCT FROM team_adv_stats
                                                          INNER JOIN team_stats ON team_stats.TEAM_ID = team_adv_stats.TEAM_ID     
                                                          WHERE team_adv_stats.TEAM_ID = (?) 
                                                      """, (home,))
    home_o_reb,home_d_reb,reb_home_total,home_fgm,home_fga, home_fg_pct = cursor.fetchall()[0]
    cursor.execute("""SELECT OREB_PCT,DREB_PCT,REB,FGM,FGA, FG_PCT FROM team_adv_stats
                                                              INNER JOIN team_stats ON team_stats.TEAM_ID = team_adv_stats.TEAM_ID     
                                                              WHERE team_adv_stats.TEAM_ID = (?) 
                                                          """, (guest,))
    away_o_reb, away_d_reb, away_total,away_fgm, away_fga,away_fg_pct = cursor.fetchall()[0]
    score_home+=home_fg_pct*(home_fgm-home_fga)*(home_o_reb-(1-away_d_reb))
    score_away+=away_fg_pct*(away_fgm-away_fga)*(away_o_reb-(1-home_d_reb))
    return score_home,score_away,home,guest
