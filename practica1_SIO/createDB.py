import psycopg2
try:
    connection = psycopg2.connect(user = "postgres",
                                  password = "aleixDatabase",
                                  host = "localhost",
                                  port = "3306",
                                  database = "siodb")

    cursor = connection.cursor()

    #cursor.execute('''DROP TABLE users, restaurants, ratings''')

    create_table_users = '''CREATE TABLE users (
                                id INTEGER NOT NULL UNIQUE,
                                PRIMARY KEY (id)
                                );'''

    create_table_restaurants = '''CREATE TABLE restaurants (
                                id INTEGER NOT NULL UNIQUE,
                                PRIMARY KEY (id)
                                );'''

    create_table_ratings = '''CREATE TABLE ratings (
                                rating INTEGER NOT NULL,
                                username INTEGER NOT NULL,
                                restaurant INTEGER NOT NULL
                                FOREIGN KEY (username) REFERENCES users (id),
                                FOREIGN KEY (restaurant) REFERENCES restaurants (id)
                                );'''

    cursor.execute(create_table_users)
    cursor.execute(create_table_restaurants)
    cursor.execute(create_table_ratings)
    connection.commit()
    print("Table created successfully in PostgreSQL ")

except (Exception, psycopg2.DatabaseError) as error:
    print("Error while creating PostgreSQL table", error)
finally:
    # closing database connection.
    if (connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")