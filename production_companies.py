import mysql.connector
import pandas as pd

def get_connection():
    return mysql.connector.connect(
        host='localhost',
        database='imdb_backup',
        user='Ugo321_user',
        password='spring_2025',
        auth_plugin='mysql_native_password'
    )

def close_connection(connection):
    if connection:
        connection.close()

# Load Movies.csv
movies = pd.read_csv('Movies.csv')

# ===== Spoken Languages =====
def extract_and_insert_unique(column_name, table_name, field_name):
    items_series = movies[column_name].dropna().apply(lambda x: x.split('|'))
    all_items = [item.strip() for sublist in items_series for item in sublist]
    unique_items = sorted(set(all_items))
    insert_data = [(item,) for item in unique_items]

    try:
        connection = get_connection()
        cursor = connection.cursor()

        insert_query = f"""
            INSERT IGNORE INTO {table_name} ({field_name})
            VALUES (%s)
        """

        cursor.executemany(insert_query, insert_data)
        connection.commit()

        print(f"Clean values inserted into '{table_name}'")
        print(f"Total unique entries: {len(insert_data)}")

    except Exception as e:
        print(f"Database error for {table_name}:", e)
        connection.rollback()
    finally:
        cursor.close()
        close_connection(connection)

# Run for spoken_languages and production_companies
extract_and_insert_unique('SpokenLanguages', 'spoken_languages', 'language_name')
extract_and_insert_unique('ProductionCompanies', 'production_companies', 'company_name')