import mysql.connector
import csv
import pandas

def get_connection():
    connection = mysql.connector.connect(host='localhost',
                                         database='imdb_backup',
                                         user='Ugo321_user',
                                         password='spring_2025',
                                         auth_plugin='mysql_native_password')
    return connection

def close_connection(connection):
    if connection:
        connection.close()

def read_database_version():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        print("You are connected to MySQL version: ", db_version)
        close_connection(connection)
    except (Exception, mysql.connector.Error) as error:
        print("Error while getting data", error)

def get_driver_detail(driver_id):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        select_query = """select * from drivers where id = %s"""
        cursor.execute(select_query, (driver_id,))
        records = cursor.fetchall()
        print("Printing Driver information")
        for row in records:
            print("Id:", row[0])
            print("Driver Name:", row[1])
        close_connection(connection)
    except (Exception, mysql.connector.Error) as error:
        print("No data available", error)


def get_csvdata():
    filename = 'Persons.csv'

    lines = open('Persons.csv', mode = 'r').readlines()

    for line in lines:
        items = line.split(',')
        #print(items[2], items[3])
        if items[3] == '1':
            print(items[2], 'M')
        elif items[3] == '2':
            print(items[2], 'F')
        else:
            print(items[2], 'Unknown')
    



get_csvdata()



