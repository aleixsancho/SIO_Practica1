import pandas as pd
import numpy as np

try:
    #Read the .csv file.
    data = pd.read_csv("../../dataset.csv", delimiter=";")

    #Create a Data Frame with the user name and an identifier starts with 1.
    client_df = pd.DataFrame(data, columns=['USERS', 'ID'])
    client_df['USERS'] = data['DATASET']
    client_df['ID'] = np.arange(1, len(client_df)+1)

    # Create a Data Frame with the restaurant name and an identifier starts with 1.
    restaurant_names = pd.DataFrame(data.iloc[0]).iloc[1:]
    restaurant_df = pd.DataFrame(restaurant_names, columns=['ID']).rename_axis('RESTAURANT').reset_index()
    restaurant_df['ID'] = np.arange(1, len(restaurant_names) + 1)

    #Create a Data Frame with each user repeated for all the restaurants.
    """
    REST_ID
    1
    ..
    1
    2
    ..
    2
    len = all users * 100 
    Every user appears 100 times (1 for restaurant).   
    """
    client_id = pd.DataFrame(np.repeat(client_df['ID'].values,100, axis=0))
    client_id = pd.DataFrame(client_id.values, columns=['USER_ID']).reset_index()

    #Create a Data Frame with all the restaurants repeated, to make the relation with 1 user and all the restaurants, and this for all users.
    """
    REST_ID
    1
    ..
    100
    1
    ..
    100
    len = all users * 100    
    """
    restaurant_id = pd.DataFrame(restaurant_df['ID']).rename(columns={"ID":"REST_ID"})
    restaurant_id = pd.concat([restaurant_id]*len(client_df)).reset_index()
    restaurant_id['index'] = np.arange(len(restaurant_id))

    relation_df = pd.merge(left=client_id, right=restaurant_id,  left_on='index', right_on='index')

    ratings_df = pd.DataFrame(data).T
    ratings_df = ratings_df.drop('DATASET').T
    ratings_df = pd.DataFrame(ratings_df.values.ravel(), columns=['RATINGS']).reset_index()

    relation_df = pd.merge(left=relation_df, right=ratings_df,  left_on='index', right_on='index')
    relation_df = relation_df.drop(['index'], axis=1)
    print(relation_df)

except FileNotFoundError:
    print('File does not exist.')

except Exception as error:
    print(error)