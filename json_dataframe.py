import pandas as pd
# import streamlit as st
from streamlit_autorefresh import st_autorefresh
from Multipage_AppFile.Crick_Buzz_Analysis.pages.cbrapid_api import call_rapid

def json_normlZer(df):
    df_n=pd.json_normalize(df)
    return df_n

def json_exploder(dfEXP):
    df_explode= dfEXP.explode()  
    df_norm= json_normlZer(df_explode)
    return df_norm

def fn_exploder(df_obj):
    df_exp= df_obj.explode()
    return df_exp

url_2 = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/recent"

# @st.cache_data(ttl=12 * 60 * 60)
def fn_json_automator():
    return call_rapid(url=url_2) # Recent matches data

# st_autorefresh(interval = 12 * 60 * 60 * 1000, limit= 2, key="refresh")

json_recent= fn_json_automator()



def json_rec_N():
    json_recent_N= json_normlZer(json_recent['typeMatches']) # Normalise "raw_json"  based on key - "typeMatches"
    return json_recent_N


json_recent_N2 = json_rec_N()
json_international =json_recent_N2['seriesMatches'][json_recent_N2['matchType']=="International"]
json_domestic =json_recent_N2['seriesMatches'][json_recent_N2['matchType']=="Domestic"]
json_league =json_recent_N2['seriesMatches'][json_recent_N2['matchType']=="League"]
json_women =json_recent_N2['seriesMatches'][json_recent_N2['matchType']=="Women"]



def new_series_entry():
    for i in json_recent_N2['matchType'].unique:
        if i!= "International" or i!= "Domestic" or i!= "League" or i!= "Women":
            json_NewEntry = json_recent_N2['seriesMatches'][json_recent_N2['matchType']==i]
            df_NewEntry_exp= json_exploder(json_NewEntry) 
            df_NewEntry_exp_N = json_exploder(df_NewEntry_exp['seriesAdWrapper.matches']) 
            df_rec_NewEntry = pd.DataFrame(df_rec_NewEntry)
            return df_rec_NewEntry


def date_converter(df, colms_date, cols_bools = None):
    for i in colms_date: #enumerate
        if i in df.columns:
            df[i] = pd.to_numeric(df[i], errors='coerce')
            df[i] = pd.to_datetime(df[i], unit='ms')
            df[i] = df[i].fillna((pd.Timestamp('1970-01-01')))
        
        for ilk in cols_bools:
            if ilk and ilk in df.columns and ilk != 'NA':
                df[ilk] = df[ilk].fillna(value=0).astype(int)
                df= df.astype({ilk:int}, errors='ignore')
    return df

