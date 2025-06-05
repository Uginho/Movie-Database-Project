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

def close_connection(conn):
    if conn:
        conn.close()

# Load data from CSV
movies = pd.read_csv('Movies.csv')

# Convert release date to extract year
movies['ReleaseDate'] = pd.to_datetime(movies['ReleaseDate'], errors='coerce')
movies['year'] = movies['ReleaseDate'].dt.year

# Prepare insert data
insert_data = []

for i, row in movies.iterrows():
    if i % 1000 == 0:
        print(f"Processing row: {i}")
    
    try:
        movie_id = int(row['MovieID']) if pd.notna(row['MovieID']) else None
        title = row['OriginalTitle'] if pd.notna(row['OriginalTitle']) else None
        year = int(row['year']) if pd.notna(row['year']) else None
        original_language = row['OriginalLanguage'] if pd.notna(row['OriginalLanguage']) else None
        original_title = row['OriginalTitle'] if pd.notna(row['OriginalTitle']) else None
        english_title = row['EnglishTitle'] if pd.notna(row['EnglishTitle']) else None
        budget = int(row['Budget']) if pd.notna(row['Budget']) else None
        revenue = int(row['Revenue']) if pd.notna(row['Revenue']) else None
        runtime = int(row['Runtime']) if pd.notna(row['Runtime']) else None
        production_countries = row['ProductionCountries'] if pd.notna(row['ProductionCountries']) else None

        insert_data.append((
            movie_id,
            title,
            year,
            original_language,
            original_title,
            english_title,
            budget,
            revenue,
            runtime,
            production_countries
        ))
    except Exception as e:
        print(f"⚠️ Skipping row {i} due to error: {e}")

# Insert into MySQL
try:
    conn = get_connection()
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO temp_movies (
            id, title, year, original_language,
            original_title, english_title, budget, revenue, runtime, ProductionCountries
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            title = VALUES(title),
            year = VALUES(year),
            original_language = VALUES(original_language),
            original_title = VALUES(original_title),
            english_title = VALUES(english_title),
            budget = VALUES(budget),
            revenue = VALUES(revenue),
            runtime = VALUES(runtime),
            ProductionCountries = VALUES(ProductionCountries)
    """

    cursor.executemany(insert_query, insert_data)
    conn.commit()

    print("✅ temp_movies updated successfully!")
    print(f"🎬 Total rows processed: {len(insert_data)}")

except Exception as e:
    print("❌ Database error:", e)
    conn.rollback()
finally:
    cursor.close()
    close_connection(conn)





