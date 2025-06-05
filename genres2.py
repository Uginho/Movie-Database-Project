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

# Extract unique genres
genre_series = movies['Genres'].dropna().apply(lambda x: x.split('|'))
all_genres = [genre.strip() for sublist in genre_series for genre in sublist]
unique_genres = sorted(set(all_genres))

# Prepare insert list (just genre_name)
insert_data = [(genre,) for genre in unique_genres]

# Insert into MySQL genres table
try:
    connection = get_connection()
    cursor = connection.cursor()

    insert_query = """
        INSERT IGNORE INTO genres (genre_name)
        VALUES (%s)
    """

    cursor.executemany(insert_query, insert_data)
    connection.commit()

    print("✅ Clean genres inserted into 'genres' table.")
    print(f"🎬 Total unique genres: {len(insert_data)}")

except Exception as e:
    print("❌ Database error:", e)
    connection.rollback()
finally:
    cursor.close()
    close_connection(connection)