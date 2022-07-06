from mysql.connector import connect, Error
import time

start_time = time.time()


def init_db():
    connection = connect(
            host="localhost",
            port="8889",
            user="root",
            password="root",
            database="scrapper",
        ) 
    cursor = connection.cursor()
    return connection, cursor

def inject_data(url, data):
    connection, cursor = init_db()

    show_db_query = "SHOW DATABASES"
    inject_text_query = """
    INSERT INTO scrape (url, data_blob)
    VALUES (%s, %s)
    """
    values = (url, data)


    cursor.execute(inject_text_query, values)
    connection.commit()

    for db in cursor:
        print(db)

def search_data(keyword):
    connection, cursor = init_db()

    param = "%{}%".format(keyword)
    search_query = """
    SELECT *
    FROM scrape
    WHERE data_blob LIKE %s
    """

    cursor.execute(search_query, (param,))
    data = cursor.fetchall()

    return data

def search_module():
    keyword = input("Enter keyword to search : ")
    data = search_data(keyword)

    length = len(data)
    print("Rows :: " + str(length))
    for row in data:
        print("############################################################################################################")
        print("ID -> " + str(row[0]))
        print("URL -> " + row[1])
        print("Blob -> \n" + row[2])
        print("Exec Time : ", (time.time() - start_time))
        print("############################################################################################################")