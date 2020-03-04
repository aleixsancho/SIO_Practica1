import psycopg2
try:
    connection = psycopg2.connect(user = "postgres",
                                  password = "aleixDatabase",
                                  host = "localhost",
                                  port = "3306",
                                  database = "siodb")

    cursor = connection.cursor()

    cursor.execute('''DROP TABLE users, restaurants, ratings''')
    connection.commit()
except Exception as e:
    print(e)
finally:
    # closing database connection.
    if (connection):
        cursor.close()
        connection.close()
