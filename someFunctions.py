import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

housing = pd.read_csv("housing.csv")

#housing.hist(bins=50, figsize=(20,15))
#plt.show()

#print(housing.head(5))

def split_train_test(data, test_ratio):
    np.random.seed(42)
    shuffled_indices = np.random.permutation(len(data))
    test_set_size = int(len(data) * test_ratio)
    test_indices = shuffled_indices[:test_set_size]
    train_indices = shuffled_indices[test_set_size:]
    return data.iloc[train_indices], data.iloc[test_indices]

def display_scores(scores):
    #print("scores:", scores)
    print("mean:", scores.mean())
    print("standard deviation:", scores.std())
