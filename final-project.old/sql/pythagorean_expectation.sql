-- Create a  stored procedure for calculating a few different Pythagorean expectations,
-- for home and away teams,
-- for a given number of previous games.
-- https://en.wikipedia.org/wiki/Pythagorean_expectation

-- Pythagorean Expectation using all prior data (career)
-- === === === ===
DROP TEMPORARY TABLE IF EXISTS t_home_lookup;
CREATE TEMPORARY TABLE t_home_lookup AS
SELECT
	l.game_id,
	SUM(r.home_score) AS home_r,
	SUM(r.away_score) AS home_ra,
	IF(COUNT(r.game_id)>0,COUNT(r.game_id),NULL) AS home_g
FROM game_results l
LEFT JOIN game_results r
	ON l.home_id = r.home_id
	AND r.home_priors < l.home_priors
GROUP BY l.game_id;
DROP TABLE IF EXISTS t_away_lookup;
CREATE TEMPORARY TABLE t_away_lookup AS
SELECT
	l.game_id,
	SUM(r.home_score) AS away_r,
	SUM(r.away_score) AS away_ra,
	IF(COUNT(r.game_id)>0,COUNT(r.game_id),NULL) AS away_g
FROM game_results l
LEFT JOIN game_results r
	ON l.away_id = r.home_id
	AND r.home_priors < l.away_priors
GROUP BY l.game_id;

DROP TEMPORARY TABLE IF EXISTS t_lookup;
CREATE TEMPORARY TABLE t_lookup AS
	SELECT
		h.*,
		a.away_r,
		a.away_ra,
		a.away_g,
		POWER(h.home_r + h.home_ra / h.home_g, 0.287) AS home_exp,
		POWER(a.away_r + a.away_ra / a.away_g, 0.287) AS away_exp
	FROM t_home_lookup h
	JOIN t_away_lookup a ON h.game_id = a.game_id;
-- WHERE 
-- home_g IS NOT NULL and away_g IS NOT NULL;
	
DROP TABLE IF EXISTS career_pythagorean;
CREATE TABLE career_pythagorean AS
	SELECT
		game_id,
			POWER(home_r, 2.00) / (POWER(home_r, 2.00) + POWER(home_ra, 2.00))
			AS home_200,
			POWER(away_r, 2.00) / (POWER(away_r, 2.00) + POWER(away_ra, 2.00))
			AS away_200,
			POWER(home_r, 1.83) / (POWER(home_r, 1.83) + POWER(home_ra, 1.83))
			AS home_183,
			POWER(away_r, 1.83) / (POWER(away_r, 1.83) + POWER(away_ra, 1.83))
			AS away_183,		
			POWER(home_r, home_exp) / (POWER(home_r, home_exp) + POWER(home_ra, home_exp))
			AS home_smyth,
			POWER(away_r, away_exp) / (POWER(away_r, away_exp) + POWER(away_ra, away_exp))
			AS away_smyth			
		FROM t_lookup;
SELECT *,
	home_200 - away_200 AS diff_200,
	home_183 - away_183 AS diff_183,
	home_smyth - away_smyth AS diff_smyth
FROM career_pythagorean;

DROP TEMPORARY TABLE t_home_lookup;
DROP TEMPORARY TABLE t_away_lookup;
DROP TEMPORARY TABLE t_lookup;


-- Pythagorean Expectation using all prior games in the same year (season)
-- === === === ===
DROP TEMPORARY TABLE IF EXISTS t_home_lookup;
CREATE TEMPORARY TABLE t_home_lookup AS
SELECT
	l.game_id,
	SUM(r.home_score) AS home_r,
	SUM(r.away_score) AS home_ra,
	IF(COUNT(r.game_id)>0,COUNT(r.game_id),NULL) AS home_g
FROM game_results l
LEFT JOIN game_results r
	ON l.home_id = r.home_id
	AND r.home_priors < l.home_priors
	AND YEAR(l.local_date) = YEAR(r.local_date)
GROUP BY l.game_id;
DROP TABLE IF EXISTS t_away_lookup;
CREATE TEMPORARY TABLE t_away_lookup AS
SELECT
	l.game_id,
	SUM(r.home_score) AS away_r,
	SUM(r.away_score) AS away_ra,
	IF(COUNT(r.game_id)>0,COUNT(r.game_id),NULL) AS away_g
FROM game_results l
LEFT JOIN game_results r
	ON l.away_id = r.home_id
	AND r.home_priors < l.away_priors
	AND YEAR(l.local_date) = YEAR(r.local_date)
GROUP BY l.game_id;

DROP TEMPORARY TABLE IF EXISTS t_lookup;
CREATE TEMPORARY TABLE t_lookup AS
	SELECT
		h.*,
		a.away_r,
		a.away_ra,
		a.away_g,
		POWER(h.home_r + h.home_ra / h.home_g, 0.287) AS home_exp,
		POWER(a.away_r + a.away_ra / a.away_g, 0.287) AS away_exp
	FROM t_home_lookup h
	JOIN t_away_lookup a ON h.game_id = a.game_id;
