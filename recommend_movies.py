import argparse
import mysql.connector
from collections import Counter
from collections import defaultdict

parser = argparse.ArgumentParser(description="Recommend movies based on genre preferences.")
parser.add_argument('--user', type=int, required=True, help='User ID to generate recommendations for')
args = parser.parse_args()

user_id = args.user

print(f"✅ User ID received: {user_id}")

def get_connection():
    return mysql.connector.connect(
        host='localhost',
        database='imdb_backup',
        user='Ugo321_user',
        password='spring_2025',
        auth_plugin='mysql_native_password'
    )

conn = get_connection()
cursor = conn.cursor(dictionary=True)

# Step 3: Get all movies this user has rated
cursor.execute("""
    SELECT movie_id
    FROM temp_ratings
    WHERE user_id = %s
""", (user_id,))

rated_movies = cursor.fetchall()

# Extract the movie IDs into a list
rated_movie_ids = [row['movie_id'] for row in rated_movies]

if not rated_movie_ids:
    print(f"⚠️ User {user_id} has not rated any movies.")
    exit()
else:
    print(f"✅ User {user_id} has rated {len(rated_movie_ids)} movie(s).")

format_ids = ','.join(str(mid) for mid in rated_movie_ids)

# Step 4: Get genres of rated movies
cursor.execute(f"""
    SELECT g.genre_name
    FROM movie_genres mg
    JOIN genres g ON mg.genre_id = g.genre_id
    WHERE mg.movie_id IN ({format_ids})
""")

user_genres = [row['genre_name'] for row in cursor.fetchall()]

# Step 5: Build user genre profile
user_profile = Counter(user_genres)

print(f"✅ User genre profile:")
for genre, count in user_profile.items():
    print(f"   {genre}: {count}")

cursor.execute(f"""
    SELECT m.id, m.english_title, g.genre_name
    FROM temp_movies m
    JOIN movie_genres mg ON m.id = mg.movie_id
    JOIN genres g ON mg.genre_id = g.genre_id
    WHERE m.id NOT IN ({format_ids})
""")

rows = cursor.fetchall()

# Group genres by movie_id
movie_genres = defaultdict(list)
movie_titles = {}

for row in rows:
    movie_id = row['id']
    movie_genres[movie_id].append(row['genre_name'])
    movie_titles[movie_id] = row['english_title']

scores = {}

for movie_id, genres in movie_genres.items():
    score = 0
    for genre in genres:
        score += user_profile.get(genre, 0)
    if score > 0:
        scores[movie_id] = score

top_5 = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:5]

print(f"\n🎯 Top-5 recommended movies for user {user_id}:\n")
print(f"{'Title':40} | Score")
print("-" * 55)
for movie_id, score in top_5:
    print(f"{movie_titles[movie_id]:40} | {score}")