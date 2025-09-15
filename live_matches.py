import pandas as pd
import streamlit as st
import altair as alt
import matplotlib.pyplot as plt
from streamlit_autorefresh import st_autorefresh
from Multipage_AppFile.Crick_Buzz_Analysis.pages.cbrapid_api import call_rapid,call_rapid_2
from Multipage_AppFile.Crick_Buzz_Analysis.pages.json_handeller_classes.norm_explode import json_magic
from Multipage_AppFile.Crick_Buzz_Analysis.pages.from_db_operation_sql import venu_players
st.set_page_config(layout= "wide")

# ************************ ##################### ************************ #
# AREA FOR FUNCTION CREATION

#creating function for 
def fn_live_payer_score(bat_1:str,bat_2:str, 
                        R_1: int,R_2: int, 
                        F_1: int,F_2: int, 
                        S_1: int,S_2: int, 
                        ball_1,ball_2):
    
    """
    bat_1,bat_2: Batsman 1 & 2 Name;  R_1,R_2: Batters Runs;
    F_1,F_2: No of 4;  S_1,S_2: No of 6;
    ball_1,ball_2: In balls;
    """
    player_stat={
        "Batter":[bat_1,bat_2],
        "Run":[R_1,R_2],
        "4s":[F_1,F_2],
        "6s":[S_1,S_2],
        "Balls":[ball_1,ball_2]
     }
    df=pd.DataFrame(player_stat)
    return df

#creating function for 
def fn_score_player(match_id):
    url_match_player=f"https://cricbuzz-cricket2.p.rapidapi.com/mcenter/v1/{match_id}/scard"
    return call_rapid_2(url= url_match_player)

#creating function for numeric convertion
def fn_numeric_converter(df):
    for cols in df.columns.tolist():
        df[cols]=pd.to_numeric(df[cols],errors="coerce",downcast='integer')
    return df

# ************************ ##################### ************************ #
# AREA FOR VARIABLE AND OBJECTS CREATION

venu_n_players=venu_players()
venu_all=venu_n_players.fn_venu_maker()

json_handel=json_magic()

st.markdown("### Live Stats Page")

# ************************ ##################### ************************ #
# AREA FOR JSON LIVE MATCHES DATA FETCHING

url_1 = "https://cricbuzz-cricket2.p.rapidapi.com/matches/v1/live" #URL for importing from
try:
    josn_live = call_rapid_2(url=url_1)
    json_live_N= pd.json_normalize(josn_live)
    df_exp_lv= json_handel.json_exploder(json_live_N['typeMatches'])
    df_exp_N_lv = json_handel.json_exploder(df_exp_lv['seriesMatches']).dropna(subset=['seriesAdWrapper.seriesName'])
    # st.write(json_live_N)
    # st.write(df_exp_lv)
    # st.write(df_exp_N_lv)
except Exception as error_e:
    st.json(error_e)
    st.write("Please try after sometime")

# ************************ ##################### ************************ #
#Creating Class for exporting the series id and name
class live_series_exporter():
    def __init__(self):
        pass
    def fn_series_id_exporter(self):
        s_id_lst= df_exp_N_lv['seriesAdWrapper.seriesId'].unique().tolist()
        return  s_id_lst
    def fn_series_name_exporter(self):
        s_name_lst= df_exp_N_lv['seriesAdWrapper.seriesName'].unique().tolist()
        return s_name_lst

# ************************ ##################### ************************ #
# "matchInfo.matchId"-> Primary Key of matches dataset 

all_match_types_exp =df_exp_N_lv['seriesAdWrapper.seriesName'].unique().tolist()
options=st.sidebar.selectbox("Select The Match",
                             options= all_match_types_exp, index= 0
                             )
