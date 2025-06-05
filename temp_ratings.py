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

# Load Ratings.csv with correct column names
ratings = pd.read_csv('Ratings2.csv')

# Optional: Check that UserID 9 exists
print("Top users:\n", ratings['UserID'].value_counts().head(10))

# Clean and prepare insert data
insert_data = []

for index, row in ratings.iterrows():
    try:
        user_id = int(row['UserID']) if pd.notna(row['UserID']) else None
        movie_id = int(row['MovieID']) if pd.notna(row['MovieID']) else None
        rating = float(row['Rating']) if pd.notna(row['Rating']) else None
        date = pd.to_datetime(row['Date'], errors='coerce') if pd.notna(row['Date']) else None

        insert_data.append((user_id, movie_id, rating, date))
    except Exception as e:
        print(f"⚠️ Skipping row {index} due to error: {e}")

# Insert into MySQL
try:
    conn = get_connection()
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO temp_ratings (
            user_id, movie_id, rating, date
        ) VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            rating = VALUES(rating),
            date = VALUES(date)
    """

    cursor.executemany(insert_query, insert_data)
    conn.commit()

    print("✅ Ratings insert/update complete!")
    print(f"🧾 Total rows processed: {len(insert_data)}")

except Exception as e:
    print("❌ Database error:", e)
    conn.rollback()
finally:
    cursor.close()
    close_connection(conn)