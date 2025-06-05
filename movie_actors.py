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

# Load Persons.csv
people = pd.read_csv('Persons.csv')

# Since there's no 'Role' column, we skip filtering and use all rows
actors = people

# Prepare insert data: (movie_id, person_id)
insert_data = []
skipped = 0
skipped_samples = []

for i, row in actors.iterrows():
    try:
        movie_id = int(row['MovieID'])
        person_id = int(row['CastID'])
        insert_data.append((movie_id, person_id))
    except Exception as e:
        skipped += 1
        if skipped <= 10:
            skipped_samples.append(f"Row {i}: {e} | MovieID: {row['MovieID']} | CastID: {row['CastID']}")
        continue

# Insert into movie_actors
try:
    connection = get_connection()
    cursor = connection.cursor()

    insert_query = """
        INSERT IGNORE INTO movie_actors (movie_id, person_id)
        VALUES (%s, %s)
    """

    cursor.executemany(insert_query, insert_data)
    connection.commit()

except Exception as e:
    print("❌ Database error:", e)
    connection.rollback()
finally:
    cursor.close()
    close_connection(connection)

    # ✅ Final summary
    print("movie_actors bridge table populated.")
    print(f"Total links inserted: {len(insert_data)}")
    print(f"Total rows skipped due to invalid MovieID or CastID: {skipped}")

    if skipped_samples:
        print("\n📌 Sample skipped rows (showing up to 10):")
        for sample in skipped_samples:
            print("  -", sample)