#Select box for match name
# if options in all_match_types_exp:
st.cache_data(ttl=12 * 60 * 60)
df_live_m = json_handel.json_exploder(df_exp_N_lv[df_exp_N_lv['seriesAdWrapper.seriesName']==options]['seriesAdWrapper.matches'])
df_live_m.columns=(
        df_live_m.columns.str.replace(r'[.,"\'-]', '_', regex=True))


df_live_m['matchInfo_venueInfo_latitude']=pd.to_numeric(df_live_m['matchInfo_venueInfo_latitude'], errors= "coerce")
df_live_m['matchInfo_venueInfo_longitude']=pd.to_numeric(df_live_m['matchInfo_venueInfo_longitude'], errors= "coerce")

df_live_m['matchInfo_startDate']=pd.to_numeric(df_live_m['matchInfo_startDate'], errors= "coerce")
df_live_m['matchInfo_startDate']=pd.to_datetime(df_live_m['matchInfo_startDate'], unit='ms')

df_live_m['matchInfo_endDate']=pd.to_numeric(df_live_m['matchInfo_endDate'], errors= "coerce")
df_live_m['matchInfo_endDate']=pd.to_datetime(df_live_m['matchInfo_endDate'], unit='ms')

#Radio button for match status
radio_option=df_live_m['matchInfo_state'].unique().tolist()
option2=st.sidebar.radio(label= "Match Status", options= radio_option, index= 0)
df_live_m2= df_live_m[df_live_m ['matchInfo_state']== option2]
df_live_m2=df_live_m2.dropna(subset=['matchInfo_matchId'])

# ************************ ##################### ************************ #
# options=st.sidebar.selectbox("Select The Match",options= ['International','Domestic','Women','League'], index= None)


df_live_m2['matchInfo_venueInfo_latitude']=pd.to_numeric(df_live_m2['matchInfo_venueInfo_latitude'], errors='coerce')
df_live_m2['matchInfo_venueInfo_longitude']=pd.to_numeric(df_live_m2['matchInfo_venueInfo_longitude'], errors='coerce')
# # st.dataframe(venu_all)
# st.dataframe(df_live_m2)

# ************************ ##################### ************************ #
# Getting data for each player score
player_score_json=fn_score_player(df_live_m2['matchInfo_matchId'].iloc[0]) 
score_datea = pd.json_normalize(player_score_json['scorecard'])
score_batsman=json_handel.json_exploder(score_datea['batsman'])
score_bowler=json_handel.json_exploder(score_datea['bowler'])

score_batsman[['runs','balls','fours','sixes','strkrate']]=fn_numeric_converter(score_batsman[['runs','balls','fours','sixes','strkrate']])
score_bowler[['balls','overs','runs','maidens','wickets']]=fn_numeric_converter(score_bowler[['balls','overs','runs','maidens','wickets']])

# ************************ ##################### ************************ #

