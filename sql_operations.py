import mysql.connector as My_conn
import pandas as pd
import streamlit as st
from Multipage_AppFile.Crick_Buzz_Analysis.pages.cb_sql_conn import sql_oper
from Multipage_AppFile.Crick_Buzz_Analysis.pages.json_dataframe import json_rec_N,all_recent_matchDt, new_series_entry
from Multipage_AppFile.Crick_Buzz_Analysis.pages.team_details import team_class
from Multipage_AppFile.Crick_Buzz_Analysis.pages.venu_players_info import venu_players_opp

sql_opp= sql_oper(host='localhost',user='lab001DA', password='labMySql_pro', port='3306', allow_local_infile= True)
conn, cursor = sql_opp.connection_myAdmin()

team_players=team_class()
venu_players=venu_players_opp()

#dat
#create instance/object of json_rec_N() from json_dataframe
series_name_Holder= json_rec_N()
series_lst =series_name_Holder['matchType'].unique()

#create instance/object of all_recent_matchDt() from json_dataframe
series_data_Holder = all_recent_matchDt()
team_data = team_players.fn_teamData() #holds data of team/countryname

df_matches={}
for i in series_lst:
    if i== "International":
        international_match = series_data_Holder.fn_rec_international()
        international_match = international_match.dropna(subset=['matchInfo_matchId'])
    elif i== "League":
        league_matches = series_data_Holder.fn_rec_league()
        league_matches = league_matches.dropna(subset=['matchInfo_matchId'])
    elif i== "Domestic":
        domestic_matches = series_data_Holder.fn_rec_domestic()
        domestic_matches = domestic_matches.dropna(subset=['matchInfo_matchId'])
    elif i== "Women":
        women_matches = series_data_Holder.fn_rec_women()
        domestic_matches=domestic_matches.dropna(subset=['matchInfo_matchId'])
    else:
        keys=i
        df_matches[keys] = series_data_Holder.new_series_entry()


# Creatiing a custom map function for Mysql Tabels data type:
def map_pandas_dtype_Mysql(dtype):
    if pd.api.types.is_integer_dtype(dtype):
        return 'INT'
    if pd.api.types.is_float_dtype(dtype):
        return 'FLOAT'
    if pd.api.types.is_bool_dtype(dtype):
        return 'BOOLEAN'
    if pd.api.types.is_datetime64_ns_dtype:
        # return 'DATETIME'
        return 'VARCHAR(60)' # is_datetime64_any_dtype(dtype)
    if pd.api.types.is_object_dtype(dtype):
        return 'VARCHAR(75)'
    else:
        return 'VARCHAR(75)'
    

# extracting columns and their datatypes based on the series type matches data ----->
columns_tab_intn = international_match.columns
dtype_tab_intn = international_match.dtypes

columns_tab_lg =league_matches.columns
dtype_tab_lg =league_matches.dtypes

columns_tab_dom =domestic_matches.columns
dtype_tab_dom =domestic_matches.dtypes

columns_tab_wom =women_matches.columns
dtype_tab_wom =women_matches.dtypes


