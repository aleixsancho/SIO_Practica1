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

    interval_df = all_ratings.drop(['restaurantID'], axis=1)
    interval_df['rating'] = interval_df['rating'].apply(np.int64)
    interval_df['rating'].replace({10:9}, inplace=True)
    interval_df = interval_df.groupby('rating', as_index=False).count().rename(columns={'userID':'count'})
    print(interval_df)


    ''' Show plot
    count_plot = interval_df['count']
    ax = count_plot.plot(kind='bar')
    ax.set_xticklabels(np.arange(-9, 10))
    ax.set_title('Number of occurrences per interval of ratings')
    ax.set_ylabel('Number of occurrences')
    ax.set_xlabel('Interval of ratings')
    plt.show()
    '''

    delete_decimals = all_ratings
    delete_decimals['rating'] = all_ratings['rating'].apply(np.int64)
    print(all_ratings)
    print(delete_decimals)
    delete_decimals = delete_decimals.pivot_table(index=['userID'], columns=['restaurantID'], values='rating')
    user_mode = delete_decimals.mode(axis=1)[0]
    print(user_mode)
    restaurant_mode = delete_decimals.mode()
    print(restaurant_mode)
    restaurant_ratings_sorted = pd.DataFrame(columns=['rating', 'visit'])
    restaurant_ratings_sorted['rating'] = restaurant_ratings['rating']
    restaurant_ratings_sorted['visit'] = restaurant_visits['visit']
    print(restaurant_ratings_sorted)
    restaurant_ratings_sorted = restaurant_ratings_sorted.sort_values(by=['rating'])
    print(restaurant_ratings_sorted)

    '''Show plot.
    plt.scatter(restaurant_ratings_sorted['rating'], restaurant_ratings_sorted['visit'])
    plt.title('Number of visit per restaurant rating mean')
    plt.ylabel('Number of visits')
    plt.xlabel('Restaurant rating mean')
    plt.show()
    '''
    '''
    restaurant_ratings_sorted['rating'] = restaurant_ratings_sorted['rating'].apply(np.int64)
    restaurant_ratings_sorted = restaurant_ratings_sorted.groupby(['rating']).mean().reset_index()
    print(restaurant_ratings_sorted)
    '''
    '''
    plt.bar(restaurant_ratings_sorted['rating'], restaurant_ratings_sorted['visit'])
    plt.title('Number of visit per interval restaurant rating mean')
    plt.ylabel('Number of visits')
    plt.xlabel('Restaurant rating mean')
    plt.show()
    '''
    '''
    mode_group_user = pd.DataFrame(columns=['mode', 'mean'])
    mode_group_user['mode'] = user_mode
    mode_group_user['mean'] = user_ratings['rating']
    mode_group_user = mode_group_user.groupby(['mode']).mean().reset_index()
    print(mode_group_user)

    plt.scatter(mode_group_user['mode'], mode_group_user['mean'])
    plt.title('Mean rating per interval mode')
    plt.ylabel('Mean rating')
    plt.xlabel('Interval mode')
    z = np.polyfit(mode_group_user['mode'], mode_group_user['mean'], 1)
    y = np.poly1d(z)
    plt.plot(mode_group_user['mode'], y(mode_group_user['mode']), "r--")
    plt.show()
    '''

    mean_group_user = pd.DataFrame(columns=['mode', 'mean'])
    mean_group_user['mode'] = user_mode
    mean_group_user['mean'] = user_ratings['rating'].apply(np.int64)
    mean_group_user = mean_group_user.groupby(['mean']).mean().reset_index()
    print(mean_group_user)

    '''
    plt.scatter(mean_group_user['mean'], mean_group_user['mode'])
    plt.title('Mode rating per interval mean')
    plt.ylabel('Mode rating')
    plt.xlabel('Interval mean')
    z = np.polyfit(mean_group_user['mean'], mean_group_user['mode'], 1)
    y = np.poly1d(z)
    plt.plot(mean_group_user['mean'], y(mean_group_user['mean']), "r--")
    plt.show()
    '''

    mean_counts_user = pd.DataFrame(columns=['count'])
    mean_counts_user['count'] = user_ratings['rating'].apply(np.int64)
    mean_counts_user = mean_counts_user['count'].value_counts().reset_index()
    mean_counts_user = mean_counts_user.rename(columns={'index': 'mean'})
    mean_counts_user = mean_counts_user.sort_values(by=['mean'])
    print(mean_counts_user)

    '''
    plt.scatter(mean_counts_user['mean'], mean_counts_user['count'])
    plt.title('Number of users interval mean occurrences')
    plt.ylabel('Number of occurrences')
    plt.xlabel('Interval of mean')
    plt.show()
    '''

    mean_counts_restaurant = pd.DataFrame(columns=['count'])
    mean_counts_restaurant['count'] = restaurant_ratings['rating'].apply(np.int64)
    mean_counts_restaurant = mean_counts_restaurant['count'].value_counts().reset_index()
    mean_counts_restaurant = mean_counts_restaurant.rename(columns={'index': 'mean'})
    mean_counts_restaurant = mean_counts_restaurant.sort_values(by=['mean'])
    print(mean_counts_restaurant)

    '''
    plt.scatter(mean_counts_restaurant['mean'], mean_counts_restaurant['count'])
    plt.title('Number of restaurants interval mean occurrences')
    plt.ylabel('Number of occurrences')
    plt.xlabel('Interval of mean')
    plt.show()
    '''

    prob_df = pd.DataFrame(columns=['count'])
    print(all_ratings)
    prob_df['count'] = all_ratings['rating']
    print(prob_df)
    prob_df = prob_df['count'].value_counts().reset_index()
    prob_df['probability'] = prob_df['count'] / len(user_ratings)
    prob_df = prob_df.rename(columns={'index': 'rating'})
    prob_df = prob_df.sort_values(by=['rating'])
    print(prob_df)
    plt.scatter(prob_df['rating'], prob_df['probability'])
    plt.title('Probability of each rating')
    plt.ylabel('Probability')
    plt.xlabel('Rating')
    plt.show()


except Exception as e:
    print(e)

finally:
    # closing database connection.
    if (connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")