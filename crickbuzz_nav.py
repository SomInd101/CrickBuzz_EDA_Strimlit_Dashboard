import pandas as pd
import streamlit as st

# Home = st.Page(
#     page = "Multipage_AppFile/Crick_Buzz_Analysis/pages/cb_home.py",
#     title = "Home Page",
#     icon = ":material/home_work:")

live_matches= st.Page(
    page = "Multipage_AppFile/Crick_Buzz_Analysis/pages/live_matches.py", 
                      title = "Live Matches", 
                      icon = ":material/stream:")

top_stats = st.Page(page = "Multipage_AppFile/Crick_Buzz_Analysis/pages/statsTop.py", 
                                  title = "Top Match Stats", 
                                  icon = ":material/analytics:")
pg_nav= st.navigation(pages=[live_matches, top_stats], position='top')
pg_nav.run()

# D:\Data Analytics\Streamlit_tutorial\Practice\crickbuzz_nav.py
# D:\Data Analytics\Streamlit_tutorial\Practice\.venv\Scripts\Activate.ps1
# D:\Data Analytics\Streamlit_tutorial\Practice\Multipage_AppFile\Crick_Buzz_Analysis\pages\stats_top.py
# D:\Data Analytics\Streamlit_tutorial\Practice\.venv\Scripts\python.exe


# Dashboard Design - https://www.youtube.com/watch?v=eqJteRHsfn0