-- WHERE 
-- home_g IS NOT NULL and away_g IS NOT NULL;
	
DROP TABLE IF EXISTS season_pythagorean;
CREATE TABLE season_pythagorean AS
	SELECT
		game_id,
			POWER(home_r, 2.00) / (POWER(home_r, 2.00) + POWER(home_ra, 2.00))
			AS home_200,
			POWER(away_r, 2.00) / (POWER(away_r, 2.00) + POWER(away_ra, 2.00))
			AS away_200,
			POWER(home_r, 1.83) / (POWER(home_r, 1.83) + POWER(home_ra, 1.83))
			AS home_183,
			POWER(away_r, 1.83) / (POWER(away_r, 1.83) + POWER(away_ra, 1.83))
			AS away_183,		
			POWER(home_r, home_exp) / (POWER(home_r, home_exp) + POWER(home_ra, home_exp))
			AS home_smyth,
			POWER(away_r, away_exp) / (POWER(away_r, away_exp) + POWER(away_ra, away_exp))
			AS away_smyth			
		FROM t_lookup;
SELECT *,
	home_200 - away_200 AS diff_200,
	home_183 - away_183 AS diff_183,
	home_smyth - away_smyth AS diff_smyth
FROM expectations;

DROP TEMPORARY TABLE t_home_lookup;
DROP TEMPORARY TABLE t_away_lookup;
DROP TEMPORARY TABLE t_lookup;



DELIMITER ;
DELIMITER $$

DROP PROCEDURE IF EXISTS rolling_pythagorean$$

CREATE PROCEDURE rolling_pythagorean(
	IN n_games INT
)
BEGIN
	DROP TEMPORARY TABLE IF EXISTS t_home_lookup;
	CREATE TEMPORARY TABLE t_home_lookup AS
	SELECT
		l.game_id,
		SUM(r.home_score) AS home_r,
		SUM(r.away_score) AS home_ra,
		IF(COUNT(r.game_id)>0,COUNT(r.game_id),NULL) AS home_g
	FROM game_results l
	LEFT JOIN game_results r
		ON l.home_id = r.home_id
		AND r.home_priors BETWEEN (l.home_priors - n_games - 1) AND (l.home_priors - 1)
	GROUP BY l.game_id;

	DROP TABLE IF EXISTS t_away_lookup;
	CREATE TEMPORARY TABLE t_away_lookup AS
	SELECT
		l.game_id,
		SUM(r.home_score) AS away_r,
		SUM(r.away_score) AS away_ra,
		IF(COUNT(r.game_id)>0,COUNT(r.game_id),NULL) AS away_g
	FROM game_results l
	LEFT JOIN game_results r
		ON l.away_id = r.home_id
		AND r.home_priors BETWEEN (l.away_priors - n_games - 1) AND (l.away_priors - 1)
	GROUP BY l.game_id;

	DROP TEMPORARY TABLE IF EXISTS t_lookup;
	CREATE TEMPORARY TABLE t_lookup AS
		SELECT
			h.*,
			a.away_r,
			a.away_ra,
			a.away_g,
			POWER(h.home_r + h.home_ra / h.home_g, 0.287) AS home_exp,
			POWER(a.away_r + a.away_ra / a.away_g, 0.287) AS away_exp
		FROM t_home_lookup h
		JOIN t_away_lookup a ON h.game_id = a.game_id;
	-- WHERE 
	-- home_g IS NOT NULL and away_g IS NOT NULL;
		
	DROP TEMPORARY TABLE IF EXISTS expectations;
	CREATE TEMPORARY TABLE expectations AS
		SELECT
			game_id,
				POWER(home_r, 2.00) / (POWER(home_r, 2.00) + POWER(home_ra, 2.00))
				AS home_200,
				POWER(away_r, 2.00) / (POWER(away_r, 2.00) + POWER(away_ra, 2.00))
				AS away_200,
				POWER(home_r, 1.83) / (POWER(home_r, 1.83) + POWER(home_ra, 1.83))
				AS home_183,
				POWER(away_r, 1.83) / (POWER(away_r, 1.83) + POWER(away_ra, 1.83))
				AS away_183,		
				POWER(home_r, home_exp) / (POWER(home_r, home_exp) + POWER(home_ra, home_exp))
				AS home_smyth,
				POWER(away_r, away_exp) / (POWER(away_r, away_exp) + POWER(away_ra, away_exp))
				AS away_smyth			
			FROM t_lookup;

	SELECT *,
		home_200 - away_200 AS diff_200,
		home_183 - away_183 AS diff_183,
		home_smyth - away_smyth AS diff_smyth
	FROM expectations;
	
	DROP TEMPORARY TABLE t_home_lookup;
	DROP TEMPORARY TABLE t_away_lookup;
	DROP TEMPORARY TABLE t_lookup;
	DROP TEMPORARY TABLE expectations;
	
END $$

DELIMITER ;
