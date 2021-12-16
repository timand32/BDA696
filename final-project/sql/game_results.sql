-- Create a final_scores table for each mlb game
DROP TABLE IF EXISTS t_game_results;
CREATE TABLE t_game_results
	SELECT
		i.game_id_ AS game_id,
		g.local_date,
		g.home_team_id AS home_id,
		g.away_team_id AS away_id,
		IF(i.home_score>i.away_score, 1, 0) AS home_won,
		i.home_score,
		i.away_score,
		i.home_score - i.away_score AS score_difference,
		i.innings,
		IF(i.home_score=i.away_score, 1, 0) AS tie,
		IF(i.innings>9, 1, 0) AS overtime,
		IF((i.innings<9) AND ((i.home_score - i.away_score)>=10), 1, 0) AS away_mercy,
		IF((i.innings<9) AND ((i.home_score - i.away_score)<=-10), 1, 0) AS home_mercy,
		IF((i.innings<9) AND (ABS(i.home_score - i.away_score)<10), 1, 0) AS ended_early
	FROM (
		SELECT
			CAST(game_id AS INTEGER) AS game_id_,
			MAX(inning.home_score) AS home_score,
			MAX(inning.away_score) AS away_score,
			MAX(inning.inning) AS innings
		FROM inning
		GROUP BY game_id
	) i
	JOIN game g ON i.game_id_ = g.game_id
	ORDER BY i.game_id_;

CREATE UNIQUE INDEX t_gr_game_home ON t_game_results (game_id,home_id);
CREATE UNIQUE INDEX t_gr_game ON t_game_results (game_id);
CREATE INDEX t_gr_home ON t_game_results (home_id);
CREATE INDEX t_gr_date ON t_game_results (local_date);


-- Add a counter for each home team's prior that will make rolling lookups easier.
DROP TABLE IF EXISTS t1_game_results;
CREATE TABLE t1_game_results
	SELECT
		l.*,
		COUNT(r.game_id) AS home_priors
	FROM t_game_results l
	LEFT JOIN t_game_results r 
		ON l.home_id = r.home_id
			AND r.game_id < l.game_id
	GROUP BY l.game_id;


CREATE UNIQUE INDEX t1_gr_game_home ON t1_game_results (game_id, home_id);
CREATE UNIQUE INDEX t1_gr_home_prior ON t1_game_results (home_id, home_priors);
CREATE UNIQUE INDEX t1_gr_game ON t1_game_results (game_id);
CREATE INDEX t1_gr_home ON t1_game_results (home_id);
CREATE INDEX t1_gr_date ON t1_game_results (local_date);
CREATE INDEX t1_gr_prior ON t1_game_results (home_priors);

-- Finally, add a counter for each away team's prior that will make rolling lookups easier.
DROP TABLE IF EXISTS game_results;
CREATE TABLE game_results
	SELECT
		l.*,
		COUNT(r.game_id) AS away_priors
	FROM t1_game_results l
	LEFT JOIN t_game_results r 
		ON l.away_id = r.home_id
			AND r.game_id < l.game_id
	GROUP BY l.game_id;

CREATE UNIQUE INDEX gr_game_home ON game_results (game_id, home_id);
CREATE UNIQUE INDEX gr_home_prior ON game_results (home_id, home_priors);
# CREATE UNIQUE INDEX gr_away_prior ON game_results (away_id, away_priors);
CREATE UNIQUE INDEX gr_game ON game_results (game_id);
CREATE INDEX gr_home ON game_results (home_id);
CREATE INDEX gr_date ON game_results (local_date);
CREATE INDEX gr_hprior ON game_results (home_priors);
CREATE INDEX gr_aprior ON game_results (away_priors);


-- DROP TABLE IF EXISTS t_game_results;
-- DROP TABLE IF EXISTS t1_game_results;
