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

# Load genre lookup from database
def get_genre_lookup():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT genre_id, genre_name FROM genres")
    rows = cursor.fetchall()
    cursor.close()
    close_connection(connection)
    return {name: gid for gid, name in rows}

# Prepare insert data
genre_lookup = get_genre_lookup()
insert_data = []

for i, row in movies.iterrows():
    try:
        movie_id = int(row['MovieID'])
        if pd.isna(row['Genres']):
            continue
        genres = [g.strip() for g in row['Genres'].split('|')]
        for genre in genres:
            genre_id = genre_lookup.get(genre)
            if genre_id:
                insert_data.append((movie_id, genre_id))
    except Exception as e:
        print(f"⚠️ Skipping row {i} due to error: {e}")

# Insert into movie_genres
try:
    connection = get_connection()
    cursor = connection.cursor()

    insert_query = """
        INSERT IGNORE INTO movie_genres (movie_id, genre_id)
        VALUES (%s, %s)
    """

    cursor.executemany(insert_query, insert_data)
    connection.commit()

    print("movie_genres bridge table populated.")
    print(f"Total links inserted: {len(insert_data)}")

except Exception as e:
    print("Database error:", e)
    connection.rollback()
finally:
    cursor.close()
    close_connection(connection)
    