# ************************ ##################### ************************ #
if option2=="In Progress":
    cols1, cols2 = st.columns(spec=[1.75,3.25], gap="small", border= True)
    with cols1:

        # Create two different code for status "completed", "In Progress" ************************
        
            st.markdown(f"##### ***{options}:*** *{df_live_m2['matchInfo_venueInfo_ground'].iloc[0]}*")
            with st.container(border= True, width= "stretch",horizontal_alignment="center"):
                st.markdown(f"""<h5 style= "color:black"; text-align:center;>{df_live_m2['matchInfo_team1_teamName'].iloc[0]}   -   {df_live_m2['matchScore_team1Score_inngs1_runs'].iloc[0]}   |   {df_live_m2['matchScore_team1Score_inngs1_wickets'].iloc[0]}(W)   |   {df_live_m2['matchScore_team1Score_inngs1_overs'].iloc[0]}(O) </h5>
                            """, 
                            width="stretch", unsafe_allow_html =True
                            )
            with st.container(border= True, width= "stretch",horizontal_alignment="center"):
                st.markdown(f"""
                            <h5 style= "color:black"; text-align:center;>{df_live_m2['matchInfo_team2_teamName'].iloc[0]}   -   {df_live_m2['matchScore_team2Score_inngs1_runs'].iloc[0]}   |   {df_live_m2['matchScore_team2Score_inngs1_wickets'].iloc[0]}(W)  |   {df_live_m2['matchScore_team2Score_inngs1_overs'].iloc[0]}(O) </h5>""",
                            width="stretch", unsafe_allow_html =True
                            )
            current_batters=score_batsman[score_batsman['outdec']=='batting'].copy()
            if len(current_batters) >= 2:
                bats_stats=fn_live_payer_score(bat_1= current_batters['name'].iloc[0], bat_2= current_batters['name'].iloc[1],
                                R_1= current_batters['runs'].iloc[0], R_2= current_batters['runs'].iloc[1],
                                F_1= current_batters['fours'].iloc[0], F_2= current_batters['fours'].iloc[1],
                                S_1= current_batters['sixes'].iloc[0], S_2= current_batters['sixes'].iloc[1],
                                ball_1= current_batters['balls'].iloc[0], ball_2= current_batters['balls'].iloc[1]
                            )
            else:
                bats_stats=fn_live_payer_score(bat_1= current_batters['name'].iloc[0], bat_2= None,
                                R_1= current_batters['runs'].iloc[0], R_2= None,
                                F_1= current_batters['fours'].iloc[0], F_2= None,
                                S_1= current_batters['sixes'].iloc[0], S_2= None,
                                ball_1= current_batters['balls'].iloc[0], ball_2= None
                                )

                                
            st.dataframe(bats_stats,hide_index=True)
            score_show_bts= score_batsman[['name','runs','balls','fours','sixes','strkrate','outdec']].copy()
            score_show_balls= score_bowler[['name','balls','overs','runs','maidens','wickets']].copy()
            with st.expander(label="Batsman Stats"):
                st.dataframe(score_show_bts,hide_index=True)
            with st.expander(label="Bowler Stats"):
                st.dataframe(score_show_balls,hide_index=True)
            # st.map(data=df_live_m2, latitude='matchInfo_venueInfo_latitude', longitude='matchInfo_venueInfo_longitude', color="#DB930C",size=55)
    with cols2:
        with st.expander("Batters Stats Graph"):
            bar= alt.Chart(data=score_show_bts).mark_bar(color="#2B6BF3").encode(x="name",y="runs")
            line=alt.Chart(data= score_show_bts).mark_bar(color="#EC4F64FF",filled= True,cornerRadius= 5).encode(x="name",y="balls")
            combo= bar + line
            st.altair_chart(combo,use_container_width=True)

        with st.expander("Bowlers Stats Graph"):
            ball_bar= alt.Chart(data=score_show_balls).mark_bar(color="#2B6BF3").encode(x="name",y="overs")
            ball_line=alt.Chart(data= score_show_balls).mark_bar(color="#EC4F64FF",filled= True,cornerRadius= 5).encode(x="name",y="wickets")
            ball_combo= ball_bar + ball_line
            st.altair_chart(ball_combo, use_container_width=True)

        bats_stats=fn_live_payer_score(bat_1= current_batters['name'].iloc[0], bat_2= current_batters['name'].iloc[1],
                        R_1= current_batters['runs'].iloc[0], R_2= current_batters['runs'].iloc[1],
                        F_1= current_batters['fours'].iloc[0], F_2= current_batters['fours'].iloc[1],
                        S_1= current_batters['sixes'].iloc[0], S_2= current_batters['sixes'].iloc[1],
                        ball_1= current_batters['balls'].iloc[0], ball_2= current_batters['balls'].iloc[1]
                        )
        figs, axes = plt.subplots(1, 4, figsize=(10, 3.5))
        # Plot Runs
        axes[0].bar(bats_stats["Batter"].tolist(), bats_stats["Run"].tolist())
        axes[0].set_title("Runs Stats")
        axes[0].tick_params(axis='x', rotation=45)

        # Plot Balls
        axes[1].bar(bats_stats["Batter"].tolist(), bats_stats["Balls"].tolist())
        axes[1].set_title("Balls Stats")
        axes[1].tick_params(axis='x', rotation=45) 

        # Plot 4s
        axes[2].bar(bats_stats["Batter"].tolist(), bats_stats["4s"].tolist())
        axes[2].set_title("Four Stats")
        axes[2].tick_params(axis='x', rotation=45) 


        # Plot 6s
        axes[3].bar(bats_stats["Batter"].tolist(), bats_stats["6s"].tolist())
        axes[3].set_title("Six Stats")
        axes[3].tick_params(axis='x', rotation=45) 

        plt.tight_layout()

        # Show in Streamlit
        st.pyplot(figs)




