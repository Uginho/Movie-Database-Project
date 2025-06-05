import mysql.connector
import pandas as pd

# DB Connection
def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='Ugo321_user',
        password='spring_2025',
        database='imdb',
        auth_plugin='mysql_native_password'
    )

def close_connection(connection):
    if connection:
        connection.close()

# Load and prepare Ratings.csv
ratings_df = pd.read_csv('Ratings.csv')

# Group by MovieID to calculate average rating and vote count
ratings_grouped = ratings_df.groupby('MovieID').agg(
    rating=('Rating', 'mean'),
    votes=('Rating', 'count')
).reset_index()

print(ratings_grouped.columns)

# Round the rating to 1 decimal
ratings_grouped['rating'] = ratings_grouped['rating'].round(1)

# Load Persons.csv (for stars table)
persons_df = pd.read_csv('Persons.csv')

# Rename CastID → person_id
persons_df = persons_df.rename(columns={'CastID': 'person_id'})

# Only keep MovieID and person_id columns
stars_data = persons_df[['MovieID', 'person_id']].dropna()

# Remove duplicates
stars_data = stars_data.drop_duplicates()

try:
    connection = get_connection()
    cursor = connection.cursor()

    # Insert into ratings table
    ratings_insert_query = """
        INSERT INTO ratings (MovieID, rating, votes)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE
            rating = VALUES(rating),
            votes = VALUES(votes);
    """
    ratings_records = [
        (int(row['MovieID']), float(row['rating']), int(row['votes']))
        for _, row in ratings_grouped.iterrows()
    ]
    cursor.executemany(ratings_insert_query, ratings_records)
    print(f"✅ Inserted/Updated {len(ratings_records)} rows into ratings")

    # Insert into stars table
    stars_insert_query = """
        INSERT IGNORE INTO stars (MovieID, personid)
        VALUES (%s, %s);
    """
    stars_records = [
        (int(row['MovieID']), row['person_id'])
        for _, row in stars_data.iterrows()
    ]
    cursor.executemany(stars_insert_query, stars_records)
    print(f"✅ Inserted {len(stars_records)} rows into stars")

    connection.commit()

except Exception as e:
    print("❌ Error:", e)
    connection.rollback()
finally:
    cursor.close()
    close_connection(connection)