class all_recent_matchDt():
    def __init__(self):
        pass
    # Operations for "International" matches recent data
    def fn_rec_international(self):
        df_international_exp= json_exploder(json_international) 
        df_international_exp_N = json_exploder(df_international_exp['seriesAdWrapper.matches']) 
        df_rec_international = pd.DataFrame(df_international_exp_N)
        df_rec_international= date_converter(df_rec_international, colms_date=["matchInfo.startDate", "matchInfo.endDate",
                                                                               "matchInfo.seriesStartDt","matchInfo.seriesEndDt"], 
                                                                               cols_bools = ['matchInfo.isTournament','matchInfo_isTimeAnnounced'])
        df_rec_international.columns=(
            df_rec_international.columns.str.replace('.', '_', regex=False)
            .str.replace('-', '_', regex=False)
            .str.replace("'", "", regex=False)
            .str.replace('"', "", regex=False)
            .str.replace("''", "", regex=False)
            )
        df_rec_international= df_rec_international.dropna(subset=['matchInfo_matchId'])
        return df_rec_international

    # Operations for "Domestic" matches recent data
    def fn_rec_domestic(self):
        df_Domestic_exp= json_exploder(json_domestic) 
        df_Domestic_exp_N = json_exploder(df_Domestic_exp['seriesAdWrapper.matches']) 
        df_rec_domestic = pd.DataFrame(df_Domestic_exp_N)
        df_rec_domestic = date_converter(df_rec_domestic, colms_date=["matchInfo.startDate", "matchInfo.endDate",
                                                                               "matchInfo.seriesStartDt","matchInfo.seriesEndDt"], 
                                                                               cols_bools = ['matchInfo.isTournament','matchInfo_isTimeAnnounced'])
        df_rec_domestic.columns=(
            df_rec_domestic.columns.str.replace('.', '_', regex=False)
            .str.replace('-', '_', regex=False)
            .str.replace("'", "", regex=False)
            .str.replace('"', "", regex=False)
            .str.replace("''", "", regex=False)
            )
        df_rec_domestic=df_rec_domestic.dropna(subset=['matchInfo_matchId'])
        return df_rec_domestic

    # Operations for "League" matches recent data
    def fn_rec_league(self):
        df_League_exp= json_exploder(json_league) 
        df_League_exp_N = json_exploder(df_League_exp['seriesAdWrapper.matches']) 
        df_rec_league = pd.DataFrame(df_League_exp_N)
        df_rec_league = date_converter(df_rec_league, colms_date=["matchInfo.startDate", "matchInfo.endDate",
                                                                               "matchInfo.seriesStartDt","matchInfo.seriesEndDt"], 
                                                                               cols_bools = ['matchInfo.isTournament','matchInfo_isTimeAnnounced'])
        df_rec_league.columns=(
            df_rec_league.columns.str.replace('.', '_', regex=False)
            .str.replace('-', '_', regex=False)
            .str.replace("'", "", regex=False)
            .str.replace('"', "", regex=False)
            .str.replace("''", "", regex=False)
            )
        df_rec_league=df_rec_league.dropna(subset=['matchInfo_matchId'])
        return df_rec_league

    # Operations for "Women" matches recent data
    def fn_rec_women(self):
        df_Women_exp= json_exploder(json_women) 
        df_Women_exp_N = json_exploder(df_Women_exp['seriesAdWrapper.matches']) 
        df_rec_women = pd.DataFrame(df_Women_exp_N)
        df_rec_women = date_converter(df_rec_women, colms_date=["matchInfo.startDate", "matchInfo.endDate",
                                                                               "matchInfo.seriesStartDt","matchInfo.seriesEndDt"], 
                                                                               cols_bools = ['matchInfo.isTournament','matchInfo_isTimeAnnounced'])
        df_rec_women.columns=(
            df_rec_women.columns.str.replace('.', '_', regex=False)
            .str.replace('-', '_', regex=False)
            .str.replace("'", "", regex=False)
            .str.replace('"', "", regex=False)
            .str.replace("''", "", regex=False)
            )
        df_rec_women=df_rec_women.dropna(subset=['matchInfo_matchId'])
        return df_rec_women
    

# team_details= all_recent_matchDt().fn_teamData()
# print(f"The Json Is ::::::: {team_details['teamName']}")
    

# json_live =call_rapid(url=url_1)

 


# match_type = json_live_N['matchType']

# match True:
#     case _ if "International" in match_type:
#         json_lv_international = json_live_N['seriesMatches']
#     case _ if "Domestic" in match_type:
#         json_lv_domestic = json_live_N['seriesMatches']
#     case _ if "League" in match_type:
#         json_lv_league = json_live_N['seriesMatches']
#     case _ if "Women" in match_type:
#         json_lv_women = json_live_N['seriesMatches']







# all_match_types
    
# st.write(all_match_types)

# st.dataframe(df_rec_international)




# D:\Data Analytics\Streamlit_tutorial\Practice\.venv\Scripts\python.exe

# D:\Data Analytics\Streamlit_tutorial\Practice\Multipage_AppFile\Crick_Buzz_Analysis\pages\json_dataframe.py