elif option2=="Complete" or option2=="Stumps" : #or 
    cols1_1, cols2_2 = st.columns(spec=[2,3], gap="small", border= True)
    list_matchId= df_live_m2['matchInfo_matchId'].tolist()
    i_col=0
    for i_col in range(df_live_m2.shape[i_col]):
        player_scr_json=fn_score_player(df_live_m2['matchInfo_matchId'].iloc[i_col]) 
        score_dt = pd.json_normalize(player_scr_json['scorecard'])
        score_batsM=pd.DataFrame(json_handel.json_exploder(score_dt['batsman']) )
        # st.dataframe(df_live_m2.columns)
        # score_bowler=pd.DataFrame(json_handel.json_exploder(score_datea['bowler']) )
        with cols1_1:
            st.markdown(f"##### *{df_live_m2['matchInfo_seriesName'].iloc[i_col]}*")
            with st.container(border= True, width= "stretch",horizontal_alignment="center"):
                st.markdown(f"""
                            <h5 style= "color:black";text-align:center;>{df_live_m2['matchInfo_team1_teamName'].iloc[i_col]}  -  {df_live_m2['matchScore_team1Score_inngs1_runs'].iloc[i_col]}   |   {df_live_m2['matchScore_team1Score_inngs1_wickets'].iloc[i_col]}(W)   |   {df_live_m2['matchScore_team1Score_inngs1_overs'].iloc[i_col]}(O) </h5>
                            """, 
                            width="stretch", unsafe_allow_html =True
                            )
            with st.container(border= True, width= "stretch",horizontal_alignment="center"):
                if "matchInfo_team2_teamName" in df_live_m2.columns and "matchScore_team2Score_inngs1_runs" in df_live_m2.columns and "matchScore_team2Score_inngs1_wickets" in df_live_m2.columns:
                    st.markdown(f"""
                                <h5 style= "color:black";text-align:center;>{df_live_m2['matchInfo_team2_teamName'].iloc[i_col]}   -   {df_live_m2['matchScore_team2Score_inngs1_runs'].iloc[i_col]}   |   {df_live_m2['matchScore_team2Score_inngs1_wickets'].iloc[i_col]}(W)  |   {df_live_m2['matchScore_team2Score_inngs1_overs'].iloc[i_col]}(O) </h5>""",
                                width="stretch", unsafe_allow_html =True
                                )
                else:
                    st.markdown(f"""<h5 style= "color:black";text-align:center;>No Data Avilable</h5>""", width="stretch", unsafe_allow_html =True)
            score_show= score_batsM[['name','runs','balls','fours','sixes','strkrate','outdec']].copy()
            # with st.expander(label="Players Stats"):
            #     st.dataframe(score_show)
            st.map(data=df_live_m2, latitude='matchInfo_venueInfo_latitude', longitude='matchInfo_venueInfo_longitude', color="#DB930C",size=55)

        with cols2_2:
            with st.container():
                st.markdown(f"##### *{df_live_m2['matchInfo_seriesName'].iloc[i_col]}*")
                st.bar_chart(data=score_show, x = "name",y= ["runs","balls"],color=["#2667F1","#1A27DF"])
            # bar= alt.Chart(data=score_show).mark_bar(color="#2B6BF3").encode(x="name",y="runs")
            # line=alt.Chart(data= score_show).mark_bar(color="#EC4F64FF",filled= True,cornerRadius= 5).encode(x="name",y="balls")
            # combo= bar + line
            # st.altair_chart(combo,use_container_width=True)
        i_col+=1 


