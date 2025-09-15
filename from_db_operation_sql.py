import mysql.connector as My_conn
import pandas as pd
from Multipage_AppFile.Crick_Buzz_Analysis.pages.cb_sql_conn import db_puller

#connection for pulling data from "Crick_biz" table
my_db_puller=db_puller(database='Crick_biz', host='localhost',user='lab001DA', password='labMySql_pro', port='3306')

puller_con, puller_cursor=my_db_puller.connection_myAdminP()


class venu_players():
    def __init__(self):
        pass
    def fn_venu_maker(self):# function for creating listed venus 
        ven_query='''SELECT matchInfo_venueInfo_id AS venu_ID, 
                    matchInfo_venueInfo_ground AS VENU_NAME,
                    matchInfo_venueInfo_latitude as latitude,
                    matchInfo_venueInfo_longitude as longitude
                    FROM international_series_matches
                    UNION
                    SELECT matchInfo_venueInfo_id AS venu_ID, matchInfo_venueInfo_ground AS VENU_NAME,
                    matchInfo_venueInfo_latitude as latitude,
                    matchInfo_venueInfo_longitude as longitude
                    FROM women_series_matches
                    UNION 
                    SELECT matchInfo_venueInfo_id AS venu_ID, matchInfo_venueInfo_ground AS VENU_NAME,
                    matchInfo_venueInfo_latitude as latitude,
                    matchInfo_venueInfo_longitude as longitude
                    FROM league_series_matches
                    UNION 
                    SELECT matchInfo_venueInfo_id AS venu_ID, matchInfo_venueInfo_ground AS VENU_NAME,
                    matchInfo_venueInfo_latitude as latitude,
                    matchInfo_venueInfo_longitude as longitude 
                    FROM domestic_series_matches;
                    '''
        puller_cursor.execute(ven_query)
        rows = puller_cursor.fetchall()
        df_venu =pd.DataFrame(rows, columns=['venu_ID','VENU_NAME','latitude','longitude'])
        puller_con.commit()
        return df_venu
    
    def fn_venu_sql_table(self):
        return None