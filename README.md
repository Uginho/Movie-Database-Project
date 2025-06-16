
# Movie + People Data Integration Project

## Overview
This project involves integrating movie and people data into a MySQL database (`imdb`), loading supplemental data from CSV files using Python, and performing various queries and transformations to prepare the data for analysis. The project also includes tracking package deliveries in a separate `packaroo` database and extracting reports from CSV and SQL sources.

## Technologies Used
- MySQL (via MySQL Workbench)
- Python 3 (via IDLE)
- Pandas for data processing
- CSV module for file parsing
- MySQL Connector/Python for database interaction

## MySQL Tables Created

### temp_people
```sql
CREATE TABLE temp_people (
    id INT UNSIGNED,
    name TEXT,
    birth YEAR,
    gender CHAR(1)
);
```

### testmovies
Created to support bulk movie insertion/update from a CSV file.

## Python Functions and Scripts

### Reading a CSV and Printing Contents
```python
import csv

def get_csvdata():
    filename = 'Persons.csv'
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            headers = next(reader)
            print("Headers:", headers)
            for row in reader:
                print(row)
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
```

### Reading CSV and Bulk Inserting/Updating to MySQL
Reads Movies.csv, cleans values, and uses executemany() for bulk insert/update
into the 'testmovies' table in the 'imdb' database.
Includes null-checking, handling for missing values, and logic to decide whether to insert or update based on presence in the existing DB.

### Tracking Report Query from packaroo Database
```python
def get_tracking_report(package_id):
    connection = get_connection()
    cursor = connection.cursor()
    query = """
        SELECT
            DATE_FORMAT(scans.timestamp,'%Y-%m-%d %H:%i:%s') AS timestamp,
            scans.action,
            addresses.address
        FROM scans
        JOIN addresses ON scans.address_id = addresses.id
        WHERE scans.action = 'Drop'
          AND scans.package_id = %s
    """
    cursor.execute(query, (package_id,))
    records = cursor.fetchall()
    for row in records:
        print(f"'{row[0]}', '{row[1]}', '{row[2]}'")
```

## Common SQL Queries Used

### Count total movies
```sql
USE myMovies;
SELECT COUNT(*) FROM movies;
```

### Find a movie or person named "Zolushka"
```sql
SELECT * FROM movies WHERE title LIKE '%Zolushka%'
UNION
SELECT * FROM people WHERE name LIKE '%Zolushka%';
```

### Timestamp cleanup in SQL
```sql
SELECT DATE_FORMAT(scans.timestamp, '%Y-%m-%d %H:%i:%s') AS timestamp
FROM scans;
```

## Best Practices Implemented
- Used parameterized queries (`%s`) to prevent SQL injection
- Used `executemany()` for efficient bulk inserts/updates
- Data cleaning included null-checking for fields before DB insertion
- Separated database connection logic into `get_connection()` and `close_connection()` functions
- SQL formatting and string parsing were handled using `DATE_FORMAT` and Python formatting logic

## Next Steps
- Automate insertions into `temp_people`
- Normalize the `testmovies` schema further (e.g., move languages or genres into separate tables)
- Build a command-line interface or lightweight GUI for user interaction
