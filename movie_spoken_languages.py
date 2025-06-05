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

# Load CSV
movies = pd.read_csv('Movies.csv')

# Load language lookup from database
def get_language_lookup():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT language_id, language_name FROM spoken_languages")
    rows = cursor.fetchall()
    cursor.close()
    close_connection(connection)
    return {name: lid for lid, name in rows}

# Prepare insert data
language_lookup = get_language_lookup()
insert_data = []

for i, row in movies.iterrows():
    try:
        movie_id = int(row['MovieID'])
        if pd.isna(row['SpokenLanguages']):
            continue
        languages = [lang.strip() for lang in row['SpokenLanguages'].split('|')]
        for lang in languages:
            language_id = language_lookup.get(lang)
            if language_id:
                insert_data.append((movie_id, language_id))
    except Exception as e:
        print(f"⚠️ Skipping row {i} due to error: {e}")

# Insert into movie_spoken_languages
try:
    connection = get_connection()
    cursor = connection.cursor()

    insert_query = """
        INSERT IGNORE INTO movie_spoken_languages (movie_id, language_id)
        VALUES (%s, %s)
    """

    cursor.executemany(insert_query, insert_data)
    connection.commit()

    print("movie_spoken_languages bridge table populated.")
    print(f"Total links inserted: {len(insert_data)}")

except Exception as e:
    print("Database error:", e)
    connection.rollback()
finally:
    cursor.close()
    close_connection(connection)