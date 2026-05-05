CREATE TABLE parents (parent TEXT, child TEXT);
INSERT INTO parents VALUES
  ('ace', 'bella'),
  ('ace', 'charlie'),
  ('daisy', 'hank'),
  ('finn', 'ace'),
  ('finn', 'daisy'),
  ('finn', 'ginger'),
  ('ellie', 'finn');

CREATE TABLE dogs (name TEXT, fur TEXT, height INTEGER);
INSERT INTO dogs VALUES
  ('ace',     'long',  26),
  ('bella',   'short', 52),
  ('charlie', 'long',  47),
  ('daisy',   'long',  46),
  ('ellie',   'short', 35),
  ('finn',    'curly', 32),
  ('ginger',  'short', 28),
  ('hank',    'curly', 31);

CREATE TABLE sizes (size TEXT, min INTEGER, max INTEGER);
INSERT INTO sizes VALUES
  ('toy',      24, 28),
  ('mini',     28, 35),
  ('medium',   35, 45),
  ('standard', 45, 60);

-- Q1: All dogs with parents ordered by decreasing height of their parent
CREATE TABLE by_parent_height AS
  SELECT child FROM parents, dogs WHERE parent = name ORDER BY height DESC;

-- Q2: The size of each dog
CREATE TABLE size_of_dogs AS
  SELECT name, size FROM dogs, sizes WHERE height > min AND height <= max;

-- Q3: Siblings that share the same size
CREATE TABLE siblings AS
  SELECT a.child AS first, b.child AS second
  FROM parents AS a, parents AS b
  WHERE a.parent = b.parent AND a.child < b.child;

CREATE TABLE sentences AS
  SELECT 'The two siblings, ' || first || ' and ' || second || ', have the same size: ' || s1.size
  FROM siblings, size_of_dogs AS s1, size_of_dogs AS s2
  WHERE first = s1.name AND second = s2.name AND s1.size = s2.size;

-- Q4: Height range for fur types where all heights are within 30% of the average
CREATE TABLE low_variance AS
  SELECT fur, MAX(height) - MIN(height) AS height_range
  FROM dogs
  GROUP BY fur
  HAVING MIN(height) >= 0.7 * AVG(height) AND MAX(height) <= 1.3 * AVG(height);
