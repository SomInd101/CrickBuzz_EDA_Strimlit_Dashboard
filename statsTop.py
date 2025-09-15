import pandas as pd
import streamlit as st
st.set_page_config(layout = 'wide', initial_sidebar_state= "auto")
from Multipage_AppFile.Crick_Buzz_Analysis.pages.https_operations.https_stats_puller import cls_htttp_puller



all_puller= cls_htttp_puller() #creating an object of "cls_htttp_puller()" class

final_player_puller=all_puller.fn_players_stats() # holds all bats and bowlers data for pulling the stats

final_baters_puller=all_puller.fn_baters_data_puller() # holds all baters data for pulling the stats

final_bowlers_puller=all_puller.fn_bowlers_data_puller # holds all bowlers data for pulling the stats

batting_sorting=all_puller.fn_internatinal_bts() # Batting Urls parameter and Shorting stats Name
bats_stats_name=batting_sorting['Series_param_pm'].tolist()

balling_sorting=all_puller.fn_internatinal_balls() # Balling Urls parameter and Shorting stats Name
balls_stats_name=balling_sorting['Series_param_pm'].tolist()


option_lst= final_player_puller['Series_Name'].unique().tolist()
series_option=st.sidebar.selectbox("Series Name", options= option_lst, index= 0) #don't make the index none it will show then error

batting_rdo_btn=st.sidebar.radio(label="Bats Stats", options=bats_stats_name, index=0)
balling_rdo_btn= st.sidebar.radio(label="Balling Stats", options=balls_stats_name, index=0)


if series_option in option_lst:
    st.markdown(f"### Top Stats: {str.capitalize(series_option)}")
    sorted_options_series= final_player_puller[final_player_puller['Series_Name']==series_option] #delete later

    # sorted_options_baters=final_baters_puller[final_baters_puller['Series_Name']== series_option]
    # sorted_options_baowlers=final_bowlers_puller[final_bowlers_puller['Series_Name']== series_option]
    # st.write(sorted_options_series)

    cols1, cols2= st.columns([1,1], gap= "small", 
                             vertical_alignment = "top", 
                             border = True, 
                             width = "stretch")
    with cols1:
        
        df_stats=sorted_options_series[sorted_options_series['Series_param_pm']==batting_rdo_btn]
        # st.write(df_stats)
        try:
            url=f"{df_stats['Stats_url_bats'].values[0]}"
            html_stats=pd.read_html(url, index_col="Unnamed: 0")
            df_stats=pd.DataFrame(html_stats[0])
            columns=df_stats.columns[0]
            avg_val=0
            for avg_val in range(df_stats.shape[0]):

                if "Avg" in columns and (df_stats['Avg'].iloc[avg_val] =='-'):
                    if "Matches" in columns:
                        df_stats['Avg']=df_stats['Runs']/df_stats['Matches']
                    else:
                        None
                avg_val+=1
            
            st.write(df_stats)
            multi_option= st.multiselect(label= "Select The data", options=df_stats.columns[1:], max_selections= 3, default=df_stats.columns[1])
            st.bar_chart(data=df_stats, x= columns, y= multi_option)
            
        except Exception as error:
            st.write(F"SORRY! NO DATA AVILABLE")
            print(f"The error is: {error}")

    with cols2:
        
        df_balls_stats=sorted_options_series[sorted_options_series['Series_param_pm']==balling_rdo_btn]
        # st.write(df_balls_stats)
        try:
            url_bals=f"{df_balls_stats['Stats_url_balls'].values[0]}"
            html_balling_stats=pd.read_html(url_bals, index_col="Unnamed: 0")
            df_ballling_stats=pd.DataFrame(html_balling_stats[0])
            st.write(df_ballling_stats)
            columns_balls=df_ballling_stats.columns[0]
            multi_option_balls= st.multiselect(label= "Select The data", options=df_ballling_stats.columns[1:], max_selections= 3, default=df_ballling_stats.columns[1])
            st.bar_chart(data=df_ballling_stats, x= columns_balls, y= multi_option_balls)
        except Exception as error:
            st.write(F"SORRY! NO DATA AVILABLE")
            print(f"The error is: {error}")
        
    
        












# ************************ ##################### ************************ #
# for _, sts_id in enumerate(arc_series_id_international):
#     for _, sts_param in enumerate(url_stats_param_batsU):
#         key= f"{sts_id}_{sts_param}"











# D:\Data Analytics\Streamlit_tutorial\Practice\Multipage_AppFile\Crick_Buzz_Analysis\pages\statsTop.py







# '''/* 
# matchInfo.matchId
# matchInfo.seriesId
# matchInfo.seriesName
# matchInfo.matchDesc
# matchInfo.matchFormat
# matchInfo.startDate
# matchInfo.endDate
# matchInfo.state
# matchInfo.status
# matchInfo.team1.teamId
# matchInfo.team1.teamName
# matchInfo.team1.teamSName
# matchInfo.team1.imageId
# matchInfo.team2.teamId
# matchInfo.team2.teamName
# matchInfo.team2.teamSName
# matchInfo.team2.imageId
# matchInfo.venueInfo.id
# matchInfo.venueInfo.ground
# matchInfo.venueInfo.city
# matchInfo.venueInfo.timezone
# matchInfo.venueInfo.latitude
# matchInfo.venueInfo.longitude
# matchInfo.currBatTeamId
# matchInfo.seriesStartDt
# matchInfo.seriesEndDt
# matchInfo.isTimeAnnounced
# matchInfo.stateTitle
# matchScore.team1Score.inngs1.inningsId
# matchScore.team1Score.inngs1.runs
# matchScore.team1Score.inngs1.wickets
# matchScore.team1Score.inngs1.overs
# matchScore.team2Score.inngs1.inningsId
# matchScore.team2Score.inngs1.runs
# matchScore.team2Score.inngs1.wickets
# matchScore.team2Score.inngs1.overs
# */'''
