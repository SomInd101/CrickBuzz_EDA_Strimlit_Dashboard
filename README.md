# CrickBuzz_EDA_Strimlit_Dashboard

older & File Structure:
************************
Practice

        ipl_navigation.py
        
--| Multipage_AppFile

                    __init__.py
                    
--------------------| Crick_Buzz_Analysis

                                         __init__.py
                                         
----------------------------------------| pages

                                            ----__init__.py
                                            
                                            ----live_matches.py
                                            
                                            ----statsTop.py
                                            
                                            ----cbrapid_api.py
                                            
                                            ----cb_sql_conn.py
                                            
                                            ----json_dataframe.py
                                            
                                            ----sql_operations.py
                                            
                                            ----json_fetcher.ipynb
                                            
                                            ----from_db_operation_sql.py
                                            
                                            ----team_details.py
                                            
                                            ----venu_players_info.py
                                            
                                            ----bg_automation.py
                                            
                                                
--------------------------------------------------- | json_handeller_classes

                                                                        ---- norm_explode.py
                                                                        
--------------------------------------------------- | https_operations

                                                                  ---- https_stats_puller.py
                                                                  

cbrapid_api.py(fetched Json Data) -> 
-> json_fetcher.ipynb (Contain DataFrames of recent matches) Just for testing

cb_sql_conn.py -> Contain Class for establising connecting with MySQL dataBase

sql_operations.py-> for performing sql DDL operations

bg_automation.py-> For setting background operations

team_details.py -> For pulling team_details only

live_matches.py-> Pull data from live matches

statsTop.py-> Show matches top stats

json_dataframe.py-> Convert recent matches data into dataframes and data cleaning -----> ONLY USE IF YOU HAVE ENOUGH SUBSCRIPTION
from_db_operation_sql.py-> Pulls Data from database
venu_players_info.py-> Dynamically pulls running matches venu and players information-> ONLY USE IF YOU HAVE ENOUGH SUBSCRIPTION FOR API 
SINGLE RUNS WILL REQUEST MINIMUM 35+ FOR PULLING THE DATA.
