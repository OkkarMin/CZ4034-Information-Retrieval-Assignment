import pandas as pd

data = pd.read_csv("./data/all_unclassified_data.csv")

# Shuffle data in place and reset the index
data = data.sample(frac=1).reset_index(drop=True)

data.to_csv("./data/all_classified_data_shuffled.csv")