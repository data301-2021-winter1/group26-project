import pandas as pd
import numpy as np

#Disclaimer: Some of this code may be messy/inefficient, I apologize as I did not attend any of the lab sections for help, mind you not because I don't think I needed the help but because I like to see if I can figure things out for myself by googling. I find that I learn a lot more by searching for the answer myself even if I do come across a lot of jank solutions, if you have a slow pc, I thank you for your patience.

def clean_and_process(csv_file):
    #This function will drop all the columns I am not using, rename them to look nicer, create a new column that is a ratio of pos and neg ratings, and finally remove any low owner count games
    df1 = (
        pd.read_csv(csv_file)
        .drop(['release_date','english', 'developer', 'publisher','platforms', 'required_age','achievements','average_playtime', 'median_playtime','price','name','appid','categories'], axis =1)
        .rename(columns = {'genres':'Genre','steamspy_tags':'Tags', 'positive_ratings':'Positive Reviews', 'negative_ratings':'Negative Reviews','owners':'Copies Sold'}, errors="raise")         
        )
    df1['Positive Percentage'] = df1['Positive Reviews'] /(df1['Negative Reviews']+df1['Positive Reviews'])
    df1 = remove_low_performers(df1)
    return df1

def remove_low_performers(df):
    #This function will remove all games who have less than 20000 owners, I need to do this to make sure the positive percentage does not get skewed by games with only a few reviews and all positive or negative as their ratio is weighted equally to those with thousands of reviews.
    count = 0
    df1 = df.copy()
    for x in df['Copies Sold']:
        if(x=='0-20000'):
            df1 = df1.drop(count)
        count+=1
    df1 =df1.reset_index(drop=True)
    return df1

def genre_group(df):
    #Splits apart on the genre column, then removes any genre that appears 50 times or less.
    df1 =(df.assign(Genre=df['Genre'].str.split(';')).explode('Genre')
        .groupby('Genre').filter(lambda x : len(x) > 50)
        .reset_index(drop=True)
         )
    return df1

def tags_group(df):
       #Splits apart on the tags column, then removes any tag that appears less than 200 times.
    df1 = (
        df.assign(Tags=df['Tags'].str.split(';')).explode('Tags')
        .groupby('Tags').filter(lambda x : len(x) >= 200)
        .reset_index(drop=True)
        )
    return df1
