-- Quel est le film le plus long ?

SELECT title, MAX(duration)
FROM movies;

-- Quels sont les 5 films les mieux notés ?

SELECT title, score
FROM movies
ORDER BY score DESC
LIMIT 5;

-- Dans combien de films a joué Morgan Freeman ? Tom Cruise ?

SELECT COUNT(title)
FROM movies
WHERE top_cast like '%Morgan Freeman%';

SELECT COUNT(title)
FROM movies
WHERE top_cast like '%Tom Cruise%';

-- Quels sont les 3 meilleurs films d'horreur ? Dramatique ? Comique ?

SELECT title, score
FROM movies 
WHERE genre like '%Horror%'
ORDER BY score DESC 
LIMIT 3;

SELECT title, score
FROM movies 
WHERE genre like '%Drama%'
ORDER BY score DESC 
LIMIT 3;

SELECT title, score
FROM movies 
WHERE genre like '%Comedy%'
ORDER BY score DESC 
LIMIT 3;

-- Parmi les 100 films les mieux notés, quel pourcentage sont américains ? Français ?

SELECT country, score, COUNT(title)
FROM movies
WHERE title in (
SELECT title
FROM movies
ORDER BY score DESC
LIMIT 100)
GROUP BY country;

-- Quelle est la durée moyenne d’un film en fonction du genre ?

SELECT genre, AVG(duration)
FROM movies
GROUP BY genre;

-- En fonction du genre, afficher la liste des films les plus longs.

SELECT title, genre, MAX(duration)
FROM movies 
GROUP BY genre;

