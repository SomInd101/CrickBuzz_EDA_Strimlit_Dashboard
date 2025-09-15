import pandas as pd
import streamlit as st


arc_series_id_international=["10917","10587","10702"] #_international series ID
arc_series_name_international=["Mozambique tour of Eswatini 2025",
                               "Asia Cup 2025",
                               "ICC Womens T20 World Cup East Asia Pacific Qualifier 2025"]
arc_stats_URL_international=["https://www.cricbuzz.com/cricket-series/10917/mozambique-tour-of-eswatini-2025/stats",
                             "https://www.cricbuzz.com/cricket-series/10587/asia-cup-2025/stats",
                             "https://www.cricbuzz.com/cricket-series/10702/icc-womens-t20-world-cup-east-asia-pacific-qualifier-2025/stats"] # series URL for stats


url_stats_param_batsU=["most-runs","highest-score","highest-avg",
                       "highest-sr","most-hundreds","most-fifties",
                       "most-fours","most-sixes","most-nineties"] # Url parameter for bats scores
stats_param_bats_name= ["Most-runs","Highest-scores","Best-batting-average",
                        "Best-batting-strike-rate","Most-hundreds","Most-fifties",
                        "Most-fours","Most-sixes","Most-nineties"] # Calling parameter for bats scores

url_stats_param_ballsU=["most-wickets","lowest-avg","best-bowling-innings","most-five-wickets","lowest-econ","lowest-sr",] # Url parameter for balls scores
stats_param_balling_name= ["Most-wickets","Best Bowling Average",
                           "Best Bowling","Most 5 Wickets Haul",
                           "Best Economy","Best Bowling Strike Rate"]# Calling parameter for bowllers scores


rawdt_international={"Series_Name":arc_series_name_international,
              "Series_id":arc_series_id_international,
              "Series_URL":arc_stats_URL_international
              } #holds just data for liternational matche name,id
df_int_raw=pd.DataFrame(rawdt_international)


rawdt_international_bts={
              "Series_param":url_stats_param_batsU,
              "Series_param_pm":stats_param_bats_name
              } #holds just data for baters urls parameter and shorting Name

df_international_bts=pd.DataFrame(rawdt_international_bts)


rawdt_international_balls={
              "Series_param":url_stats_param_ballsU,
              "Series_param_pm":stats_param_balling_name
              } #holds just data for bowlers urls parameter and shorting Name

df_international_balls=pd.DataFrame(rawdt_international_balls)


class cls_htttp_puller():
    def __init__(self):
        pass

    def fn_bowlers_data_puller(self):
        url_stats_pullerBalls=[] # hold international bowllers data pulling urls
        for _, id_balls in enumerate(arc_series_id_international):

            for _, url_balls in enumerate(url_stats_param_ballsU):
                series_ballsurl=f"https://www.cricbuzz.com/api/html/series/{id_balls}/{url_balls}/0/0/0" # Url for table stats pulling International & T20
                url_stats_pullerBalls.append({
                    "series_id": id_balls,
                    "Stats_Param_Name": url_balls,
                    "Stats_url_balls": series_ballsurl
                    })
        stats_international_df_balls=pd.DataFrame(url_stats_pullerBalls) # creating the dataFrame for bowlers

        stats_international_df_balls=stats_international_df_balls.merge(df_int_raw, 
                                                              left_on="series_id", 
                                                              right_on="Series_id").drop(columns=['Series_id',
                                                                                                  'Series_URL'])

        stats_international_df_balls=stats_international_df_balls.merge(df_international_balls, 
                                                                    left_on="Stats_Param_Name", 
                                                                    right_on="Series_param").drop(columns=["Series_param",
                                                                                                            "Stats_Param_Name"]).rename(columns={"Series_param":"Stats_Param_Balls"})
        return stats_international_df_balls
    
    def fn_baters_data_puller(self):
        url_stats_pullerBTS=[] # hold international bats data pulling urls
        for _, id in enumerate(arc_series_id_international):
            for _, url_bts in enumerate(url_stats_param_batsU):
                series_btsurl=f"https://www.cricbuzz.com/api/html/series/{id}/{url_bts}/0/0/0" # Url for table stats pulling International & T20

                url_stats_pullerBTS.append({
                    "series_id": id,
                    "Stats_Param_Name": url_bts,
                    "Stats_url_bats": series_btsurl
                })

        stats_international_df_bats=pd.DataFrame(url_stats_pullerBTS) # creating the dataFrame for Batsman

        stats_international_df_bats=stats_international_df_bats.merge(df_int_raw, 
                                                              left_on="series_id", 
                                                              right_on="Series_id").drop(columns=['Series_id',
                                                                                                  'Series_URL'])
        stats_international_df_bats=stats_international_df_bats.merge(df_international_bts, 
                                                                    left_on="Stats_Param_Name", 
                                                                    right_on="Series_param").drop(columns=["Series_param",
                                                                                                            "Stats_Param_Name"]).rename(columns={"Series_param":"Stats_Param_Bats"})
        return stats_international_df_bats
    

    def fn_players_stats(self):
        stats_international_df_bats= cls_htttp_puller().fn_baters_data_puller()
        stats_international_df_balls= cls_htttp_puller().fn_bowlers_data_puller()
        df_mergeFinal=pd.concat([stats_international_df_bats, stats_international_df_balls]).fillna(value="NA")
        return df_mergeFinal
    
    def fn_internatinal_raw(self):
        return df_int_raw
    
    def fn_internatinal_bts(self):
        return df_international_bts
    
    def fn_internatinal_balls(self):
        return df_international_balls

