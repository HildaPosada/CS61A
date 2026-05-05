-- Q1: 10 newest movies
CREATE TABLE newest AS
  SELECT title, year FROM titles ORDER BY year DESC LIMIT 10;

-- Q2: Movies with a character whose name includes "dog"
CREATE TABLE dog_movies AS
  SELECT title, character
  FROM titles, principals
  WHERE titles.tconst = principals.tconst
    AND character LIKE '%dog%';

-- Q3: Actors who have been the lead in more than 10 movies
CREATE TABLE leads AS
  SELECT name, COUNT(*) AS lead_roles
  FROM names, principals
  WHERE names.nconst = principals.nconst
    AND ordering = 1
  GROUP BY names.nconst
  HAVING lead_roles > 10;

-- Q4: Number of movies over 3 hours long per decade
CREATE TABLE long_movies AS
  SELECT (year / 10) * 10 || 's' AS decade, COUNT(*) AS count
  FROM titles
  WHERE runtime > 180
  GROUP BY decade
  ORDER BY decade;