#Custom Class for SQL DDL/ DML Operations:
class sql_ddl_dml():

    def __init__(self):
        pass
    def table_name_formation(self):
        for tab_name in series_lst:
        #creating table based on the series type ----->
        # 1:
            if tab_name == "International":
                column_array =[]
                for colz, dtypz in zip(columns_tab_intn, dtype_tab_intn):
                    map_dtypes= map_pandas_dtype_Mysql(dtype=dtypz)
                    if colz == 'matchInfo_matchId':
                        column_array.append(f"{colz} {map_dtypes} PRIMARY KEY")
                    else:
                        column_array.append(f"{colz} {map_dtypes}")
                
                sql_columns=','.join(column_array)

                if conn is not None and cursor is not None:
                    try:
                        query1= f"""CREATE TABLE IF NOT EXISTS {tab_name}_Series_Matches ({sql_columns});"""
                        cursor.execute(query1)
                        conn.commit()
                    except Exception as erroR:
                        return st.write(erroR)
            
        # 2:
            elif tab_name == "Women":
                column_array =[]
                for colz, dtypz in zip(columns_tab_wom, dtype_tab_wom):
            
                    map_dtypes= map_pandas_dtype_Mysql(dtype=dtypz)
                    if colz == 'matchInfo_matchId':
                        column_array.append(f"{colz} {map_dtypes} PRIMARY KEY")
                    else:
                        column_array.append(f"{colz} {map_dtypes}")

                sql_columns=','.join(column_array)

                if conn is not None and cursor is not None:
                    try:
                        query1= f"""CREATE TABLE IF NOT EXISTS {tab_name}_Series_Matches ({sql_columns});"""
                        cursor.execute(query1)
                        conn.commit()
                    except Exception as erroR:
                        return st.write(erroR)
            
        # 3:
            elif tab_name == "League":
                column_array =[]
                for colz, dtypz in zip(columns_tab_lg, dtype_tab_lg):
            
                    map_dtypes= map_pandas_dtype_Mysql(dtype=dtypz)
                    if colz == 'matchInfo_matchId':
                        column_array.append(f"{colz} {map_dtypes} PRIMARY KEY")
                    else:
                        column_array.append(f"{colz} {map_dtypes}")
                    
                sql_columns=','.join(column_array)
                if conn is not None and cursor is not None:
                    try:
                        query1= f"""CREATE TABLE IF NOT EXISTS {tab_name}_Series_Matches ({sql_columns});"""
                        cursor.execute(query1)
                        conn.commit()
                        
                    except Exception as erroR:
                        return st.write(erroR)
            
        # 4:
            elif tab_name == "Domestic":
                column_array =[]
                for colz, dtypz in zip(columns_tab_dom, dtype_tab_dom):
            
                    map_dtypes= map_pandas_dtype_Mysql(dtype=dtypz)
                    if colz == 'matchInfo_matchId':
                        column_array.append(f"{colz} {map_dtypes} PRIMARY KEY")
                    else:
                        column_array.append(f"{colz} {map_dtypes}")
                    
                sql_columns=','.join(column_array)
                if conn is not None and cursor is not None:
                    try:
                        query1= f"""CREATE TABLE IF NOT EXISTS {tab_name}_Series_Matches ({sql_columns});"""
                        cursor.execute(query1)
                        conn.commit()
                        
                    except Exception as erroR:
                        return st.write(erroR)
    
    #Function for inserting the data into the tables
    def table_insert(self):
        for tab_namz in series_lst:
        # 1:
            if tab_namz =='International':
                if conn is not None and cursor is not None:
                    # dynamic_values=[] # holds the data "%s" in list format
                    cols_insert= columns_tab_intn.tolist() # holds the columns names in list format
                    dynamic_valuesI =', '.join(['%s']*len(columns_tab_intn.tolist()))
                    tab_name=f"{tab_namz}_Series_Matches"
                    sql_cols =','.join(cols_insert)
                    try:
                        data= international_match.values.tolist() # data is two dimentional array 
                        query_insert=f"""INSERT INTO {tab_name} ({sql_cols}) 
                        VALUES ({dynamic_valuesI}) 
                        ON DUPLICATE KEY UPDATE matchInfo_matchId = matchInfo_matchId;
                        """
                    # data is two dimentional array 
                    # # tuple(str(val) if pd.notnull(val) else '' for val in ros) - Replace NaN with empty string within each rows values
                        data_execute= [tuple(val if pd.notnull(val) else None for val in ros) for ros in data]
                        cursor.executemany(query_insert, data_execute)
 
                        conn.commit()
                        print(f"Inserted {cursor.rowcount} rows into {tab_name}")
                    except Exception as erroR:
                        print(f"Error inserting into {tab_name}: {erroR}")


                    # finally:
                    #     cursor.close()

        # 2:
            elif tab_namz =='Women':
                if conn is not None and cursor is not None:
                    cols_insert= columns_tab_wom.tolist() # holds the columns names in list format
                    sql_cols=','.join(cols_insert)
                    dynamic_valuesW=', '.join(['%s']*len(cols_insert)) # holds the data "%s" in list format
                    tab_nameW=f"{tab_namz}_Series_Matches"
                    
                    try:
                        data= women_matches.values.tolist()
                        query_insert=f'''INSERT INTO {tab_nameW} ({sql_cols}) 
                        VALUES({dynamic_valuesW}) 
                        ON DUPLICATE KEY UPDATE matchInfo_matchId = matchInfo_matchId;'''
                    
                        data_executeW=[tuple(valu if pd.notnull(valu) else None for valu in rows) for rows in data]
                        cursor.executemany(query_insert, data_executeW)
                        conn.commit()
                    except Exception as erroR:
                        print(f"Error inserting into {tab_nameW}: {erroR}")
            
        # 3:
            elif tab_namz =='League':
                if conn is not None and cursor is not None:
                    cols_insert= columns_tab_lg.tolist() # holds the columns names in list format
                    sql_cols=','.join(cols_insert)
                    sql_dynValL=', '.join(['%s']*len(cols_insert))
                    tab_nameL=f"{tab_namz}_Series_Matches"

                    try:
                        data= league_matches.values.tolist()
                        query_insert=f'''
                        INSERT INTO {tab_nameL} ({sql_cols}) 
                        VALUES({sql_dynValL}) 
                        ON DUPLICATE KEY UPDATE matchInfo_matchId = matchInfo_matchId;'''
                        data_executeL= [tuple(val if pd.notnull(val) else None for val in rows) for rows in data]
                        cursor.executemany(query_insert, data_executeL)
                        conn.commit()
                    except Exception as erroR:
                        print(f"Error inserting into {tab_nameL}: {erroR}")

        # 4:
            elif tab_namz =='Domestic':
                if conn is not None and cursor is not None:
                    cols_insert= columns_tab_dom.tolist() # holds the columns names in list format
                    sql_cols=','.join(cols_insert) # formatting into STR format
                    # dynamic_values=[] # holds the data "%s" in list format
                    sql_dynValD=','.join(['%s']*len(cols_insert))
                    tab_nameD=f"{tab_namz}_Series_Matches"

                    try:
                        data= domestic_matches.values.tolist()
                        query_insert=f'''
                        INSERT INTO {tab_nameD} ({sql_cols}) values({sql_dynValD}) 
                        ON DUPLICATE KEY UPDATE matchInfo_matchId = matchInfo_matchId;'''
                        
                        data_executeD=[tuple(val if pd.notnull(val) else None for val in rows) for rows in data]
                        cursor.executemany(query_insert, data_executeD)
                        conn.commit()
                    except Exception as erroR:
                        print(f"Error inserting into {tab_nameD}: {erroR}")



        



# pt_class= sql_ddl_dml()
# pt_class.table_name_formation()
    # def table_name_formation(self):    
        
    
    # query= f"""CREATE TABLE IF NOT EXISTS {tab_name}_Series_Matches(Series_types_mt varchar))"""
    #             cursor.execute(query)





# conn1, cursor1= sql_opp.connection_myAdmin()
# cursor1.execute(""" Select * from T1""")
# rows_my =cursor1.fetchall()
# df_emp= pd.DataFrame(rows_my, columns=['EmployeeID','Name','DepartmentID','Designation','JoiningDate','Salary'])
# st.dataframe(df_emp)

# D:\Data Analytics\Streamlit_tutorial\Practice\Multipage_AppFile\Crick_Buzz_Analysis\pages\sql_operations.py
# Dashboard Design - https://www.youtube.com/watch?v=eqJteRHsfn0