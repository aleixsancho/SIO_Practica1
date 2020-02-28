import pandas as pd
import numpy as np

try:
    data = pd.read_csv("../../dataset.csv", delimiter=";")
    client_df = pd.DataFrame(data, columns=['DATASET', 'ID'])
    client_df['ID'] = np.arange(1, len(client_df)+1)
    print(client_df.head())


except FileNotFoundError as error:
    print('File does not exist.')
