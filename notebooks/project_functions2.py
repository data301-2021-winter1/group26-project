#Task 3

import pandas as pd 
import numpy as np
import seaborn as sns

start_year = '2006'

def load_and_process(data_csv):
    
    #load data, drop irrelevant columns and drop NaN rows if any
    df1 = (pd.read_csv(data_csv)
            .drop(['name', 'genres', 'appid', 'english', 'developer', 'publisher', 'required_age', 'platforms', 'achievements', 'categories', 
'steamspy_tags', 'positive_ratings', 'negative_ratings', 'average_playtime', 'median_playtime', 'owners'], axis=1)
            .dropna(axis=0)
            .reset_index(drop=True)
          )

    #drop free games and games with a price more than 100 as these games are unnecessary and will affect the results
    df2 = (df1
            .drop(df1[df1.price > 100].index)
            .drop(df1[df1.price == 0].index)
            .reset_index(drop=True)
          )

    #convert exact release date to just the release year and remove games from before 2006 as there is insufficient data 
    df3 = (df2
            .assign(release_date = [int(i.split('-')[0]) for i in df2["release_date"]])
            .sort_values(by='release_date', ascending=True)
            .drop(df2[df2.release_date < start_year].index)
            .reset_index()
          )

    #the code below creates lists of the years, the amount of games, the sum of game prices and the average prices
    #it is messy and probably not the best way to do this but it works
    years = []
    added_price = []
    game_count = []
    average_price = []
    starting_year = int(start_year)

    for x in range(2020 - starting_year):   
        years.append(starting_year + x)
        added_price.append(0)
        game_count.append(0)
        average_price.append(0)
        for y in range(len(df3)):
            if df3['release_date'][y] == x + starting_year:
                added_price[x] = added_price[x] + df3['price'][y]
                game_count[x] = game_count[x] + 1
        if game_count[x] != 0:
            average_price[x] = added_price[x] / game_count[x]

    #create a dictionary of the new lists
    d = {"Year": years, "Game_Count": game_count, "Price_Sum": added_price, "Price_Average": average_price}

    #create dataframe using dictionary
    df4 = pd.DataFrame(d)

    return df4