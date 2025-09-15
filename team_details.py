import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh
from Multipage_AppFile.Crick_Buzz_Analysis.pages.cbrapid_api import call_rapid
from Multipage_AppFile.Crick_Buzz_Analysis.pages.json_dataframe import json_normlZer, json_exploder,fn_exploder

url_matchID="https://cricbuzz-cricket.p.rapidapi.com/teams/v1/international"

@st.cache_data(ttl=12 * 60 * 60)
def fn_matchID_automator():
    return call_rapid(url= url_matchID)
def fn_score_player(match_id):
    url_match_player=f"https://cricbuzz-cricket.p.rapidapi.com/mcenter/v1/{match_id}/scard"
    return call_rapid(url= url_match_player)

json_team_details=fn_matchID_automator() #holds json data of teams
json_match_score= fn_score_player()

class team_class():
    def __init__(self):
        pass
    def fn_teamData(self):
        team_data= json_normlZer(json_team_details['list'])
        team_dataPD=pd.DataFrame(team_data)
        team_dataPD.columns=(
            team_dataPD.columns.str.replace(r'[.,"\'\'-]', '_', regex=True)
            )
        return team_dataPD
    
    def fn_player_scoreZ(self):
        score_datea = pd.json_normalize(json_match_score['scorecard'])
        score_datea.columns=(score_datea.columns.str.replace(r'[.,"\'\'-]', '_', regex=True))
        score_batsman=json_exploder(score_datea['batsman'])
        score_bowler=json_exploder(score_datea['bowler'])
        fow_data=json_exploder(score_datea['fow_fow'])
        partnership_data=json_exploder(score_datea['partnership_partnership'])
        return score_datea, score_batsman,score_bowler, fow_data, partnership_data
    
# match_score=team_class().fn_player_scoreZ()

# print(f"The match score is - ::::::: {match_score}")

# D:\Data Analytics\Streamlit_tutorial\Practice\Multipage_AppFile\Crick_Buzz_Analysis\pages\team_details.py