elif option2=="Innings Break":
    cols3_1, cols3_2 = st.columns(spec=[2,3], gap="small", border= True)
    list_matchId_3= df_live_m2['matchInfo_matchId'].tolist()
    i_col=0
    for i_col in range(df_live_m2.shape[i_col]):
        player_scr_json=fn_score_player(df_live_m2['matchInfo_matchId'].iloc[i_col]) 
        score_dt = pd.json_normalize(player_scr_json['scorecard'])
        score_batsM=pd.DataFrame(json_handel.json_exploder(score_dt['batsman']) )
        # score_bowler=pd.DataFrame(json_handel.json_exploder(score_datea['bowler']) )
        with cols3_1:
            st.markdown(f"##### *{df_live_m2['matchInfo_seriesName'].iloc[i_col]}*")
            with st.container(border= True, width= "stretch",horizontal_alignment="center"):
                st.markdown(f"""
                            <h5 style= "color:black";text-align:center;>{df_live_m2['matchInfo_team1_teamName'].iloc[i_col]}  -  {df_live_m2['matchScore_team1Score_inngs1_runs'].iloc[i_col]}   |   {df_live_m2['matchScore_team1Score_inngs1_wickets'].iloc[i_col]}(W)   |   {df_live_m2['matchScore_team1Score_inngs1_overs'].iloc[i_col]}(O) </h5>
                            """, 
                            width="stretch", unsafe_allow_html =True
                            )
            # with st.container(border= True, width= "stretch",horizontal_alignment="center"):
            #     st.markdown(f"""
            #                 <h5 style= "color:black";text-align:center;>{df_live_m2['matchInfo_team2_teamName'].iloc[i_col]}   -   {df_live_m2['matchScore_team2Score_inngs1_runs'].iloc[i_col]}   |   {df_live_m2['matchScore_team2Score_inngs1_wickets'].iloc[i_col]}(W)  |   {df_live_m2['matchScore_team2Score_inngs1_overs'].iloc[i_col]}(O) </h5>""",
            #                 width="stretch", unsafe_allow_html =True
            #                 )
            score_show_3= score_batsM[['name','runs','balls','fours','sixes','strkrate','outdec']].copy()
            with st.expander(label="Players Stats"):
                st.dataframe(score_show_3)
            # st.map(data=df_live_m2.iloc[i_col], latitude='matchInfo_venueInfo_latitude', longitude='matchInfo_venueInfo_longitude', color="#DB930C",size=55)

        with cols3_2:
            with st.container():
                st.markdown(f"##### *{df_live_m2['matchInfo_seriesName'].iloc[i_col]}*")
                st.bar_chart(data=score_show_3, x = "name",y= ["runs","balls"],color=["#2667F1","#1A27DF"])
            # bar= alt.Chart(data=score_show).mark_bar(color="#2B6BF3").encode(x="name",y="runs")
            # line=alt.Chart(data= score_show).mark_bar(color="#EC4F64FF",filled= True,cornerRadius= 5).encode(x="name",y="balls")
            # combo= bar + line
            # st.altair_chart(combo,use_container_width=True)
        i_col+=1 

    



# <div style="background-color: lightblue; padding: 5px; border-radius: 5px;"> 
# D:\Data Analytics\Streamlit_tutorial\Practice\Multipage_AppFile\Crick_Buzz_Analysis\pages\live_matches.py