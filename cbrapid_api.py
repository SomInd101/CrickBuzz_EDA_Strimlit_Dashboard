import streamlit as st
import requests
# url_in ="https://cricbuzz-cricket.p.rapidapi.com/teams/v1/international"

def call_rapid(url):
    headers = {'x-rapidapi-key': "c31604d990msh3cdca1efe31f760p13ab31jsnb7625dd29998",
               'x-rapidapi-host': "cricbuzz-cricket.p.rapidapi.com"
                 }
    response =requests.get(url,headers=headers)
    raw_json= response.json()
    # print(raw_json)
    return raw_json

def call_rapid_2(url):
    headers = {'x-rapidapi-key': "c31604d990msh3cdca1efe31f760p13ab31jsnb7625dd29998",
               'x-rapidapi-host': "cricbuzz-cricket2.p.rapidapi.com"
                 }
    response =requests.get(url,headers=headers)
    raw_json2= response.json()
    # print(raw_json)
    return raw_json2

# print(call_rapid(url=url_in))

# schedule.every(12).hours.do(json_df)
# while True:
#     schedule.run_pending()
#     time.sleep(1)


# @st.cache_data(ttl=12 * 60 * 60)
# def json_df():
#     json_recent =call_rapid(url= url_)
#     return json_recent

# st_autorefresh(interval = 12 * 60 * 60 * 1000, limit= 2, key="refresh")
# automating the task

# url =

# D:\Data Analytics\Streamlit_tutorial\Practice\Multipage_AppFile\Crick_Buzz_Analysis\pages\cbrapid_api.py