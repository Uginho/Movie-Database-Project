-- ALL CREATE TABLES:
-- USE imdb_backup;
-- USE imdb;

-- CREATE TABLE temp_movies (
-- id INT UNSIGNED,
-- title VARCHAR(50),
-- year INT,
-- original_language VARCHAR(50),
-- original_title VARCHAR(50),
-- english_title VARCHAR(50),
-- budget INT UNSIGNED DEFAULT NULL,
-- revenue INT UNSIGNED DEFAULT NULL,
-- PRIMARY KEY(id)
-- );
-- ALTER TABLE temp_movies
-- ADD COLUMN production_countries VARCHAR(100);
-- ALTER TABLE temp_movies
-- MODIFY COLUMN production_countries VARCHAR(250);


-- CREATE TABLE temp_ratings (
-- user_id INT UNSIGNED,
-- movie_id INT UNSIGNED,
-- rating FLOAT,
-- date DATE,
-- PRIMARY KEY(user_id)
-- );


-- CREATE TABLE temp_people (
-- person_id INT UNSIGNED AUTO_INCREMENT,
-- name VARCHAR(100),
-- birth INT,
-- gender char(1),
-- PRIMARY KEY(person_id)
-- );
-- INSERT INTO temp_people SELECT * FROM people;
-- ALTER TABLE temp_people ADD COLUMN gender CHAR(1) DEFAULT NULL;
-- ALTER TABLE temp_people
-- DROP PRIMARY KEY


-- CREATE TABLE movie_actors (
-- movie_id INT UNSIGNED,
-- person_id INT UNSIGNED,
-- PRIMARY KEY(movie_id, person_id),
-- FOREIGN KEY (movie_id) REFERENCES temp_movies(id),
-- FOREIGN KEY (person_id) REFERENCES temp_people(person_id)
-- );


-- CREATE TABLE movie_production_companies (
-- movie_id INT UNSIGNED,
-- company_id INT UNSIGNED,
-- PRIMARY KEY(movie_id, company_id),
-- FOREIGN KEY (movie_id) REFERENCES temp_movies(id),
-- FOREIGN KEY (company_id) REFERENCES production_companies(company_id)
-- );


-- CREATE TABLE movie_spoken_languages (
-- movie_id INT UNSIGNED,
-- language_id INT UNSIGNED,
-- PRIMARY KEY(movie_id, language_id),
-- FOREIGN KEY (movie_id) REFERENCES temp_movies(id),
-- FOREIGN KEY (language_id) REFERENCES spoken_languages(language_id)
-- );


-- CREATE TABLE movie_genres (
-- movie_id INT UNSIGNED,
-- genre_id INT UNSIGNED,
-- PRIMARY KEY(movie_id, genre_id),
-- FOREIGN KEY (movie_id) REFERENCES temp_movies(id),
-- FOREIGN KEY (genre_id) REFERENCES genres(genre_id)
-- );


-- CREATE TABLE spoken_languages (
-- language_id INT UNSIGNED AUTO_INCREMENT,
-- language_name VARCHAR(50) UNIQUE,
-- PRIMARY KEY(language_id)
-- );


-- CREATE TABLE genres (
-- genre_id INT UNSIGNED AUTO_INCREMENT,
-- genre_name VARCHAR(100) UNIQUE,
-- PRIMARY KEY(genre_id)
-- );


-- CREATE TABLE production_companies (
-- company_id INT UNSIGNED AUTO_INCREMENT,
-- company_name VARCHAR(150) UNIQUE,
-- PRIMARY KEY(company_id)
-- );