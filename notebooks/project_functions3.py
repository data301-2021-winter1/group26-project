import pandas as pd
import numpy as np

def clean_and_process(csv_file):
    df1 = (
          pd.read_csv(csv_file)
        .drop(['release_date','english', 'developer', 'publisher','platforms', 'required_age','achievements','average_playtime', 'median_playtime','price','name','appid'], axis =1)
        .rename(columns = {'categories':'Category', 'genres':'Genre','steamspy_tags':'Tags', 'positive_ratings':'Positive Reviews', 'negative_ratings':'Negative Reviews','owners':'Copies Sold'}, errors="raise")         
      )
    df1['Positive Percentage'] = df1['Positive Reviews'] /(df1['Negative Reviews']+df1['Positive Reviews'])
    return df1

def remove_low_performers(df):
    count = 0
    df1 = df.copy()
    for x in df['Copies Sold']:
        if(x=='0-20000'):
            df1 = df1.drop(count)
        count+=1
    df1 =df1.reset_index(drop=True)
    return df1

def genre_group(df):
    df1 =(df.assign(Genre=df['Genre'].str.split(';')).explode('Genre')
        .groupby('Genre').filter(lambda x : len(x) > 50)
        .reset_index(drop=True)
         )
    return df1

def tags_group(df):
    df1 = (
        df.assign(Tags=df['Tags'].str.split(';')).explode('Tags')
        .groupby('Tags').filter(lambda x : len(x) >= 200)
        .reset_index(drop=True)
        )
    return df1
