import pandas as pd
import numpy as np
import seaborn as sns

def load_and_process(path):
    # Method Chain 1: LOAD DATA
    dfc = (pd
           .read_csv(path)
           .dropna(axis=0)
           .reset_index(drop=True)
          )
    
    # Method Chain 2: CLEAN DATA
    dfc = (dfc
           .drop(["appid", "release_date", "english", "developer", "publisher", "required_age", "platforms", "achievements", "name", "categories", "genres", "steamspy_tags"], axis=1)
           .assign(owners=[int((int(i.split('-')[0]) + int(i.split('-')[1])) / 2) for i in dfc["owners"]])
           .reset_index(drop=True)
          )
    
    # have to do drops seperately so that they don't crash method chains
    # dropping games with prices higher than $80 as that is the current maximum market trend for triple-A games
    # dropping games with playercount less than 15,000 because games that small are more likely to have 'cult followings' and therefore very skewed results with hyperbolic reviews
    # dropping games where the median playtime is greater than 5000 hours because those cases are definitely outliers
    dfc = dfc.drop(dfc[dfc.price > 80].index)
    dfc = dfc.drop(dfc[dfc.owners < 15000].index)
    dfc = dfc.drop(dfc[dfc.median_playtime > 5000].index).reset_index(drop=True)

    # Method Chain 3: PROCESS DATA
    # have to do total ratings assignment before the positive/negative assignment as the index doesn't exist until the statement completes
    dfc = dfc.assign(total_ratings=[dfc["positive_ratings"][i] + dfc["negative_ratings"][i] for i in range(dfc.shape[0])])
    dfc = (dfc
           .assign(positive_percent=[dfc["positive_ratings"][i] / dfc["total_ratings"][i] * 100 for i in range(dfc.shape[0])])
           .assign(negative_percent=[dfc["negative_ratings"][i] / dfc["total_ratings"][i] * 100 for i in range(dfc.shape[0])])
          )

    # WRANGLE/EXPORT DATA
    #dfc.to_csv("../data/processed/analysis1.csv")
    return dfc