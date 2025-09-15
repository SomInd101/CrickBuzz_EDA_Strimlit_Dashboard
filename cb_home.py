import pandas as pd
import streamlit as st
st.markdown("### Home Page")
from Multipage_AppFile.Crick_Buzz_Analysis.pages.json_dataframe import json_rec_N, json_exploder
st.set_page_config(layout = 'wide', initial_sidebar_state = "auto")

json_recent_N=json_rec_N()
json_recent_N['matchType']= json_recent_N['matchType'].dropna()
# Creating Sidebar based on the Crecket Types
all_match_types_exp =[mt for mt in json_recent_N['matchType']] 
option = st.sidebar.selectbox("Select Cricket Types", options= all_match_types_exp, index = 1)

if option in all_match_types_exp:
    json_df=json_recent_N['seriesMatches'][json_recent_N['matchType']== option]

# json_exploder() 1st explode the Json list type the Normalize it
    df_exp= json_exploder(json_df) 
    df_exp_N = json_exploder(df_exp['seriesAdWrapper.matches'])
    df_exp_P = pd.DataFrame(df_exp_N)

    # Converting and Properly formatting the Date colums
    # # step 1- converting into Numeric
    df_exp_P['matchInfo.startDate'] = pd.to_numeric(df_exp_P['matchInfo.startDate'], errors='coerce')
    df_exp_P['matchInfo.endDate'] = pd.to_numeric(df_exp_P['matchInfo.endDate'], errors='coerce')
    df_exp_P['matchInfo.seriesStartDt'] = pd.to_numeric(df_exp_P['matchInfo.seriesStartDt'], errors='coerce')
    df_exp_P['matchInfo.seriesEndDt'] = pd.to_numeric(df_exp_P['matchInfo.seriesEndDt'], errors='coerce')

    # # step 2- converting into Date format
    df_exp_P['matchInfo.startDate'] = pd.to_datetime(df_exp_P['matchInfo.startDate'], unit='ms')
    df_exp_P['matchInfo.endDate'] = pd.to_datetime(df_exp_P['matchInfo.endDate'], unit='ms')
    df_exp_P['matchInfo.seriesStartDt'] = pd.to_datetime(df_exp_P['matchInfo.seriesStartDt'], unit='ms')
    df_exp_P['matchInfo.seriesEndDt'] = pd.to_datetime(df_exp_P['matchInfo.seriesEndDt'], unit='ms')

    # # Converting to Numeric latitude, longitude colums:
    # df_exp_P['matchInfo.venueInfo.latitude'] = pd.to_numeric(df_exp_P['matchInfo.venueInfo.latitude'], errors='coerce')
    # df_exp_P['matchInfo.venueInfo.longitude'] = pd.to_numeric(df_exp_P['matchInfo.venueInfo.longitude'], errors='coerce')
    df_exp_P['matchInfo.venueInfo.latitude'] = df_exp_P['matchInfo.venueInfo.latitude'].astype('float')
    df_exp_P['matchInfo.venueInfo.longitude'] = df_exp_P['matchInfo.venueInfo.longitude'].astype('float')

    df_shows= df_exp_P[['matchInfo.seriesName','matchInfo.team1.teamName',
                        'matchInfo.team2.teamName','matchInfo.status','matchInfo.startDate',
                        'matchScore.team1Score.inngs1.runs','matchScore.team1Score.inngs1.wickets','matchScore.team1Score.inngs1.overs',
                        'matchScore.team2Score.inngs1.runs','matchScore.team2Score.inngs1.wickets','matchScore.team2Score.inngs1.overs',
                        'matchInfo.endDate','matchInfo.venueInfo.ground','matchInfo.venueInfo.latitude','matchInfo.venueInfo.longitude']].copy()
    
    # Selecting Unique values from seriesName
    value = df_exp_P['matchInfo.seriesName'].unique()
    matched_options = [nesT for nesT in value ]
    pick_option= st.sidebar.selectbox("Select Series Name", options= matched_options, index= None)
    df_rec = pd.DataFrame(df_shows[df_shows['matchInfo.seriesName']==pick_option],
                          columns=['matchInfo.team1.teamName',
                        'matchInfo.team2.teamName','matchInfo.status','matchInfo.startDate',
                        'matchScore.team1Score.inngs1.runs','matchScore.team1Score.inngs1.wickets','matchScore.team1Score.inngs1.overs',
                        'matchScore.team2Score.inngs1.runs','matchScore.team2Score.inngs1.wickets','matchScore.team2Score.inngs1.overs',
                        'matchInfo.endDate'])



    team_u= pd.concat([df_rec['matchInfo.team1.teamName'], 
                       df_rec['matchInfo.team2.teamName']],ignore_index=False)
    df_u =pd.DataFrame(team_u, columns=['select_team'])
    
    if pick_option in matched_options:
        multi_secLst= df_u['select_team'].unique()
        op1= st.sidebar.selectbox("Select Team", options= multi_secLst, index= None)
    
        if op1 in multi_secLst:
            df_ms1= df_rec[
            (df_rec['matchInfo.team1.teamName']== op1)|
            (df_rec['matchInfo.team2.teamName']== op1)
            ] 
            st.dataframe(df_ms1)
        else:
            st.dataframe(df_rec)
        # st.expander()
        # df_rec.shape[0]
    else:
        df_rec = pd.DataFrame(df_shows)
        st.dataframe(df_rec)
        st.map(df_rec, latitude = 'matchInfo.venueInfo.latitude', longitude = 'matchInfo.venueInfo.longitude', 
               color="#F31717", zoom= 2)