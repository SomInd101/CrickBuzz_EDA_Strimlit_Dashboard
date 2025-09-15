import pandas as pd
import streamlit as st
from Multipage_AppFile.Crick_Buzz_Analysis.pages.cbrapid_api import call_rapid
from Multipage_AppFile.Crick_Buzz_Analysis.pages.from_db_operation_sql import venu_players

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


venus_sl=venu_players()
venu_initial= venus_sl.fn_venu_maker()
venu_ids=venu_initial['venu_ID'].unique()

url_venu = "https://cricbuzz-cricket.p.rapidapi.com/venues/v1/66"
url_plyer = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/6635"


@st.cache_data(ttl=12 * 60 * 60)
# RETURN JSON FILE OF ALL VENU DETAILS
def fn_venuJSON():
    return call_rapid(url= url_venu)

# RETURN JSON FILE OF ALL PLAYERS DETAILS
def fn_playersSTATIC():
    return call_rapid(url=url_plyer)

venu_jsonF=fn_venuJSON()
player_jsonF=fn_playersSTATIC()



class venu_players_opp():

    def __init__(self):
        pass
     
    def venu_dataframe(self):
        df_venu =json_normlZer(venu_jsonF)
        return df_venu
    
    def players_dataframe(self):
        all_players =json_normlZer(player_jsonF)
        df_players=json_exploder(all_players['teamNameIds'])
        return all_players, df_players
    
data_class= venu_players_opp()


venu_coldata=data_class.venu_dataframe()
venu_column= venu_coldata.columns
venu_column= venu_column.insert(0,'Venu_Id')

# creating variables for collecting the venus columns name
# single time run calls 29 API calls because of the 29 venu ID
class venu_players_puller():

    def __init__(self):
        pass

    def Venu_puller(self): # single time run calls 29 API calls because of the 29 venu ID
        venu_lst=[]
        for idx in enumerate(venu_ids):
            Dynamic_url_venu = f"https://cricbuzz-cricket.p.rapidapi.com/venues/v1/{idx}"
            json_Vdata= call_rapid(url= Dynamic_url_venu)
            dyn_df_venu= json_normlZer(json_Vdata)
            dyn_df_venu['Venu_Id']= pd.DataFrame(idx)
            # new_venu_list=dyn_df_venu.values.tolist()
            venu_lst.append(dyn_df_venu.values)
            
        venu_all= [items for sublist in venu_lst for items in sublist]
        venu_df=pd.DataFrame([items for sublist in venu_lst for items in sublist], columns=venu_column)
        # venu_df=venu_df.merge(venu_initial, left_on='Venu_Id', right_on='venu_ID')
        # venu_df.drop(columns=['VENU_NAME','venu_ID'], inplace=True)
        return venu_df
    

venu_df_cls=venu_players_puller()
st.dataframe(venu_df_cls.Venu_puller())


st.dataframe(venu_initial)

venu_initial= venus_sl.fn_venu_maker()
st.write(venu_initial.columns)
st.write(venu_column)





# st.write(venu_lst)

# player_raw, players_IdName= data_class.players_dataframe()
# st.write(data_class.venu_dataframe())
# st.write(player_raw)
# st.write(players_IdName)
# st.write(player_jsonF)
# st.write(venu_jsonF)

# D:\Data Analytics\Streamlit_tutorial\Practice\Multipage_AppFile\Crick_Buzz_Analysis\pages\venu_players_info.py