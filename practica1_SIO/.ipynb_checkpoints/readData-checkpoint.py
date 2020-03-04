import pandas as pd
import numpy as np
import psycopg2
from sqlalchemy import create_engine

def insert_database():
    sql = "INSERT INTO users(id) VALUES(%s)"
    conn = None
    try:
        engine = create_engine('postgresql+psycopg2://postgres:aleixDatabase@localhost:3306/siodb')
        client_df['id'].to_sql('users', engine, if_exists='append', index=False)  # truncates the table
        restaurant_df['id'].to_sql('restaurants', engine, if_exists='append', index=False)  # truncates the table
        relation_df['rating'].to_sql('ratings', engine, if_exists='append', index=False)  # truncates the table
        conn = engine.raw_connection()
        conn.commit()

    except Exception as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

try:
    #Read the .csv file.
    data = pd.read_csv("../../dataset.csv", delimiter=";")

    #Create a Data Frame with the user name and an identifier starts with 1.
    client_df = pd.DataFrame(data, columns=['USERS', 'id'])
    client_df['USERS'] = data['DATASET']
    client_df['id'] = np.arange(1, len(client_df)+1)

    # Create a Data Frame with the restaurant name and an identifier starts with 1.
    restaurant_names = pd.DataFrame(data.iloc[0]).iloc[1:]
    restaurant_df = pd.DataFrame(restaurant_names, columns=['id']).rename_axis('RESTAURANT').reset_index()
    restaurant_df['id'] = np.arange(1, len(restaurant_names) + 1)

    #Create a Data Frame with each user repeated for all the restaurants.
    """
    restaurant
    1
    ..
    1
    2
    ..
    2
    len = all users * 100 
    Every user appears 100 times (1 for restaurant).   
    """
    client_id = pd.DataFrame(np.repeat(client_df['id'].values,100, axis=0))
    client_id = pd.DataFrame(client_id.values, columns=['username']).reset_index()

    #Create a Data Frame with all the restaurants repeated, to make the relation with 1 user and all the restaurants, and this for all users.
    """
    restaurant
    1
    ..
    100
    1
    ..
    100
    len = all users * 100    
    """
    restaurant_id = pd.DataFrame(restaurant_df['id']).rename(columns={"id":"restaurant"})
    restaurant_id = pd.concat([restaurant_id]*len(client_df)).reset_index()
    restaurant_id['index'] = np.arange(len(restaurant_id))

    relation_df = pd.merge(left=client_id, right=restaurant_id,  left_on='index', right_on='index')

    ratings_df = pd.DataFrame(data).T
    ratings_df = ratings_df.drop('DATASET').T
    ratings_df = pd.DataFrame(ratings_df.values.ravel(), columns=['rating']).reset_index()

    relation_df = pd.merge(left=relation_df, right=ratings_df,  left_on='index', right_on='index')
    relation_df = relation_df.drop(['index'], axis=1)
    relation_df = relation_df[relation_df.rating != 99].reset_index().drop(['index'], axis=1)

    insert_database()

except FileNotFoundError:
    print('File does not exist.')

except Exception as error:
    print(error)


