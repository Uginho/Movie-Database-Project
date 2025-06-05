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

# Load company lookup from DB
def get_company_lookup():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT company_id, company_name FROM production_companies")
    rows = cursor.fetchall()
    cursor.close()
    close_connection(connection)
    return {name: cid for cid, name in rows}

# Prepare insert data
company_lookup = get_company_lookup()
insert_data = []

for i, row in movies.iterrows():
    try:
        movie_id = int(row['MovieID'])
        if pd.isna(row['ProductionCompanies']):
            continue
        companies = [c.strip() for c in row['ProductionCompanies'].split('|')]
        for company in companies:
            company_id = company_lookup.get(company)
            if company_id:
                insert_data.append((movie_id, company_id))
    except Exception as e:
        print(f"⚠️ Skipping row {i} due to error: {e}")

# Insert into movie_production_companies
try:
    connection = get_connection()
    cursor = connection.cursor()

    insert_query = """
        INSERT IGNORE INTO movie_production_companies (movie_id, company_id)
        VALUES (%s, %s)
    """

    cursor.executemany(insert_query, insert_data)
    connection.commit()

    print("movie_production_companies bridge table populated.")
    print(f"Total links inserted: {len(insert_data)}")

except Exception as e:
    print("Database error:", e)
    connection.rollback()
finally:
    cursor.close()
    close_connection(connection)