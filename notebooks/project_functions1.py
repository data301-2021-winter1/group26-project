import pandas as pd
import numpy as np
import seaborn as sns

def load_and_process(path):
    # Method Chain 1: LOAD DATA
    dfc = (pd.read_csv(path)
           .dropna(axis=0)
           .reset_index(drop=True)
          )

    # Method Chain 2: CLEAN DATA
    dfc = (dfc
           .drop(["appid", "release_date", "english", "developer", "publisher", "required_age", "platforms", "achievements", "name", "categories", "genres", "steamspy_tags"], axis=1)
           .assign(owners=[int((int(i.split('-')[0]) + int(i.split('-')[1])) / 2) for i in dfc["owners"]])
           .reset_index(drop=True)
          )

    # Method Chain 3: PROCESS DATA
    dfc = (dfc
           .assign(positive_percent=[dfc["positive_ratings"][i] / (dfc["positive_ratings"][i] + dfc["negative_ratings"][i]) * 100 for i in range(dfc.shape[0])])
           .assign(negative_percent=[dfc["negative_ratings"][i] / (dfc["positive_ratings"][i] + dfc["negative_ratings"][i]) * 100 for i in range(dfc.shape[0])])
           .drop(dfc[dfc.price > 80].index)
           .reset_index()
          )

    # WRANGLE/EXPORT DATA
    #dfc.to_csv("../data/processed/analysis1.csv")
    return dfc