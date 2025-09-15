from apscheduler.schedulers.background import BackgroundScheduler
# from Multipage_AppFile.Crick_Buzz_Analysis.pages.json_dataframe import all_recent_matchDt
from Multipage_AppFile.Crick_Buzz_Analysis.pages.sql_operations import sql_ddl_dml
# from Multipage_AppFile.Crick_Buzz_Analysis.pg_admin_pages.pg_sql_opp import pgsql_ddl_dml
import streamlit as st

# recent_matches_raw= all_recent_matchDt()
# inter_N_matches = recent_matches_raw.fn_rec_international()

recent_matches_sql= sql_ddl_dml()

def automate_recent_matche():
    recent_matches_sql.table_name_formation()
    st.write("table created")
    recent_matches_sql.table_insert()
    if recent_matches_sql.table_insert():
        st.write("Data are inserted")


if __name__== "__main__":
    automate_recent_matche()

    myScheduler =BackgroundScheduler()
    myScheduler.add_job(func=automate_recent_matche, trigger='interval', hours=3)
    myScheduler.start()


# D:\Data Analytics\Streamlit_tutorial\Practice\Multipage_AppFile\Crick_Buzz_Analysis\pages\bg_automation.py
# streamlit run bg_automation.py
# .venv\Scripts\Activate.ps1
# __init__.py.bin
# cd "D:\Data Analytics\Streamlit_tutorial\Practice" streamlit run Multipage_AppFile/Crick_Buzz_Analysis/pages/bg_automation.py
# pip show streamlit
# .venv\Scripts\pip install streamlit --upgrade streamlit