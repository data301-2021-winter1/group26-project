#Task 3

import pandas as pd 
import numpy as np
import seaborn as sns

start_year = '2006'

def load_and_process(data_csv):
    
    #load data, drop irrelevant columns and drop NaN rows if any
    df1 = (
            pd.read_csv(data_csv)
            .drop(['name', 'genres', 'appid', 'english', 'developer', 'publisher', 'required_age', 'platforms', 'achievements', 'categories', 
'steamspy_tags', 'positive_ratings', 'negative_ratings', 'average_playtime', 'median_playtime', 'owners'], axis=1)
            .dropna(axis=0)
            .reset_index(drop=True)
            )

    #drop free games and games with a price more than 80 as these games are unnecessary and will affect the results
    df2 = (
            df1
            .drop(df1[df1.price > 80].index)
            .drop(df1[df1.price == 0].index)
            .reset_index(drop=True)
            )

    #convert exact release date to only the release year, remove games from before 2006 as there is insufficient data and sort rows by year
    #also drop 2019 data as it is incomplete
    df3 = (
            df2
            .assign(release_date = [int(i.split('-')[0]) for i in df2['release_date']])
            .drop(df2[df2.release_date < start_year].index)
            .drop(df2[df2.release_date >= '2019'].index)
            .sort_values(by='release_date', ascending=True)
            .reset_index()
            )
            

    return df3

def create_new_dataframe(df3):
    
    #the code below creates lists of the years, the amount of games, the average prices, the most expensive game price,
    #the least expensive game price, the amount of expensive games, the amount of cheap games and the percentage of cheap games.
    years = []
    added_price = []
    game_count = []
    average_price = []
    starting_year = int(start_year)
    max_price = []
    min_price = []
    expensive_games = []
    cheap_games = []
    cheap_game_percent = []

    for x in range(2019 - starting_year):   
        years.append(starting_year + x)
        added_price.append(0)
        game_count.append(0)
        average_price.append(0)
        max_price.append(0)
        min_price.append(100)
        expensive_games.append(0)
        cheap_games.append(0)
        cheap_game_percent.append(0)
        for y in range(len(df3)):
            if df3['release_date'][y] == x + starting_year:
                if df3['price'][y] > 49:
                    expensive_games[x] = expensive_games[x] + 1
                if df3['price'][y] > max_price[x]:
                    max_price[x] = df3['price'][y]
                if df3['price'][y] < 5:
                    cheap_games[x] = cheap_games[x] + 1
                if df3['price'][y] < min_price[x]:
                    min_price[x] = df3['price'][y]
                added_price[x] = added_price[x] + df3['price'][y]
                game_count[x] = game_count[x] + 1
        if game_count[x] != 0:
            average_price[x] = added_price[x] / game_count[x]
            cheap_game_percent[x] = (cheap_games[x] / game_count[x]) * 100

    #create a dictionary of the new lists
    d = {"Year": years, "Game Count": game_count, "Average Price": average_price, "Max Price": max_price, 
     "Min Price": min_price, "Over $49": expensive_games, "Under $5": cheap_games, "Cheap Game Percent": cheap_game_percent}

    #create new dataframe using dictionary
    df4 = pd.DataFrame(d)
    
    return df4