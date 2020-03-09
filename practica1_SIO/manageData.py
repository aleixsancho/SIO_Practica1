import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

try:
    connection = psycopg2.connect(user="postgres",
                                  password="aleixDatabase",
                                  host="localhost",
                                  port="3306",
                                  database="siodb")

    cursor = connection.cursor()

    median_query = '''SELECT username, restaurant, rating FROM ratings'''

    cursor.execute(median_query)
    ratings = cursor.fetchall()
    all_ratings = pd.DataFrame(ratings, columns=['userID', 'restaurantID', 'rating'])
    '''
    user_ratings = all_ratings.drop(['restaurantID'], axis=1)
    user_ratings = user_ratings.groupby('userID', as_index=False).mean()
    print(user_ratings)

    restaurant_ratings = all_ratings.drop(['userID'], axis=1)
    restaurant_ratings = restaurant_ratings.groupby('restaurantID', as_index=False).mean()
    print(restaurant_ratings)

    restaurant_visits = all_ratings.drop(['rating'], axis=1)
    restaurant_visits = restaurant_visits.groupby('restaurantID', as_index=False).count().rename(columns={'userID':'visit'})
    print(restaurant_visits)

    user_visits = all_ratings.drop(['rating'], axis=1)
    user_visits = user_visits.groupby('userID', as_index=False).count().rename(columns={'restaurantID':'visit'})
    print(user_visits)

    pivot_ratings = all_ratings.pivot_table(index=['userID'], columns=['restaurantID'], values='rating')
    print(pivot_ratings)

    user_sd = pivot_ratings.std(axis=1, skipna=True)
    print(user_sd)
    '''
    interval_df = all_ratings.drop(['restaurantID'], axis=1)
    interval_df['rating'] = interval_df['rating'].apply(np.int64)
    interval_df['rating'].replace({10:9}, inplace=True)
    interval_df = interval_df.groupby('rating', as_index=False).count().rename(columns={'userID':'count'})
    print(interval_df)

    count_plot = interval_df['count']
    ax = count_plot.plot(kind='bar')
    ax.set_xticklabels(np.arange(-9, 10))
    ax.set_title('Number of occurrences per interval of ratings')
    ax.set_ylabel('Number of occurrences')
    ax.set_xlabel('Interval of ratings')
    plt.show()
except Exception as e:
    print(e)

finally:
    # closing database connection.
    if (connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")