import pandas as pd

#this class is made for normalising the json files

class json_magic():
    def __init__(self):
        pass
    def json_normlZer(self, df):
        df=self.df
        df_n=pd.json_normalize(df)
        return df_n

    def json_exploder(self, dfEXP):
        df_explode = dfEXP.explode()  
        df_norm= pd.json_normalize(df_explode)
        return df_norm

    def fn_exploder(self, df_obj):
        df_obj=self.df_obj
        df_exp= df_obj.explode()
        return df_exp