import pandas as pd
import os
df = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../Dataset/dish.csv"))
def getDataset():
    return df;