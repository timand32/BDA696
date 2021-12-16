-- Create a table containing only MLB teams.
DROP TABLE IF EXISTS mlb_teams;
CREATE TABLE mlb_teams
SELECT 
	team_id,
	name_full,
	league, 
	division
FROM team
WHERE league != "";

