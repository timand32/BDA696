-- Create a  stored procedure for calculating a few different Pythagorean expectations,
-- for home and away teams,
-- for a given number of previous games.
-- https://en.wikipedia.org/wiki/Pythagorean_expectation
DELIMITER ;
DELIMITER $$

DROP PROCEDURE IF EXISTS pythagorean$$

CREATE PROCEDURE pythagorean(
	IN n_games INT
)
BEGIN
	DROP TABLE IF EXISTS t_home_lookup;
	CREATE TABLE t_home_lookup AS
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
	CREATE TABLE t_away_lookup AS
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

	DROP TABLE IF EXISTS t_lookup;
	CREATE TABLE t_lookup AS
		SELECT
			h.*,
			a.away_r,
			a.away_ra,
			a.away_g,
			POWER(h.home_r + h.home_ra / h.home_g, 0.287) AS home_exp,
			POWER(a.away_r + a.away_ra / a.away_g, 0.287) AS away_exp
		FROM t_home_lookup h
		JOIN t_away_lookup a ON h.game_id = a.game_id
		WHERE 
			home_g IS NOT NULL and away_g IS NOT NULL;
		
	DROP TABLE IF EXISTS expectations;
	CREATE TABLE expectations AS
		SELECT
			game_id,
			IF(home_r<=0 OR home_ra<=0, 0,
				POWER(home_r, 2.00) / (POWER(home_r, 2.00) + POWER(home_ra, 2.00))
			) AS home_200,
			IF(away_r<=0 OR away_ra<=0, 0,
				POWER(away_r, 2.00) / (POWER(away_r, 2.00) + POWER(away_ra, 2.00))
			) AS away_200,
			IF(home_r<=0 OR home_ra<=0, 0,
				POWER(home_r, 1.83) / (POWER(home_r, 1.83) + POWER(home_ra, 1.83))
			) AS home_183,
			IF(away_r<=0 OR away_ra<=0, 0,
				POWER(away_r, 1.83) / (POWER(away_r, 1.83) + POWER(away_ra, 1.83))
			) AS away_183,		
			IF(home_r<=0 OR home_ra<=0, 0,
				POWER(home_r, home_exp) / (POWER(home_r, home_exp) + POWER(home_ra, home_exp))
			) AS home_smyth,
			IF(away_r<=0 OR away_ra<=0, 0,
				POWER(away_r, away_exp) / (POWER(away_r, away_exp) + POWER(away_ra, away_exp))
			) AS away_smyth			
			FROM t_lookup;

	SELECT *,
		home_200 - away_200 AS diff_200,
		home_183 - away_183 AS diff_183,
		home_smyth - away_smyth AS diff_smyth
	FROM expectations;
	
	DROP TABLE t_home_lookup;
	DROP TABLE t_away_lookup;
	DROP TABLE t_lookup;
	DROP TABLE expectations;
	
END $$

DELIMITER ;

CALL pythagorean(1);

