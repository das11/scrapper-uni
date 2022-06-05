from mysql.connector import connect, Error

def init_db():
    try:
        with connect(
            host="localhost",
            port="8889",
            user="root",
            password="root",
        ) as connection:
            cursor = connection.cursor()
            inject_data(cursor)
    except Error as e:
        print(e)

def inject_data(cursor):
    show_db_query = "SHOW DATABASES"
    cursor.execute(show_db_query)
    for db in cursor:
        print(db)